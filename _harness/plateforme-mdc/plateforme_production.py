"""Plateforme privée de production MDC (14/10/2026) — http://localhost:8765, consultable uniquement depuis le Mac du gérant.

- Écoute sur 127.0.0.1 seulement : aucun accès depuis un autre ordinateur ni depuis internet. Rien n'est publié.
- Les requêtes portent un jeton secret propre à chaque démarrage, et l'en-tête Host est contrôlé (protection contre les sites
  qui tenteraient d'appeler la plateforme depuis le navigateur).
- Les documents ne sont jamais déplacés : la plateforme lit DOSSIER CLIENTS et SUPERVISEUR GENERAL, ouvre les fichiers avec
  l'application du Mac, et enregistre les validations dans etat_validation.json (même état que production_par_jour.py).
- Mise à jour continue : l'index est relu à chaque affichage (au plus toutes les 60 secondes) ; les raccourcis de
  PRODUCTION_PAR_JOUR sont régénérés toutes les 15 minutes.
Lancement manuel : /usr/bin/python3 plateforme_production.py"""
import os, sys, re, json, time, secrets, threading, subprocess, shutil, html as _h, datetime as dt
from urllib.parse import urlparse, parse_qs, quote, unquote
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import production_par_jour as ppj
import mail_import
import r2_cloud
import edition_word

PORT = 8765
# Relais sur le serveur (03/11/2026) : la même plateforme tourne aussi sur le serveur, sur une copie des documents,
# et prend le relais quand le Mac est fermé ou hors ligne. Elle n'écoute que nginx (127.0.0.1:18766).
SERVEUR = os.environ.get('MDC_SERVEUR') == '1'
TOKEN = secrets.token_urlsafe(24)
try:   # jeton lisible par le serveur MCP local (fichier privé, renouvelé à chaque démarrage)
    _tp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.token'); open(_tp, 'w').write(TOKEN); os.chmod(_tp, 0o600)
except Exception: pass
ALLOWED_HOSTS = {f'127.0.0.1:{PORT}', f'localhost:{PORT}'}
import ipaddress, hashlib, hmac, gzip as _gzip
ACCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'acces.json')
SESSIONS = {}          # jeton de session -> (expiration, adresse du visiteur)
ECHECS = {}            # adresse réelle du visiteur -> (nombre d'échecs, heure du dernier échec)
SESSION_DUREE = 3 * 3600
LOCAL_ONLY = ('/api/r2', '/api/mail', '/api/ouvrir', '/api/finder', '/api/deplacer', '/api/livrables-dossier', '/api/export', '/api/acces')

def lan_ips():
    if SERVEUR: return []
    out = []
    for i in ('en0', 'en1', 'en2'):
        r = subprocess.run(['ipconfig', 'getifaddr', i], capture_output=True, text=True)
        if r.stdout.strip(): out.append(r.stdout.strip())
    return out

def hostname_local():
    if SERVEUR: return ''
    r = subprocess.run(['scutil', '--get', 'LocalHostName'], capture_output=True, text=True)
    return (r.stdout.strip() + '.local') if r.stdout.strip() else ''

def acces():
    try: return json.load(open(ACCES, encoding='utf-8'))
    except Exception: return {}

def hash_mdp(mdp, sel=None):
    sel = sel or secrets.token_hex(16)
    return sel, hashlib.pbkdf2_hmac('sha256', mdp.encode('utf-8'), bytes.fromhex(sel), 300000).hex()

def verifier_mdp(mdp):
    a = acces()
    if not a.get('hash'): return False
    return hmac.compare_digest(hash_mdp(mdp, a['sel'])[1], a['hash'])

HN = hostname_local()
# Adresses de ce Mac : une requête qui en provient a traversé le tunnel, pas le Wi-Fi.
IPS_LOCALES = set(lan_ips()) | {'127.0.0.1', '::1'}

LOGIN_HTML = '''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Production MDC</title>
<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#1a1a2e;font:16px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
form{background:#fff;border-radius:14px;padding:28px 24px;width:min(360px,90vw);box-shadow:0 10px 40px rgba(0,0,0,.4)}h1{font-size:18px;margin:0 0 4px;color:#1a1a2e}p{color:#6b6b80;font-size:13px;margin:0 0 18px}
input{width:100%;box-sizing:border-box;padding:12px;border:1px solid #d0d0d8;border-radius:8px;font-size:16px;margin-bottom:12px}button{width:100%;padding:12px;border:0;border-radius:8px;background:#c99a2e;color:#1a1a2e;font-weight:700;font-size:16px}
.err{color:#b00020;font-size:13px;margin-bottom:10px}</style></head><body><form method="post" action="/login"><h1>LA MAISON DE LA CONFORMITÉ</h1><p>Plateforme privée de production — réseau local</p>
__ERR__<input type="password" name="mdp" placeholder="Mot de passe" autocomplete="current-password" autofocus required><button>Se connecter</button></form></body></html>'''
LOCK = threading.RLock()   # verrou réentrant : un traitement qui le détient peut relire l index sans se bloquer
CACHE = {'t': 0, 'docs': None}
HERE = os.path.dirname(os.path.abspath(__file__))
LIV = ppj.SG + 'MES_LIVRABLES/'

def _safe(name):
    return ''.join(c for c in name if c not in '/:').strip() or 'SANS_NOM'

MOD = ppj.SG + 'MES_MODELES/'

def modele(k, on):
    """Coché : copie du document dans MES_MODELES/<catégorie>/, avec une fiche d'origine (expéditeur, objet, date) si le document
    a été reçu par mail. Décoché : la copie est rangée dans MES_MODELES/_RETIRES/ (jamais supprimée)."""
    docs = index(); g = docs.get(k)
    if not g: return False
    stamp = dt.datetime.now().strftime('%Y-%m-%d_%H%M')
    with LOCK:
        st = ppj.load_state(); e = st.get(k, {}); cat = ppj.effective_cat(k, g, st)
        for c in e.get('modele', {}).get('copies', []):
            if os.path.exists(c):
                dest = MOD + '_RETIRES/'; os.makedirs(dest, exist_ok=True); b, x = os.path.splitext(os.path.basename(c))
                shutil.move(c, dest + f'{b}_{stamp}{x}')
        if on:
            dest = MOD + _safe(cat) + '/'; os.makedirs(dest, exist_ok=True); copies = []
            for p in sorted(g['files']):
                t = dest + os.path.basename(p)
                if os.path.exists(t):
                    b, x = os.path.splitext(os.path.basename(p)); t = dest + f'{b}_{stamp}{x}'
                shutil.copy2(p, t); copies.append(t)
            mi = mail_import.index().get('fichiers', {}); m = next((mi[p] for p in g['files'] if p in mi), None)
            fiche = dest + os.path.splitext(os.path.basename(copies[0]))[0] + ' — ORIGINE.txt'
            open(fiche, 'w', encoding='utf-8').write(
                f"Modèle ajouté le {dt.date.today():%d/%m/%Y}\nDocument : {g['nom']}\nCatégorie : {cat}\nOriginal : {g['dir']}\n"
                + (f"Reçu par mail de : {m['de']} <{m['adresse']}>\nObjet : {m['objet']}\nDate : {m['date']}\n" if m else ''))
            copies.append(fiche)
            e['modele'] = {'le': dt.date.today().isoformat(), 'cat': cat, 'copies': copies}
        else:
            e.pop('modele', None)
        st[k] = e; ppj.save_state(st)
    return True

def livrable(k, on):
    """Coché : copie du document (tous ses formats) dans MES_LIVRABLES/<dossier>/. Décoché : la copie est rangée dans
    MES_LIVRABLES/_RETIRES/ (jamais supprimée). Recoché après modification : l'ancienne copie va dans _ANCIENNES_VERSIONS."""
    docs = index(); g = docs.get(k)
    if not g: return False
    stamp = dt.datetime.now().strftime('%Y-%m-%d_%H%M')
    with LOCK:
        st = ppj.load_state(); e = st.get(k, {}); old = e.get('livrable', {}).get('copies', [])
        for c in old:
            if os.path.exists(c):
                dest = LIV + ('_RETIRES/' if not on else '_ANCIENNES_VERSIONS/') + _safe(g['dossier']) + '/'
                os.makedirs(dest, exist_ok=True); b, x = os.path.splitext(os.path.basename(c))
                shutil.move(c, dest + f'{b}_{stamp}{x}')
        if on:
            dest = LIV + _safe(g['dossier']) + '/'; os.makedirs(dest, exist_ok=True); copies = []
            for p in sorted(g['files']):
                t = dest + os.path.basename(p)
                if os.path.exists(t):
                    b, x = os.path.splitext(os.path.basename(p)); t = dest + f'{b}_{stamp}{x}'
                shutil.copy2(p, t); copies.append(t)
            e['livrable'] = {'le': dt.date.today().isoformat(), 'mtime': g['mtime'], 'copies': copies}
        else:
            e.pop('livrable', None)
        st[k] = e; ppj.save_state(st)
    return True

def index(force=False):
    with LOCK:
        if force or CACHE['docs'] is None or time.time() - CACHE['t'] > 15:
            CACHE['docs'] = ppj.scan(); CACHE['t'] = time.time()
        return CACHE['docs']

ETAPES = ["Entrée : notes méthodologiques et propositions financières", "Création", "Suivi complet", "Audit", "Demandes d'explications", "Rapports", "Contrats de travail", "Autres documents"]

def etape_auto(nom, rel):
    """Étape de mission proposée d'après le nom du document, puis son emplacement (le gérant peut la changer)."""
    e = _etape_de(nom.upper().replace('-', '_').replace(' ', '_'))
    if e != ETAPES[7] or 'DOCUMENTS_RECUS_PAR_MAIL' in rel: return e
    return _etape_de(rel.upper().replace('-', '_').replace(' ', '_'))

def _etape_de(n):
    if re.search(r'METHODO|PROPOSITION|PROPALE|OFFRE|DEVIS|CONTRAT_DE_PRESTATION|LETTRE_DE_MISSION', n): return ETAPES[0]
    if re.search(r'DEMANDE_?D?_?EXPLICATION|\bDEE\b|_DEE_|DEE_', n): return ETAPES[4]
    if re.search(r'CONTRAT_DE_TRAVAIL|CONTRAT_TRAVAIL|AVENANT|ORDRE_DE_MISSION|CDD|CDI|DETACHEMENT|CERTIFICAT', n): return ETAPES[6]
    if re.search(r'CREATION|(^|_)CONSTITUTION|STATUTS|IMMATRICULATION|\bDFE\b|DFE_', n) and 'RECONSTITUTION' not in n: return ETAPES[1]
    if re.search(r'RAPPORT|SYNTHESE', n): return ETAPES[5]
    if re.search(r'AUDIT|DIAGNOSTIC|MATRICE|EXPOSITION|PROFIL_CONFORMITE|NOTATION', n): return ETAPES[3]
    if re.search(r'SUIVI|RECAPITULATIF|SOMMAIRE|FICHE|CONVENTION|A_SIGNER|NOTE_|DEBOURS|BALANCE|GRAND_LIVRE|DECLARATION', n): return ETAPES[2]
    return ETAPES[7]

PROCEDURES = ["L'arrivée du client", "Création d'entreprise", "Suivi complet", "Audit complet"]

def procedure_auto(nom, rel):
    """Procédure de l'Agence à laquelle se rattache un document de méthode (le gérant peut la changer)."""
    n = (rel + ' ' + nom).upper().replace('-', '_').replace(' ', '_')
    if re.search(r'CREATION|(^|_)CONSTITUTION|STATUTS|IMMATRICULATION', n) and not re.search(r'RECONSTITUTION', n): return PROCEDURES[1]
    if re.search(r'TRAVAUX_PRELIMINAIRES|PROFIL_ENTREPRISE|PROFIL_DE_L_ENTREPRISE|ARRIVEE|ACCUEIL|PROPOSITION|METHODO|CONTRAT_DE_PRESTATION|DEMANDE_DE_PIECES|LIVRABLES_D_ENTREE|DEMARRAGE', n): return PROCEDURES[0]
    if re.search(r'AUDIT|DIAGNOSTIC|NOTATION|INDICE_MDC|MATRICE|EXPOSITION|VISA', n): return PROCEDURES[3]
    if re.search(r'SUIVI|MENSUEL|FICHE_PROBLEMATIQUE|AVIS|NOTIFICATION|REGULARITE|STABILISER|COMPTE_RENDU|FEUILLE_DE_ROUTE|GUIDE_D_EXECUTION|ENGAGEMENTS|COLLABORATION', n): return PROCEDURES[2]
    return ''

def payload(local=True):
    docs = index(); st = ppj.load_state(); out = []; mi = mail_import.index().get('fichiers', {}); pv = ppj.premiere_vue(docs); today = dt.date.today()
    for k, g in docs.items():
        s = ppj.statut(k, g, st); e = st.get(k, {})
        out.append({'k': k, 'd': g['dossier'], 'n': g['nom'], 'j': dt.date.fromtimestamp(g['mtime']).isoformat(), 'mt': int(g['mtime']),
                    'f': sorted({os.path.splitext(p)[1][1:].lower() for p in g['files']}),
                    'e': os.path.relpath(g['dir'], ppj.DOCS) if g['dir'].startswith(ppj.DOCS) else '~/' + os.path.relpath(g['dir'], os.path.expanduser('~')),
                    's': s, 'v': e.get('valide_le'), 'o': e.get('obs', ''),
                    'c': ppj.effective_cat(k, g, st),
                    'mail': next((mi[p] for p in g['files'] if p in mi), None),
                    'pv': pv.get(k), 'm': bool(e.get('cat')),
                    'in': (not e.get('cat')) and today < dt.date.fromisoformat(pv.get(k, today.isoformat())) + dt.timedelta(days=ppj.DELAI_RANGEMENT),
                    'al': (dt.date.fromisoformat(pv.get(k, today.isoformat())) + dt.timedelta(days=ppj.DELAI_RANGEMENT)).isoformat(),
                    'env': (e.get('envois') or [None])[-1],
                    'cl': ({'le': e['cloud']['le'], 'ajour': g['mtime'] <= e['cloud'].get('mtime', 0) + 2} if e.get('cloud') else None),
                    'md': bool(e.get('modele')), 'mdl': e.get('modele', {}).get('le'),
                    'l': bool(e.get('livrable')), 'll': e.get('livrable', {}).get('le'),
                    'pr': e.get('procedure') if e.get('procedure') in PROCEDURES else '',
                    'pa': procedure_auto(g['nom'], os.path.relpath(g['dir'], ppj.DOCS) if g['dir'].startswith(ppj.DOCS) else ''),
                    'et': 'Retirés des étapes' if e.get('etape') == 'AUCUNE' else e.get('etape') if e.get('etape') in ETAPES else etape_auto(g['nom'], os.path.relpath(g['dir'], ppj.DOCS) if g['dir'].startswith(ppj.DOCS) else ''),
                    'lu': bool(e.get('livrable')) and g['mtime'] > e['livrable'].get('mtime', 0) + 2})
    return {'local': local, 'docs': out, 'etapes': ETAPES, 'procedures': PROCEDURES, 'cats': ppj.all_categories(), 'rub': ppj.rubriques(), 'maj': dt.datetime.now().strftime('%d/%m/%Y à %H:%M')}

def set_status(keys, statut, obs=None):
    docs = index()
    with LOCK:
        st = ppj.load_state()
        for k in keys:
            if k not in docs: continue
            e = st.get(k, {})
            e['statut'] = statut
            if statut == 'Validé': e.update(valide_le=dt.date.today().isoformat(), mtime_validation=docs[k]['mtime'])
            if statut == 'À valider': e.pop('valide_le', None); e.pop('mtime_validation', None)
            if obs is not None: e['obs'] = obs
            st[k] = e
        ppj.save_state(st)

VIEW_CSS = ('<style>body{font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:900px;margin:24px auto;padding:0 24px;color:#1a1a2e;background:#fff}'
            'h1,h2,h3{color:#1a1a2e}table{border-collapse:collapse;margin:12px 0;font-size:13px}td,th{border:1px solid #d0d0d8;padding:4px 7px;vertical-align:top}'
            'th{background:#1a1a2e;color:#fff}.sheet{margin:28px 0 8px;padding:6px 10px;background:#f5e5a5;font-weight:700}.note{color:#6b6b80;font-size:12px}table.xl{table-layout:fixed;width:auto;border-collapse:collapse;font-size:12.5px;background:#fff;color:#1a1a2e}table.xl td{border:1px solid #d9d9e3;padding:4px 6px;vertical-align:top;overflow-wrap:anywhere}'
            '@media (prefers-color-scheme:dark){body{background:#1b1b29;color:#ececf3}h1,h2,h3{color:#e8c547}td,th{border-color:#2c2c3e}.sheet{background:#2d2814}table.xl{background:#fff;color:#1a1a2e}}</style>')

def docx_html(path):
    """Conversion simple d'un Word en page lisible : titres, paragraphes (gras), tableaux, dans l'ordre du document."""
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = Document(path); out = []
    for el in d.element.body.iterchildren():
        tag = el.tag.split('}')[-1]
        if tag == 'p':
            p = Paragraph(el, d)
            txt = ''.join(f'<b>{_h.escape(r.text)}</b>' if r.bold else _h.escape(r.text) for r in p.runs)
            if not txt.strip() or len(p.text) > len(''.join(r.text for r in p.runs)) + 2: txt = _h.escape(p.text)
            if not txt.strip(): continue
            try: st = (p.style.name or '').lower()
            except Exception: st = ''
            if st.startswith('heading 1') or st == 'title': out.append(f'<h1>{txt}</h1>')
            elif st.startswith('heading 2'): out.append(f'<h2>{txt}</h2>')
            elif st.startswith('heading'): out.append(f'<h3>{txt}</h3>')
            elif 'list' in st: out.append(f'<ul><li>{txt}</li></ul>')
            else: out.append(f'<p>{txt}</p>')
        elif tag == 'tbl':
            t = Table(el, d); rows = []
            for i, r in enumerate(t.rows):
                seen = []; cells = []
                for c in r.cells:
                    if c._tc in seen: continue
                    seen.append(c._tc); cells.append(_h.escape(c.text).replace('\n', '<br>'))
                tg = 'th' if i == 0 else 'td'
                rows.append('<tr>' + ''.join(f'<{tg}>{x}</{tg}>' for x in cells) + '</tr>')
            out.append('<table>' + ''.join(rows) + '</table>')
    return out

def md_html(txt):
    """Lecture d'un script Markdown : titres, gras, italique, listes, citations, tableaux, séparateurs."""
    def inl(t):
        t = _h.escape(t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t); t = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'<i>\1</i>', t)
        return re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    out, lines, i = [], txt.split('\n'), 0
    while i < len(lines):
        l = lines[i].rstrip()
        if l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells): rows.append(cells)
                i += 1
            out.append('<table>' + ''.join('<tr>' + ''.join(f'<{"th" if j == 0 else "td"}>{inl(c)}</{"th" if j == 0 else "td"}>' for c in r) + '</tr>' for j, r in enumerate(rows)) + '</table>'); continue
        m = re.match(r'^(#{1,6})\s+(.*)', l)
        if m: n = min(len(m.group(1)), 3); out.append(f'<h{n}>{inl(m.group(2))}</h{n}>')
        elif re.match(r'^\s*[-*]\s+', l): out.append('<ul><li>' + inl(re.sub(r'^\s*[-*]\s+', '', l)) + '</li></ul>')
        elif re.match(r'^\s*\d+[.)]\s+', l): out.append('<ol><li>' + inl(re.sub(r'^\s*\d+[.)]\s+', '', l)) + '</li></ol>')
        elif l.startswith('>'): out.append('<blockquote style="border-left:3px solid #c99a2e;margin:8px 0;padding:4px 12px;background:#fbf3dc">' + inl(l.lstrip('> ')) + '</blockquote>')
        elif re.fullmatch(r'-{3,}|\*{3,}', l.strip()): out.append('<hr>')
        elif l.strip(): out.append('<p>' + inl(l) + '</p>')
        i += 1
    return out

PAGE_CACHE = {}   # pages déjà rendues (clé : fichier, version, numéro)
def pages_html(pdf, base):
    import fitz
    d = fitz.open(pdf); out = []
    for i, pg in enumerate(d):
        w, h = int(pg.rect.width), int(pg.rect.height)
        lz = '' if i < 2 else ' loading="lazy"'
        out.append(f'<img{lz} decoding="async" width="{w}" height="{h}" src="/page?{base}&n={i}" alt="Page {i+1}" style="width:100%;max-width:900px;height:auto;display:block;margin:0 auto 14px;box-shadow:0 1px 6px rgba(0,0,0,.25);background:#fff">')
    return d.page_count, ''.join(out)
WORD_CACHE = os.path.expanduser('~/Library/Containers/com.microsoft.Word/Data/Documents/MDC_APERCUS')
WORD_LOCK = threading.Lock()

def docx_pdf(path):
    """Aperçu fidèle d'un Word : Microsoft Word le convertit en PDF, mis en cache par version du fichier. Renvoie None si Word n'est pas disponible."""
    import hashlib
    if SERVEUR: return edition_word.pdf_libreoffice(path, os.path.expanduser('~/cache_apercus'))
    if not os.path.isdir('/Applications/Microsoft Word.app'): return None
    os.makedirs(WORD_CACHE, exist_ok=True)
    dst = os.path.join(WORD_CACHE, hashlib.sha1(path.encode('utf-8')).hexdigest()[:16] + f'_{int(os.path.getmtime(path))}.pdf')
    if os.path.exists(dst): return dst
    with WORD_LOCK:
        if os.path.exists(dst): return dst
        esc = lambda x: x.replace('\\', '\\\\').replace('"', '\\"')
        script = (f'set src to POSIX file "{esc(path)}"\n'
                  'tell application "Microsoft Word"\n'
                  '  open src with read only\n'
                  '  set d to active document\n'
                  f'  save as d file name "{esc(dst)}" file format format PDF\n'
                  '  close d saving no\n'
                  'end tell')
        try: subprocess.run(['osascript', '-e', script], capture_output=True, timeout=120)
        except Exception: return None
    return dst if os.path.exists(dst) else None


def lisible(f):
    """Vrai si la plateforme peut réellement lire le fichier (macOS peut bloquer l'accès aux données d'une autre application)."""
    try:
        with open(f, 'rb') as h: h.read(4)
        return True
    except Exception: return False


def apercu_docx(path, fichiers=()):
    """PDF à afficher pour un Word : la conversion par Word si elle est lisible, sinon le PDF du même document s'il est à jour."""
    pdf = docx_pdf(path)
    if pdf and lisible(pdf): return pdf
    for f in fichiers:
        if f.lower().endswith('.pdf') and os.path.getmtime(f) >= os.path.getmtime(path) - 600 and lisible(f): return f
    return None

def xlsx_html(path, max_rows=400, max_cols=40):
    """Affiche un classeur avec sa mise en forme : couleurs de fond, gras, couleur du texte, alignement, cellules fusionnées, largeurs."""
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    leger = os.path.getsize(path) > 4 * 1024 * 1024          # très gros classeur : affichage simple, plus rapide
    wb = load_workbook(path, read_only=leger, data_only=True); out = []
    def couleur(c):
        try:
            v = c.rgb if c is not None and c.type == 'rgb' else None
            return '#' + v[-6:] if isinstance(v, str) and len(v) >= 6 else None
        except Exception: return None
    def fmt(v, nf):
        if v is None: return ''
        if isinstance(v, (dt.datetime, dt.date)): return v.strftime('%d/%m/%Y')
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if nf and '%' in nf: return f'{v*100:,.1f} %'.replace(',', ' ').replace('.0 %', ' %')
            if isinstance(v, float) and v != int(v): return f'{v:,.2f}'.replace(',', ' ')
            return f'{int(v):,}'.replace(',', ' ')
        return str(v)
    for ws in wb.worksheets:
        out.append(f'<div class="sheet">Feuille : {_h.escape(ws.title)}</div>')
        if leger:
            out.append('<table>'); n = 0
            for row in ws.iter_rows(max_col=max_cols, values_only=True):
                if not any(v is not None for v in row): continue
                n += 1
                if n > max_rows: break
                out.append('<tr>' + ''.join(f'<td>{_h.escape(fmt(v, None))}</td>' for v in row) + '</tr>')
            out.append('</table>'); continue
        # dernière colonne et dernière ligne réellement utilisées
        maxc = maxr = 0
        for row in ws.iter_rows(max_col=max_cols, max_row=max_rows + 50):
            for c in row:
                if c.value is not None or (c.fill is not None and c.fill.fill_type == 'solid'):
                    if c.value is not None: maxc = max(maxc, c.column); maxr = max(maxr, c.row)
        if not maxc: out.append('<p class="note">Feuille vide.</p>'); continue
        fus, cache = {}, set()
        for m in ws.merged_cells.ranges:
            if m.min_col > maxc or m.min_row > maxr: continue
            fus[(m.min_row, m.min_col)] = (min(m.max_row, maxr) - m.min_row + 1, min(m.max_col, maxc) - m.min_col + 1)
            for r in range(m.min_row, m.max_row + 1):
                for cc in range(m.min_col, m.max_col + 1):
                    if (r, cc) != (m.min_row, m.min_col): cache.add((r, cc))
        cols = ''.join(f'<col style="width:{int((ws.column_dimensions[get_column_letter(i)].width or 10) * 7)}px">' for i in range(1, maxc + 1))
        out.append(f'<table class="xl"><colgroup>{cols}</colgroup>')
        for row in ws.iter_rows(min_row=1, max_row=min(maxr, max_rows), max_col=maxc):
            cells = []
            for c in row:
                if (c.row, c.column) in cache: continue
                st = []
                try:
                    if c.fill is not None and c.fill.fill_type == 'solid':
                        bg = couleur(c.fill.fgColor)
                        if bg: st.append(f'background:{bg}')
                    f = c.font
                    if f is not None:
                        if f.b: st.append('font-weight:700')
                        if f.i: st.append('font-style:italic')
                        fc = couleur(f.color)
                        if fc: st.append(f'color:{fc}')
                    al = c.alignment
                    if al is not None and al.horizontal in ('center', 'right', 'left'): st.append(f'text-align:{al.horizontal}')
                    elif isinstance(c.value, (int, float)) and not isinstance(c.value, bool): st.append('text-align:right')
                except Exception: pass
                sp = fus.get((c.row, c.column)); attr = ''
                if sp: attr = (f' rowspan="{sp[0]}"' if sp[0] > 1 else '') + (f' colspan="{sp[1]}"' if sp[1] > 1 else '')
                cells.append(f'<td{attr} style="{";".join(st)}">{_h.escape(fmt(c.value, c.number_format))}</td>')
            out.append('<tr>' + ''.join(cells) + '</tr>')
        if maxr > max_rows: out.append(f'<tr><td colspan="{maxc}" class="note">… affichage limité aux {max_rows} premières lignes : ouvrir dans Excel pour la suite.</td></tr>')
        out.append('</table>')
    wb.close()
    return out

def choisir_dossier(depart):
    """Ouvre la fenêtre macOS de choix de dossier, au premier plan. Renvoie le chemin choisi, ou None si le gérant annule."""
    depart = depart if os.path.isdir(depart) else ppj.DOCS
    script = ['-e', 'tell application "Finder"', '-e', 'activate',
              '-e', f'set f to choose folder with prompt "Où ranger ce document ?" default location (POSIX file "{depart}")',
              '-e', 'end tell', '-e', 'POSIX path of f']
    r = subprocess.run(['osascript'] + script, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None

def deplacer(k):
    """Déplace tous les formats d'un document vers le dossier choisi par le gérant. Jamais d'écrasement : si un fichier du même nom
    existe déjà dans le dossier choisi, rien n'est déplacé. Le statut, la validation, la rubrique et la date de première vue suivent le document."""
    docs = index(force=True); g = docs.get(k)
    if not g: return {'err': 'Document introuvable'}
    dest = choisir_dossier(g['dir'])
    if not dest: return {'cancel': True}
    dest = dest.rstrip('/') + '/'
    if os.path.realpath(dest) == os.path.realpath(g['dir']): return {'err': 'Le document est déjà dans ce dossier'}
    clash = [os.path.basename(p) for p in g['files'] if os.path.exists(dest + os.path.basename(p))]
    if clash: return {'err': 'Un fichier du même nom existe déjà dans ce dossier : ' + ', '.join(clash) + '. Rien n\'a été déplacé.'}
    with LOCK:
        for p in g['files']: shutil.move(p, dest + os.path.basename(p))
        newk = os.path.relpath(dest + g['nom'], ppj.DOCS)
        for nomx, basex in ppj.EXTERNES.items():
            if (dest + g['nom']).startswith(basex + '/'): newk = nomx + '/' + os.path.relpath(dest + g['nom'], basex)
        st = ppj.load_state(); e = st.pop(k, {}); e.update(range_par='gérant', range_le=dt.date.today().isoformat())
        if not e.get('cat'): e['cat'] = ppj.classify(g['nom'], k)
        st[newk] = e; ppj.save_state(st)
        try:
            pv = json.load(open(ppj.PREMIERE_VUE, encoding='utf-8'))
            if k in pv: pv[newk] = pv.pop(k)
            json.dump(pv, open(ppj.PREMIERE_VUE, 'w', encoding='utf-8'), ensure_ascii=False)
        except Exception: pass
    index(force=True)
    suivi = any(newk.startswith(r + '/') for r in ppj.ROOTS)
    return {'ok': True, 'dest': os.path.relpath(dest, ppj.DOCS) if dest.startswith(ppj.DOCS) else dest, 'suivi': suivi}

def rebuild_views():
    """Relit les dossiers (les raccourcis PRODUCTION_PAR_JOUR ne sont plus régénérés : voir production_par_jour.build)."""
    try:
        index(force=True)
    except Exception as ex:
        print('Raccourcis non régénérés :', ex, file=sys.stderr)

def loop():
    while True:
        rebuild_views(); time.sleep(900)

def r2_envoyer(keys):
    """Envoie tous les formats des documents vers R2 et le note sur chaque document. Renvoie (nb fichiers, Mo, erreurs)."""
    docs = index(); n = 0; taille = 0; erreurs = []
    for k in keys:
        g = docs.get(k)
        if not g: continue
        cles = []
        try:
            for p in sorted(g['files']):
                cle, t = r2_cloud.envoyer_fichier(p, g['dossier']); cles.append(cle); n += 1; taille += t
        except Exception as ex:
            erreurs.append(f"{g['nom']} : {ex}"); continue
        with LOCK:
            st = ppj.load_state(); e = st.get(k, {}); e['cloud'] = {'le': dt.date.today().isoformat(), 'mtime': g['mtime'], 'cles': cles}; st[k] = e; ppj.save_state(st)
    return n, round(taille / 1048576, 1), erreurs

def r2_loop():
    """Envoi automatique vers R2 des livrables (★), nouveaux ou modifiés depuis leur dernier envoi (toutes les 15 minutes, si l'option est active)."""
    while True:
        time.sleep(900)
        c = r2_cloud.config()
        if c.get('actif') and c.get('auto_valides'):
            try:
                docs = index(); st = ppj.load_state()
                todo = [k for k, g in docs.items() if st.get(k, {}).get('livrable') and (not st.get(k, {}).get('cloud') or g['mtime'] > st[k]['cloud'].get('mtime', 0) + 2)]
                if todo:
                    n, mo, err = r2_envoyer(todo); c = r2_cloud.config(); c['dernier_auto'] = f'{dt.datetime.now():%d/%m/%Y à %H:%M} — {n} fichier(s), {mo} Mo' + (f', {len(err)} erreur(s)' if err else ''); r2_cloud.save_config(c)
            except Exception as ex:
                c = r2_cloud.config(); c['erreur'] = f'{dt.datetime.now():%d/%m %H:%M} — {ex}'; r2_cloud.save_config(c)

def relais_loop():
    """Synchronisation avec le relais du serveur toutes les 5 minutes. Lancée d'ici parce que macOS n'autorise
    l'accès au dossier Documents qu'à la plateforme, pas à une tâche de fond."""
    script = os.path.expanduser('~/.mdc/relais/synchro_relais.sh')
    log = os.path.expanduser('~/.mdc/relais/synchro.log')
    time.sleep(60)
    while True:
        if os.path.exists(script):
            try:
                with open(log, 'a') as out:
                    subprocess.run(['/bin/zsh', script], stdout=out, stderr=out, timeout=3 * 3600)
            except Exception as ex:
                print('Synchronisation du relais :', ex, file=sys.stderr)
        time.sleep(300)

def mail_loop():
    """Relève des mails toutes les 2 minutes, si l'import est activé. Aucune erreur ne peut arrêter la relève."""
    while True:
        try:
            if mail_import.config().get('actif'):
                r = mail_import.importer()
                if r.get('fichiers'): index(force=True)
        except Exception as ex:
            try:
                c = mail_import.config(); c['erreur'] = f'{dt.datetime.now():%d/%m %H:%M} — {ex}'; mail_import.save(mail_import.CONFIG, c)
            except Exception: pass
        time.sleep(120)

class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        if not self.is_local():   # trace des connexions des autres appareils (diagnostic)
            print(dt.datetime.now().strftime('%d/%m %H:%M:%S'), self.client_address[0], self.command if hasattr(self, 'command') else '', self.path if hasattr(self, 'path') else '', fmt % a, flush=True)
    def is_local(self):
        if SERVEUR: return False
        return self.client_address[0] in ('127.0.0.1', '::1')
    def is_lan(self):
        try: return ipaddress.ip_address(self.client_address[0]).is_private
        except ValueError: return False
    def visiteur(self):
        # Derrière le tunnel, tout internet arrive avec l'adresse de ce Mac : nginx transmet
        # alors l'adresse réelle, qu'on n'accepte que de ce saut-là, jamais d'un autre appareil.
        src = self.client_address[0]
        if src in IPS_LOCALES:
            vu = (self.headers.get('X-Real-IP') or '').strip()
            if vu:
                try:
                    ipaddress.ip_address(vu); return vu
                except ValueError:
                    pass
        return src
    def identite_plateforme(self):
        # Requête venue du tunnel : la connexion de la plateforme (compte nominatif et code à six
        # chiffres) a déjà été contrôlée par le frontal, qui joint l'identité de la personne.
        if self.client_address[0] not in IPS_LOCALES:
            return ''
        return unquote((self.headers.get('X-MDC-Login') or '').strip())
    def ok_host(self):
        if SERVEUR: return self.client_address[0] == '127.0.0.1'   # seul nginx du serveur peut joindre le relais
        h = self.headers.get('Host', '')
        if self.is_local(): return h in ALLOWED_HOSTS
        if not self.is_lan(): return False
        name, _, port = h.rpartition(':')
        if port != str(PORT): return False
        if name and name == HN: return True
        try: return ipaddress.ip_address(name).is_private
        except ValueError: return False
    def session_ok(self):
        if self.is_local(): return True
        if self.identite_plateforme(): return True
        c = self.headers.get('Cookie', '')
        for part in c.split(';'):
            k, _, v = part.strip().partition('=')
            if k == 'mdc_session' and v in SESSIONS:
                fin, qui = SESSIONS[v]
                if fin > time.time() and qui == self.visiteur(): return True
                SESSIONS.pop(v, None)
        return False
    def send(self, code, body, ctype='application/json; charset=utf-8'):
        b = body if isinstance(body, bytes) else body.encode('utf-8')
        gz = len(b) > 2048 and ctype.startswith(('application/json', 'text/')) and 'gzip' in self.headers.get('Accept-Encoding', '')
        if gz: b = _gzip.compress(b, 5)   # la liste des documents (2 Mo) passe à quelques centaines de Ko : chargement rapide hors du bureau
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(b)))
        if gz: self.send_header('Content-Encoding', 'gzip'); self.send_header('Vary', 'Accept-Encoding')
        self.send_header('Cache-Control', 'no-store'); self.send_header('X-Frame-Options', 'SAMEORIGIN')
        if ctype != 'application/pdf': self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-src 'self'; object-src 'self'")
        self.end_headers(); self.wfile.write(b)
    def authed(self):
        return self.ok_host() and self.session_ok() and secrets.compare_digest(self.headers.get('X-MDC-Token', ''), TOKEN)
    def redirect(self, loc, cookie=None):
        self.send_response(303); self.send_header('Location', loc)
        if cookie: self.send_header('Set-Cookie', cookie)
        self.send_header('Content-Length', '0'); self.end_headers()
    def do_GET(self):
        if not self.ok_host(): return self.send(403, '{}')
        if self.path == '/robots.txt':
            return self.send(200, 'User-agent: *\nDisallow: /\n', 'text/plain; charset=utf-8')
        if self.path == '/logout':
            return self.redirect('/', 'mdc_session=; Max-Age=0; Path=/; HttpOnly; SameSite=Strict')
        if not self.session_ok():
            if self.path in ('/', '/index.html', '/login'):
                return self.send(200, LOGIN_HTML.replace('__ERR__', '' if acces().get('hash') else '<div class="err">Accès à distance non activé : définissez d\'abord le mot de passe sur le Mac.</div>'), 'text/html; charset=utf-8')
            return self.send(403, '{}')
        if self.path in ('/', '/index.html'):
            html = open(os.path.join(HERE, 'plateforme_production.html'), encoding='utf-8').read().replace('__TOKEN__', TOKEN)
            return self.send(200, html, 'text/html; charset=utf-8')
        if self.path.startswith('/qr'):
            if not self.is_local(): return self.send(403, '{}')
            q = parse_qs(urlparse(self.path).query); url = (q.get('u') or [''])[0]
            if not url.startswith('http://') or url.split('//', 1)[1].split(':')[0] not in lan_ips() + [HN]: return self.send(400, '{}')
            out = os.path.join(HERE, 'logs', 'qr.png')
            subprocess.run([os.path.join(HERE, 'qrgen'), url, out], capture_output=True)
            if not os.path.exists(out): return self.send(404, '{}')
            b = open(out, 'rb').read(); self.send_response(200); self.send_header('Content-Type', 'image/png'); self.send_header('Content-Length', str(len(b)))
            self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(b); return
        if self.path.startswith('/page'):
            q = parse_qs(urlparse(self.path).query)
            if not secrets.compare_digest((q.get('t') or [''])[0], TOKEN): return self.send(403, '{}')
            g = index().get((q.get('k') or [''])[0])
            if (q.get('ext') or [''])[0] == 'docx':
                dx = [p for p in (g['files'] if g else []) if p.lower().endswith('.docx')]
                pdfs = [x for x in [apercu_docx(dx[0], g['files']) if dx else None] if x]
            else:
                pdfs = [p for p in (g['files'] if g else []) if p.lower().endswith('.pdf')]
            if not pdfs: return self.send(404, '{}')
            try:
                import fitz
                i = int((q.get('n') or ['0'])[0]); ck = (pdfs[0], os.path.getmtime(pdfs[0]), i)
                png = PAGE_CACHE.get(ck)
                if png is None:
                    png = fitz.open(pdfs[0])[i].get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).tobytes('png')
                    if len(PAGE_CACHE) > 300: PAGE_CACHE.clear()
                    PAGE_CACHE[ck] = png
            except Exception:
                return self.send(404, '{}')
            self.send_response(200); self.send_header('Content-Type', 'image/png'); self.send_header('Content-Length', str(len(png)))
            self.send_header('Cache-Control', 'private, max-age=86400'); self.end_headers(); self.wfile.write(png); return   # l'adresse change avec la version du fichier : aucun risque de page périmée
        if self.path.startswith('/edit'):
            q = parse_qs(urlparse(self.path).query)
            if not secrets.compare_digest((q.get('t') or [''])[0], TOKEN): return self.send(403, '{}')
            k = (q.get('k') or [''])[0]; g = index().get(k)
            dx = [p for p in (g['files'] if g else []) if p.lower().endswith('.docx')]
            if not dx: return self.send(404, 'Document introuvable', 'text/plain; charset=utf-8')
            try: return self.send(200, edition_word.page_edition(dx[0], k, TOKEN), 'text/html; charset=utf-8')
            except Exception as ex: return self.send(200, '<!doctype html><meta charset="utf-8">' + VIEW_CSS + f'<p class="note">Modification impossible ({_h.escape(str(ex))}).</p>', 'text/html; charset=utf-8')
        if self.path.startswith('/voir'):
            q = parse_qs(urlparse(self.path).query)
            if not secrets.compare_digest((q.get('t') or [''])[0], TOKEN): return self.send(403, '{}')
            g_key = (q.get('k') or [''])[0]; g = index().get(g_key); ext = (q.get('ext') or [''])[0].lower()
            if not g: return self.send(404, 'Document introuvable', 'text/plain; charset=utf-8')
            files = [p for p in g['files'] if p.lower().endswith('.' + ext)] or g['files']
            f = files[0]; e = os.path.splitext(f)[1].lower()
            title = f'<title>{_h.escape(g["nom"])}</title>'
            try:
                if e == '.pdf' and (q.get('brut') or [''])[0] != '1':
                    import fitz
                    base = f'k={quote(g_key)}&t={quote(TOKEN)}&v={int(os.path.getmtime(f))}'   # v : version du fichier, pour ne jamais afficher une page périmée
                    n, imgs = pages_html(f, base)
                    css = '<style>body{margin:0;padding:16px;background:#525659;font:13px -apple-system,sans-serif;color:#ddd;text-align:center}a{color:#e8c547}</style>'
                    return self.send(200, f'<!doctype html><meta charset="utf-8">{title}{css}<p>{n} page(s) — <a href="/voir?{base}&ext=pdf&brut=1" target="_blank">ouvrir le PDF d\'origine dans un nouvel onglet</a></p>{imgs}', 'text/html; charset=utf-8')
                if e == '.pdf':
                    b = open(f, 'rb').read(); self.send_response(200)
                    self.send_header('Content-Type', 'application/pdf'); self.send_header('Content-Length', str(len(b)))
                    self.send_header('Content-Disposition', 'inline'); self.send_header('Cache-Control', 'no-store'); self.send_header('X-Frame-Options', 'SAMEORIGIN'); self.end_headers(); self.wfile.write(b); return
                if e == '.html':
                    self.send_response(200); b = open(f, 'rb').read()
                    self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(b)))
                    self.send_header('Content-Security-Policy', 'sandbox'); self.end_headers(); self.wfile.write(b); return
                if e in ('.png', '.jpg', '.jpeg'):
                    if (q.get('brut') or [''])[0] == '1':
                        b = open(f, 'rb').read(); self.send_response(200); self.send_header('Content-Type', 'image/png' if e == '.png' else 'image/jpeg')
                        self.send_header('Content-Length', str(len(b))); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(b); return
                    src = f'/voir?k={quote(g_key)}&t={quote(TOKEN)}&ext={e[1:]}&brut=1&v={int(os.path.getmtime(f))}'
                    return self.send(200, f'<!doctype html><meta charset="utf-8">{title}<style>body{{margin:0;background:#525659;text-align:center;padding:16px}}img{{max-width:100%;box-shadow:0 1px 8px rgba(0,0,0,.4)}}</style><img src="{src}">', 'text/html; charset=utf-8')
                if e in ('.md', '.txt'):
                    body = md_html(open(f, encoding='utf-8', errors='replace').read()) if e == '.md' else ['<pre style="white-space:pre-wrap">' + _h.escape(open(f, encoding='utf-8', errors='replace').read()) + '</pre>']
                    return self.send(200, '<!doctype html><meta charset="utf-8">' + title + VIEW_CSS + ''.join(body), 'text/html; charset=utf-8')
                if e == '.docx':
                    pdf = apercu_docx(f, g['files'])
                    if pdf:
                        import fitz
                        base = f'k={quote(g_key)}&t={quote(TOKEN)}&v={int(os.path.getmtime(f))}&ext=docx'
                        n, imgs = pages_html(pdf, base)
                        css = '<style>body{margin:0;padding:16px;background:#525659;font:13px -apple-system,sans-serif;color:#ddd;text-align:center}</style>'
                        return self.send(200, f'<!doctype html><meta charset="utf-8">{title}{css}<p>{n} page(s)</p>{imgs}', 'text/html; charset=utf-8')
                    body = docx_html(f)
                elif e == '.xlsx':
                    body = xlsx_html(f)
                else:
                    body = ['<p class="note">Ce format ne peut pas être affiché dans la plateforme. Utilisez « Ouvrir dans l\'application ».</p>']
                note = ''
                return self.send(200, '<!doctype html><meta charset="utf-8">' + title + VIEW_CSS + note + ''.join(body), 'text/html; charset=utf-8')
            except Exception as ex:
                return self.send(200, '<!doctype html><meta charset="utf-8">' + VIEW_CSS + f'<p class="note">Aperçu impossible ({_h.escape(str(ex))}). Utilisez « Ouvrir dans l\'application ».</p>', 'text/html; charset=utf-8')
        if self.path.startswith('/api/docs'):
            if not self.authed(): return self.send(403, '{}')
            if 'refresh=1' in self.path: index(force=True)
            return self.send(200, json.dumps(payload(self.is_local()), ensure_ascii=False))
        self.send(404, '{}')
    def do_POST(self):
        if self.path == '/login':
            if not self.ok_host(): return self.send(403, '{}')
            ip = self.visiteur(); nb, t0 = ECHECS.get(ip, (0, 0))
            if nb >= 5 and time.time() - t0 < 900:
                return self.send(429, LOGIN_HTML.replace('__ERR__', '<div class="err">Trop de tentatives : réessayez dans 15 minutes.</div>'), 'text/html; charset=utf-8')
            n = int(self.headers.get('Content-Length', 0) or 0)
            mdp = parse_qs(self.rfile.read(min(n, 4096)).decode('utf-8', 'ignore')).get('mdp', [''])[0]
            if mdp and verifier_mdp(mdp):
                ECHECS.pop(ip, None); sid = secrets.token_urlsafe(32); SESSIONS[sid] = (time.time() + SESSION_DUREE, ip)
                return self.redirect('/', f'mdc_session={sid}; Max-Age={SESSION_DUREE}; Path=/; HttpOnly; SameSite=Strict')
            ECHECS[ip] = (nb + 1, time.time())
            return self.send(401, LOGIN_HTML.replace('__ERR__', '<div class="err">Mot de passe incorrect.</div>'), 'text/html; charset=utf-8')
        if not self.authed(): return self.send(403, '{}')
        if self.path in LOCAL_ONLY and not self.is_local(): return self.send(403, '{"err":"Action réservée au Mac"}')
        n = int(self.headers.get('Content-Length', 0) or 0)
        try: data = json.loads(self.rfile.read(n) or b'{}')
        except Exception: return self.send(400, '{}')
        docs = index()
        if self.path == '/api/statut':
            s = data.get('statut')
            if s not in ppj.STATUTS[:3]: return self.send(400, '{}')
            set_status(data.get('keys', []), s, data.get('obs'))
            return self.send(200, '{"ok":true}')
        if self.path == '/api/procedure':
            pr = data.get('procedure') or ''; keys = [k for k in data.get('keys', []) if k in docs]
            if (pr and pr not in PROCEDURES) or not keys: return self.send(400, '{}')
            with LOCK:
                st = ppj.load_state()
                for k in keys:
                    e = st.get(k, {})
                    if pr: e['procedure'] = pr
                    else: e.pop('procedure', None)
                    st[k] = e
                ppj.save_state(st)
            return self.send(200, '{"ok":true}')
        if self.path == '/api/etape':
            et = data.get('etape'); keys = [k for k in data.get('keys', []) if k in docs]
            if et == '': et = 'AUCUNE'
            if (et not in ETAPES and et != 'AUCUNE') or not keys: return self.send(400, '{}')
            with LOCK:
                st = ppj.load_state()
                for k in keys:
                    e = st.get(k, {}); e['etape'] = et; st[k] = e
                ppj.save_state(st)
            return self.send(200, '{"ok":true}')
        if self.path == '/api/categorie':
            k, cat = data.get('k'), data.get('cat')
            keys = data.get('keys') or [k]
            if cat not in ppj.all_categories() or not all(x in docs for x in keys): return self.send(400, '{}')
            with LOCK:
                st = ppj.load_state()
                for x in keys:
                    e = st.get(x, {}); e.update(cat=cat, range_par='gérant', range_le=dt.date.today().isoformat()); st[x] = e
                ppj.save_state(st)
            return self.send(200, '{"ok":true}')
        if self.path == '/api/acces':
            if data.get('mdp') is not None:
                mdp = data.get('mdp') or ''
                if len(mdp) < 8: return self.send(400, '{"err":"8 caractères au minimum"}')
                sel, h = hash_mdp(mdp); json.dump({'sel': sel, 'hash': h, 'le': dt.date.today().isoformat()}, open(ACCES, 'w')); os.chmod(ACCES, 0o600)
                SESSIONS.clear()
            a = acces(); ips = lan_ips(); hn = hostname_local()
            return self.send(200, json.dumps({'actif': bool(a.get('hash')), 'le': a.get('le'), 'urls': [f'http://{i}:{PORT}' for i in ips] + ([f'http://{hn}:{PORT}'] if hn else []), 'sessions': sum(1 for v in SESSIONS.values() if v[0] > time.time())}, ensure_ascii=False))
        if self.path == '/api/mail':
            act = data.get('action')
            if act == 'configurer':
                adr = (data.get('adresse') or '').strip(); mdp = (data.get('mdp') or '').replace(' ', ''); dep = data.get('depuis') or dt.date.today().isoformat()
                if not adr or not mdp: return self.send(400, json.dumps({'err': 'Adresse et mot de passe d\'application obligatoires'}, ensure_ascii=False))
                try: mail_import.tester(adr, mdp)
                except Exception as ex: return self.send(400, json.dumps({'err': f'Connexion refusée par Gmail : {ex}'}, ensure_ascii=False))
                mail_import.set_password(adr, mdp)
                c = mail_import.config(); c.update(adresse=adr, depuis=dep, actif=True); mail_import.save(mail_import.CONFIG, c)
                threading.Thread(target=lambda: (mail_import.importer(), index(force=True)), daemon=True).start()
            elif act == 'importer':
                try: r = mail_import.importer(); index(force=True)
                except Exception as ex: return self.send(400, json.dumps({'err': str(ex)}, ensure_ascii=False))
            elif act == 'pause':
                c = mail_import.config(); c['actif'] = not c.get('actif'); mail_import.save(mail_import.CONFIG, c)
            c = mail_import.config(); ix = mail_import.index()
            return self.send(200, json.dumps({'adresse': c.get('adresse'), 'actif': bool(c.get('actif')), 'depuis': c.get('depuis'), 'dernier': c.get('dernier'),
                'env': mail_import.env_complet(), 'resultat': c.get('dernier_resultat'), 'erreur': c.get('erreur'), 'nb': len(ix.get('fichiers', {})), 'mdp': bool(c.get('adresse') and mail_import.get_password(c['adresse']))}, ensure_ascii=False))
        if self.path == '/api/deplacer':
            return self.send(200, json.dumps(deplacer(data.get('k')), ensure_ascii=False))
        if self.path == '/api/rubrique':
            act = data.get('action'); nom = (data.get('nom') or '').strip()[:80]; nouveau = (data.get('nouveau') or '').strip()[:80]
            with LOCK:
                r = ppj.rubriques(); st = ppj.load_state()
                if act == 'creer':
                    if not nom or nom in ppj.all_categories(): return self.send(400, '{"err":"Nom vide ou déjà utilisé"}')
                    r.append(nom)
                    if data.get('k') in docs:
                        e = st.get(data['k'], {}); e.update(cat=nom, range_par='gérant', range_le=dt.date.today().isoformat()); st[data['k']] = e
                elif act == 'renommer':
                    if nom not in r or not nouveau or nouveau in ppj.all_categories(): return self.send(400, '{"err":"Renommage impossible"}')
                    r[r.index(nom)] = nouveau
                    for e in st.values():
                        if e.get('cat') == nom: e['cat'] = nouveau
                elif act == 'supprimer':
                    if nom not in r: return self.send(400, '{}')
                    r.remove(nom)
                    for e in st.values():
                        if e.get('cat') == nom: e.pop('cat', None); e.pop('range_par', None)
                else:
                    return self.send(400, '{}')
                ppj.save_rubriques(r); ppj.save_state(st)
            return self.send(200, '{"ok":true}')
        if self.path == '/api/livrable':
            ok = livrable(data.get('k'), bool(data.get('on')))
            return self.send(200 if ok else 404, '{"ok":true}' if ok else '{}')
        if self.path == '/api/r2':
            act = data.get('action'); c = r2_cloud.config()
            if act == 'configurer':
                acc = (data.get('account') or '').strip(); bk = (data.get('bucket') or '').strip(); kid = (data.get('keyid') or '').strip(); sec = (data.get('secret') or '').strip()
                if not (acc and bk and kid and sec): return self.send(400, json.dumps({'err': 'Les quatre champs sont obligatoires'}, ensure_ascii=False))
                try: r2_cloud.tester(acc, bk, kid, sec)
                except Exception as ex: return self.send(400, json.dumps({'err': str(ex)}, ensure_ascii=False))
                r2_cloud.set_keys(acc, kid, sec)
                c.update(account=acc, bucket=bk, prefixe=(data.get('prefixe') or 'MDC').strip().strip('/'), actif=True); c.pop('erreur', None); r2_cloud.save_config(c)
            elif act == 'auto':
                c['auto_valides'] = not c.get('auto_valides'); r2_cloud.save_config(c)
            elif act == 'pause':
                c['actif'] = not c.get('actif'); r2_cloud.save_config(c)
            c = r2_cloud.config(); st = ppj.load_state()
            return self.send(200, json.dumps({'account': c.get('account'), 'bucket': c.get('bucket'), 'prefixe': c.get('prefixe'), 'actif': bool(c.get('actif')),
                'auto': bool(c.get('auto_valides')), 'env': r2_cloud.env_complet(), 'dernier_auto': c.get('dernier_auto'), 'erreur': c.get('erreur'),
                'nb': sum(1 for e in st.values() if e.get('cloud'))}, ensure_ascii=False))
        if self.path == '/api/r2-envoi':
            if not r2_cloud.config().get('actif'): return self.send(400, json.dumps({'err': "Le mode cloud n'est pas activé : ouvrez « ☁️ Cloud R2 » sur le Mac."}, ensure_ascii=False))
            st0 = ppj.load_state(); cles = [k for k in data.get('keys', []) if k in docs and st0.get(k, {}).get('livrable')]
            ignores = len([k for k in data.get('keys', []) if k in docs]) - len(cles)
            if not cles: return self.send(400, json.dumps({'err': "Seuls les livrables (★) partent vers le cloud : cochez d'abord « bon » sur les documents à transmettre."}, ensure_ascii=False))
            n, mo, err = r2_envoyer(cles)
            if ignores: err = list(err) + [f'{ignores} document(s) non envoyé(s) : ce ne sont pas des livrables']
            return self.send(200 if not err or n else 400, json.dumps({'n': n, 'mo': mo, 'erreurs': err, 'err': '; '.join(err[:3]) if err and not n else None}, ensure_ascii=False))
        if self.path == '/api/carnet':
            try: carnet = json.load(open(os.path.join(HERE, 'carnet.json'), encoding='utf-8'))
            except Exception: carnet = []
            return self.send(200, json.dumps(carnet, ensure_ascii=False))
        if self.path == '/api/envoi':
            keys = [k for k in data.get('keys', []) if k in docs]
            if not keys: return self.send(400, json.dumps({'err': 'Aucun document sélectionné'}, ensure_ascii=False))
            pref = data.get('pref', 'pdf'); mode = data.get('mode'); objet = (data.get('objet') or '').strip()[:200] or 'Transmission de documents'
            dest_list = [a.strip() for a in re.split(r'[,;\s]+', data.get('a') or '') if a.strip()]
            cc_list = [a.strip() for a in re.split(r'[,;\s]+', data.get('cc') or '') if a.strip()]
            if any(not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', a) for a in dest_list + cc_list): return self.send(400, json.dumps({'err': 'Adresse e-mail invalide'}, ensure_ascii=False))
            fichiers = []; prefs = data.get('prefs') or {}
            for k in keys:
                fs = sorted(docs[k]['files']); choix = prefs.get(k) or pref
                pdf = [f for f in fs if f.lower().endswith('.pdf')][:1]
                word = [f for f in fs if f.lower().endswith('.docx')][:1]
                if choix == 'pdf': fichiers += pdf or fs[:1]
                elif choix == 'word': fichiers += word or pdf or fs[:1]
                elif choix == 'pdf_word': fichiers += (pdf + word) or fs[:1]
                else: fichiers += fs
            if mode == 'gmail':
                try: mo = mail_import.creer_brouillon(dest_list, objet, data.get('message') or '', fichiers, cc_list)
                except Exception as ex: return self.send(400, json.dumps({'err': str(ex)}, ensure_ascii=False))
                res = {'ok': True, 'mode': 'gmail', 'n': len(fichiers), 'mo': mo}
            elif mode == 'envoyer':
                if not data.get('confirme'): return self.send(400, json.dumps({'err': 'Envoi non confirmé'}, ensure_ascii=False))
                try: mo = mail_import.envoyer(dest_list, objet, data.get('message') or '', fichiers, cc_list)
                except Exception as ex: return self.send(400, json.dumps({'err': str(ex)}, ensure_ascii=False))
                res = {'ok': True, 'mode': 'envoyer', 'n': len(fichiers), 'mo': mo}
            elif mode == 'dossier':
                if not self.is_local(): return self.send(403, json.dumps({'err': 'Réservé au Mac'}, ensure_ascii=False))
                base = ppj.DOCS + 'ENVOIS_PREPARES/' + f'{dt.date.today().isoformat()} — {_safe(objet)[:70]}'; d = base; i = 2
                while os.path.exists(d): d = f'{base} ({i})'; i += 1
                os.makedirs(d)
                for f in fichiers: shutil.copy2(f, os.path.join(d, os.path.basename(f)))
                open(os.path.join(d, '00_BORDEREAU.txt'), 'w', encoding='utf-8').write(
                    f"Objet : {objet}\nDestinataire(s) : {', '.join(dest_list) or '—'}\nCopie : {', '.join(cc_list) or '—'}\nPréparé le {dt.datetime.now():%d/%m/%Y à %H:%M}\n\n"
                    + (data.get('message') or '') + '\n\nDocuments :\n' + '\n'.join(f'- {os.path.basename(f)}' for f in fichiers))
                z = shutil.make_archive(d, 'zip', d); subprocess.Popen(['open', '-R', z])
                res = {'ok': True, 'mode': 'dossier', 'n': len(fichiers), 'dossier': os.path.relpath(d, ppj.DOCS)}
            else:
                return self.send(400, '{}')
            try:   # le carnet d'adresses apprend les destinataires utilisés, rattachés aux dossiers des documents envoyés
                cp = os.path.join(HERE, 'carnet.json'); carnet = json.load(open(cp, encoding='utf-8')) if os.path.exists(cp) else []
                parad = {e['email']: e for e in carnet}; dos = sorted({docs[k]['dossier'] for k in keys})
                for a in dest_list + cc_list:
                    a = a.lower(); e = parad.get(a)
                    if not e:
                        loc = a.split('@')[0]; parts = [x for x in re.split(r'[._-]+', loc) if x and not x.isdigit()]
                        e = {'email': a, 'nom': (parts[0].upper() + ' ' + ' '.join(x.capitalize() for x in parts[1:])) if len(parts) > 1 else loc, 'type': 'contact', 'dossiers': [], 'n': 0, 'dernier': ''}
                        carnet.append(e); parad[a] = e
                    e['n'] = e.get('n', 0) + 1; e['dernier'] = dt.date.today().isoformat(); e['dossiers'] = sorted(set(e.get('dossiers', [])) | set(dos))
                json.dump(sorted(carnet, key=lambda e: -e.get('n', 0)), open(cp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            except Exception: pass
            with LOCK:
                st = ppj.load_state()
                for k in keys:
                    e = st.get(k, {}); e.setdefault('envois', []).append({'le': dt.date.today().isoformat(), 'mode': mode, 'objet': objet, 'a': ', '.join(dest_list)}); st[k] = e
                ppj.save_state(st)
            return self.send(200, json.dumps(res, ensure_ascii=False))
        if self.path == '/api/modele':
            ok = modele(data.get('k'), bool(data.get('on')))
            return self.send(200 if ok else 404, '{"ok":true}' if ok else '{}')
        if self.path == '/api/modeles-dossier':
            if not self.is_local(): return self.send(403, '{}')
            subprocess.Popen(['open', MOD if os.path.isdir(MOD) else ppj.SG])
            return self.send(200, '{"ok":true}')
        if self.path == '/api/livrables-dossier':
            subprocess.Popen(['open', LIV if os.path.isdir(LIV) else ppj.SG])
            return self.send(200, '{"ok":true}')
        if self.path == '/api/docx-modifier':
            g = docs.get(data.get('k'))
            dx = [p for p in (g['files'] if g else []) if p.lower().endswith('.docx')]
            if not dx or not isinstance(data.get('blocs'), dict): return self.send(404, '{}')
            try: ok, msg = edition_word.enregistrer(dx[0], data['blocs'], data.get('v') or 0, data.get('ajouts') or [], data.get('suppr') or [])
            except Exception as ex: ok, msg = False, f'Enregistrement impossible ({ex})'
            if not ok: return self.send(200, json.dumps({'ok': False, 'err': msg}, ensure_ascii=False))
            okp, mp = edition_word.synchroniser_pdf(dx[0])
            threading.Thread(target=index, kwargs={'force': True}, daemon=True).start()
            return self.send(200, json.dumps({'ok': True, 'msg': msg, 'pdf': okp, 'msg_pdf': mp, 'v': int(os.path.getmtime(dx[0]))}, ensure_ascii=False))
        if self.path in ('/api/ouvrir', '/api/finder'):
            k = data.get('k'); g = docs.get(k)
            if not g: return self.send(404, '{}')
            if self.path == '/api/finder':
                subprocess.Popen(['open', '-R', sorted(g['files'])[0]])
            else:
                ext = (data.get('ext') or '').lower()
                files = [p for p in g['files'] if p.lower().endswith('.' + ext)] or g['files']
                subprocess.Popen(['open', files[0]])
            return self.send(200, '{"ok":true}')
        if self.path == '/api/actualiser':
            threading.Thread(target=rebuild_views, daemon=True).start()
            return self.send(200, '{"ok":true}')
        if self.path == '/api/export':
            with LOCK:
                st = ppj.load_state(); ppj.build(index(force=True), st, journal=True); ppj.save_state(st)
            subprocess.Popen(['open', ppj.JOURNAL])
            return self.send(200, '{"ok":true}')
        self.send(404, '{}')

if __name__ == '__main__' and SERVEUR:
    # Relais : ni relève des mails, ni envoi vers R2, ni surveillance des Word (le Mac s'en charge).
    srv = ThreadingHTTPServer(('127.0.0.1', 18766), H)
    print('Relais de la plateforme MDC sur 127.0.0.1:18766', flush=True)
    srv.serve_forever()
if __name__ == '__main__':
    threading.Thread(target=loop, daemon=True).start()
    threading.Thread(target=mail_loop, daemon=True).start()
    threading.Thread(target=relais_loop, daemon=True).start()
    threading.Thread(target=r2_loop, daemon=True).start()
    threading.Thread(target=edition_word.surveiller, args=(lambda: [p for g in index().values() for p in g['files'] if p.lower().endswith('.docx')],), daemon=True).start()
    srv = ThreadingHTTPServer(('0.0.0.0', PORT), H)   # le Mac et les appareils du réseau Wi-Fi local seulement (adresses privées)
    print(f'Plateforme MDC : http://localhost:{PORT}', flush=True)
    srv.serve_forever()
