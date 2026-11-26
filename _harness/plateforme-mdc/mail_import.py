"""Import des pièces jointes reçues par mail vers Documents/DOCUMENTS_RECUS_PAR_MAIL (15/10/2026).

- Connexion IMAP à Gmail en LECTURE SEULE (les mails ne sont ni modifiés, ni marqués comme lus, ni supprimés).
- Le mot de passe d'application Google est saisi par le gérant dans la plateforme et conservé dans le trousseau macOS
  (service « MDC-Plateforme-IMAP ») : il n'est écrit dans aucun fichier.
- Seuls les mails de la boîte de réception, reçus depuis la date choisie, et envoyés par une autre adresse que celle du compte, sont lus.
- Pièces gardées : documents (pdf, doc, docx, xls, xlsx, ppt, pptx, csv, txt, zip) et images de plus de 60 Ko (scans, photos de pièces).
  Les petites images (logos, signatures) sont ignorées.
- Rangement : DOCUMENTS_RECUS_PAR_MAIL/<AAAA-MM-JJ> — <expéditeur> — <objet>/<fichier>. Jamais d'écrasement.
- Chaque mail n'est importé qu'une fois (identifiant du message mémorisé dans mail_index.json, avec l'expéditeur, l'objet et la date)."""
import os, json, re, imaplib, email, subprocess, datetime as dt
from email.header import decode_header, make_header
from email.utils import parseaddr, parsedate_to_datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = '/Users/bilefilsseverin/Documents/DOCUMENTS_RECUS_PAR_MAIL/'
CONFIG = os.path.join(HERE, 'mail_config.json')
INDEX = os.path.join(HERE, 'mail_index.json')
SERVICE = 'MDC-Plateforme-IMAP'
DOC_EXT = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.txt', '.zip', '.rtf', '.odt', '.ods'}
IMG_EXT = {'.jpg', '.jpeg', '.png', '.heic', '.tif', '.tiff'}

def _load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d

def _env_mail():
    d = {}
    try:
        for l in open(os.path.join(HERE, '.env'), encoding='utf-8'):
            l = l.strip()
            if l and not l.startswith('#') and '=' in l:
                k, v = l.split('=', 1); d[k.strip()] = v.strip().strip('\'"')
    except Exception: pass
    return d.get('GMAIL_ADDRESS'), d.get('GMAIL_APP_PASSWORD', '').replace(' ', '')

def env_complet():
    a, m = _env_mail(); return bool(a and m)

def config():
    c = _load(CONFIG, {}); adr, mdp = _env_mail()
    if adr and mdp:
        c = {'depuis': dt.date.today().isoformat(), 'actif': True, **c, 'adresse': adr}
    return c
def index(): return _load(INDEX, {'messages': {}, 'fichiers': {}})

def save(p, d):
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def set_password(adresse, mdp):
    subprocess.run(['security', 'add-generic-password', '-U', '-s', SERVICE, '-a', adresse, '-w', mdp], capture_output=True, check=True)

def get_password(adresse):
    adr, mdp = _env_mail()
    if adr and mdp and adr.lower() == (adresse or '').lower(): return mdp
    r = subprocess.run(['security', 'find-generic-password', '-s', SERVICE, '-a', adresse, '-w'], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None

def _dec(v):
    try: return str(make_header(decode_header(v or '')))
    except Exception: return v or ''

def _safe(s, n=60):
    s = re.sub(r'[\\/:*?"<>|\r\n\t]+', ' ', s).strip().strip('.')
    return (s[:n].rstrip() or 'sans objet')

def tester(adresse, mdp):
    m = imaplib.IMAP4_SSL('imap.gmail.com', 993, timeout=30)
    try: m.login(adresse, mdp)
    finally:
        try: m.logout()
        except Exception: pass

def importer(max_messages=200):
    """Relève les nouveaux mails avec pièces jointes. Renvoie un résumé."""
    cfg = config()
    if not cfg.get('actif'): return {'ok': False, 'msg': 'Import non activé'}
    adresse = cfg['adresse']; mdp = get_password(adresse)
    if not mdp: return {'ok': False, 'msg': 'Mot de passe introuvable dans le trousseau'}
    idx = index(); depuis = dt.date.fromisoformat(cfg.get('depuis', dt.date.today().isoformat()))
    m = imaplib.IMAP4_SSL('imap.gmail.com', 993, timeout=60); n_mail = n_fic = 0
    try:
        m.login(adresse, mdp)
        m.select('INBOX', readonly=True)
        recent = max(depuis, dt.date.today() - dt.timedelta(days=3))   # les mails plus anciens sont déjà relevés : on ne relit que les 3 derniers jours
        typ, data = m.uid('search', None, f'(SINCE {recent.strftime("%d-%b-%Y")})')
        uids = data[0].split() if data and data[0] else []
        for uid in uids[-max_messages:]:
            typ, hd = m.uid('fetch', uid, '(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID FROM)])')
            raw_h = hd[0][1] if hd and hd[0] and isinstance(hd[0], tuple) else b''
            h = email.message_from_bytes(raw_h)
            mid = (h.get('Message-ID') or f'uid-{uid.decode()}').strip()
            if mid in idx['messages']: continue
            if parseaddr(h.get('From', ''))[1].lower() == adresse.lower():
                idx['messages'][mid] = {'ignore': 'envoyé par le compte'}; continue
            typ, md = m.uid('fetch', uid, '(BODY.PEEK[])')
            msg = email.message_from_bytes(md[0][1])
            nom, addr = parseaddr(msg.get('From', '')); nom = _dec(nom) or addr
            sujet = _dec(msg.get('Subject', ''))
            try: date = parsedate_to_datetime(msg.get('Date')).date()
            except Exception: date = dt.date.today()
            saved = []
            for part in msg.walk():
                fn = part.get_filename()
                if not fn or part.get_content_maintype() == 'multipart': continue
                fn = _safe(_dec(fn), 120); ext = os.path.splitext(fn)[1].lower()
                payload = part.get_payload(decode=True) or b''
                if ext in IMG_EXT and len(payload) < 60_000: continue
                if ext not in DOC_EXT | IMG_EXT: continue
                folder = os.path.join(DEST, f'{date.isoformat()} — {_safe(nom, 40)} — {_safe(sujet, 70)}')
                os.makedirs(folder, exist_ok=True)
                path = os.path.join(folder, fn); b, e = os.path.splitext(fn); i = 2
                while os.path.exists(path): path = os.path.join(folder, f'{b} ({i}){e}'); i += 1
                open(path, 'wb').write(payload); saved.append(path)
                idx['fichiers'][path] = {'de': nom, 'adresse': addr, 'objet': sujet, 'date': date.isoformat(), 'mid': mid}
            idx['messages'][mid] = {'de': addr, 'objet': sujet, 'date': date.isoformat(), 'fichiers': len(saved)}
            if saved: n_mail += 1; n_fic += len(saved)
        save(INDEX, idx)
    finally:
        try: m.logout()
        except Exception: pass
    cfg['dernier'] = dt.datetime.now().strftime('%d/%m/%Y à %H:%M'); cfg['dernier_resultat'] = f'{n_fic} pièce(s) de {n_mail} mail(s)'; cfg.pop('erreur', None)
    save(CONFIG, cfg)
    return {'ok': True, 'mails': n_mail, 'fichiers': n_fic}


# ---------------------------------------------------------------- Brouillons (15/10/2026)
from email.message import EmailMessage
import mimetypes, time as _time

SIGNATURE_TXT = ("BILE SÉVERIN\nGérant — LA MAISON DE LA CONFORMITÉ SARL\nDiagnostic, mise en conformité et défense en contrôle — Fiscal · Social\n"
                 "Tél. +225 07 19 31 49 04 · lamaisondelaconformite@gmail.com\nwww.lamaisondelaconformitesarl.net")

def _dossier_brouillons(m):
    """Le dossier des brouillons Gmail, repéré par son attribut \\Drafts (le nom dépend de la langue du compte)."""
    typ, data = m.list()
    for raw in data or []:
        line = raw.decode('utf-8', 'ignore')
        if '\\Drafts' in line:
            return line.split(' "/" ')[-1].strip()
    return '"[Gmail]/Drafts"'

def creer_brouillon(destinataires, objet, message, fichiers, copies=None):
    """Dépose un BROUILLON dans Gmail (jamais d'envoi). Renvoie la taille des pièces en Mo."""
    cfg = config(); adresse = cfg.get('adresse'); mdp = get_password(adresse) if adresse else None
    if not mdp: raise RuntimeError("La connexion à Gmail n'est pas activée : utilisez « 📨 Mails reçus » pour la configurer.")
    total = sum(os.path.getsize(f) for f in fichiers)
    if total > 24 * 1024 * 1024: raise RuntimeError(f'Les pièces font {total/1048576:.1f} Mo : Gmail limite un mail à 25 Mo. Préparez plutôt un dossier d\'envoi.')
    msg = EmailMessage(); msg['From'] = adresse; msg['Subject'] = objet
    if destinataires: msg['To'] = ', '.join(destinataires)
    if copies: msg['Cc'] = ', '.join(copies)
    msg.set_content(message.rstrip() + '\n\n' + SIGNATURE_TXT)
    for f in fichiers:
        ctype = mimetypes.guess_type(f)[0] or 'application/octet-stream'; mt, st = ctype.split('/', 1)
        msg.add_attachment(open(f, 'rb').read(), maintype=mt, subtype=st, filename=os.path.basename(f))
    m = imaplib.IMAP4_SSL('imap.gmail.com', 993, timeout=120)
    try:
        m.login(adresse, mdp)
        r = m.append(_dossier_brouillons(m), '(\\Draft)', imaplib.Time2Internaldate(_time.time()), msg.as_bytes())
        if r[0] != 'OK': raise RuntimeError(f'Gmail a refusé le brouillon : {r}')
    finally:
        try: m.logout()
        except Exception: pass
    return round(total / 1048576, 1)


# ---------------------------------------------------------------- Envoi direct, déclenché par le gérant (15/10/2026)
import smtplib, ssl

def _construire(adresse, destinataires, objet, message, fichiers, copies=None):
    msg = EmailMessage(); msg['From'] = adresse; msg['Subject'] = objet
    if destinataires: msg['To'] = ', '.join(destinataires)
    if copies: msg['Cc'] = ', '.join(copies)
    msg.set_content(message.rstrip() + '\n\n' + SIGNATURE_TXT)
    for f in fichiers:
        ctype = mimetypes.guess_type(f)[0] or 'application/octet-stream'; mt, st = ctype.split('/', 1)
        msg.add_attachment(open(f, 'rb').read(), maintype=mt, subtype=st, filename=os.path.basename(f))
    return msg

def envoyer(destinataires, objet, message, fichiers, copies=None):
    """Envoie le mail par le serveur SMTP de Gmail (copie automatique dans « Messages envoyés »). Appelé uniquement quand le
    gérant clique sur « Envoyer maintenant » et confirme dans la plateforme."""
    cfg = config(); adresse = cfg.get('adresse'); mdp = get_password(adresse) if adresse else None
    if not mdp: raise RuntimeError("La connexion à Gmail n'est pas activée : utilisez « 📨 Mails reçus » pour la configurer.")
    if not destinataires: raise RuntimeError('Indiquez au moins un destinataire.')
    total = sum(os.path.getsize(f) for f in fichiers)
    if total > 24 * 1024 * 1024: raise RuntimeError(f'Les pièces font {total/1048576:.1f} Mo : Gmail limite un mail à 25 Mo.')
    msg = _construire(adresse, destinataires, objet, message, fichiers, copies)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context(), timeout=120) as s:
        s.login(adresse, mdp); s.send_message(msg)
    return round(total / 1048576, 1)
