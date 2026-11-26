"""Mode cloud : envoi des documents vers un bucket Cloudflare R2 (API compatible S3), 15/10/2026.

- Les identifiants (clé d'accès et clé secrète R2) sont saisis par le gérant dans la plateforme et conservés dans le trousseau
  macOS (service « MDC-Plateforme-R2 ») : ils ne sont écrits dans aucun fichier. Le numéro de compte, le bucket et le préfixe sont dans r2_config.json.
- Signature AWS SigV4 écrite avec la bibliothèque standard (pas de dépendance à installer). Région « auto », service « s3ʼ.
- Rangement dans le bucket : <préfixe>/<dossier>/<nom du fichier>. Un nouvel envoi du même document remplace la version précédente.
- Le bucket doit rester PRIVÉ (pas d'accès public) : il contient des documents de clients."""
import os, json, hmac, hashlib, mimetypes, subprocess, datetime as dt, urllib.request, urllib.error
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, 'r2_config.json')
SERVICE = 'MDC-Plateforme-R2'

def _env():
    """Lit le fichier .env du dossier de l'application (clés R2_...)."""
    d = {}
    try:
        for l in open(os.path.join(HERE, '.env'), encoding='utf-8'):
            l = l.strip()
            if l and not l.startswith('#') and '=' in l:
                k, v = l.split('=', 1); d[k.strip()] = v.strip().strip('\'"')
    except Exception: pass
    return d

def env_complet():
    e = _env()
    return all(e.get(k) for k in ('R2_ACCOUNT_ID', 'R2_BUCKET', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY'))

def config():
    try: c = json.load(open(CONFIG, encoding='utf-8'))
    except Exception: c = {}
    e = _env()
    if not c.get('account') and e.get('R2_ACCOUNT_ID') and e.get('R2_BUCKET'):
        c = {'account': e['R2_ACCOUNT_ID'], 'bucket': e['R2_BUCKET'], 'prefixe': e.get('R2_PREFIX', 'MDC'), **c}
    if env_complet() and 'actif' not in c: c['actif'] = True
    return c

def save_config(c):
    json.dump(c, open(CONFIG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def set_keys(account, keyid, secret):
    subprocess.run(['security', 'add-generic-password', '-U', '-s', SERVICE, '-a', account, '-w', f'{keyid}:{secret}'], capture_output=True, check=True)

def get_keys(account):
    e = _env()
    if e.get('R2_ACCESS_KEY_ID') and e.get('R2_SECRET_ACCESS_KEY') and e.get('R2_ACCOUNT_ID', account) == account:
        return e['R2_ACCESS_KEY_ID'], e['R2_SECRET_ACCESS_KEY']
    r = subprocess.run(['security', 'find-generic-password', '-s', SERVICE, '-a', account, '-w'], capture_output=True, text=True)
    if r.returncode != 0 or ':' not in r.stdout: return None, None
    k, s = r.stdout.strip().split(':', 1); return k, s

def _hmac(key, msg): return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def _request(method, account, bucket, key='', query='', body=b'', keyid=None, secret=None, content_type=None):
    host = f'{account}.r2.cloudflarestorage.com'
    uri = '/' + bucket + ('/' + quote(key, safe='/-_.~') if key else '')
    now = dt.datetime.utcnow(); amz = now.strftime('%Y%m%dT%H%M%SZ'); day = now.strftime('%Y%m%d')
    ph = hashlib.sha256(body).hexdigest()
    headers = {'host': host, 'x-amz-content-sha256': ph, 'x-amz-date': amz}
    signed = ';'.join(sorted(headers))
    canon = '\n'.join([method, uri, query, ''.join(f'{h}:{headers[h]}\n' for h in sorted(headers)), signed, ph])
    scope = f'{day}/auto/s3/aws4_request'
    sts = '\n'.join(['AWS4-HMAC-SHA256', amz, scope, hashlib.sha256(canon.encode('utf-8')).hexdigest()])
    k = _hmac(_hmac(_hmac(_hmac(('AWS4' + secret).encode('utf-8'), day), 'auto'), 's3'), 'aws4_request')
    sig = hmac.new(k, sts.encode('utf-8'), hashlib.sha256).hexdigest()
    req = urllib.request.Request(f'https://{host}{uri}' + (f'?{query}' if query else ''), data=body if method in ('PUT', 'POST') else None, method=method)
    for h, v in headers.items():
        if h != 'host': req.add_header(h, v)
    if content_type: req.add_header('Content-Type', content_type)
    req.add_header('Authorization', f'AWS4-HMAC-SHA256 Credential={keyid}/{scope}, SignedHeaders={signed}, Signature={sig}')
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except urllib.error.URLError as e:
        if 'HANDSHAKE' in str(e).upper() or 'Name or service' in str(e) or 'nodename' in str(e):
            raise RuntimeError("Cloudflare ne reconnaît pas ce numéro de compte (Account ID) : vérifiez-le sur la page R2 de votre tableau de bord.")
        raise RuntimeError(f'Connexion à Cloudflare R2 impossible : {e.reason}')

def tester(account, bucket, keyid, secret):
    code, body = _request('GET', account, bucket, query='list-type=2&max-keys=1', keyid=keyid, secret=secret)
    if code != 200:
        msg = body.decode('utf-8', 'ignore')
        raise RuntimeError(f'R2 a refusé la connexion (code {code}) : ' + (msg[msg.find('<Code>') + 6: msg.find('</Code>')] if '<Code>' in msg else msg[:200]))

def _segment(s):
    return ''.join(c for c in s if c not in '\\:*?"<>|').strip() or 'SANS_NOM'

def envoyer_fichier(path, dossier):
    cfg = config(); account, bucket = cfg.get('account'), cfg.get('bucket')
    keyid, secret = get_keys(account) if account else (None, None)
    if not (account and bucket and keyid): raise RuntimeError("Le mode cloud n'est pas configuré : ouvrez « ☁️ Cloud R2 ».")
    prefixe = (cfg.get('prefixe') or '').strip('/')
    cle = '/'.join(x for x in [prefixe, _segment(dossier), os.path.basename(path)] if x)
    body = open(path, 'rb').read()
    code, rep = _request('PUT', account, bucket, key=cle, body=body, keyid=keyid, secret=secret,
                         content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream')
    if code not in (200, 201): raise RuntimeError(f'Envoi refusé par R2 (code {code}) pour {os.path.basename(path)}')
    return cle, len(body)
