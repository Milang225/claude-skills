"""Classement des documents produits PAR JOUR DE PRODUCTION, et validation par le gérant (14/10/2026).

Usage :
  python3 production_par_jour.py                 -> met à jour le classement (raccourcis)
  python3 production_par_jour.py export          -> écrit aussi le journal Excel 00_JOURNAL_DE_PRODUCTION.xlsx
  python3 production_par_jour.py valider MOTIF    -> valide les documents dont le chemin contient MOTIF (fichier ou dossier)
  python3 production_par_jour.py corriger MOTIF "observation"  -> marque « À corriger »
  python3 production_par_jour.py statut MOTIF     -> affiche le statut des documents correspondants

Principes :
- Les documents ne sont jamais déplacés ni copiés : PRODUCTION_PAR_JOUR ne contient que des RACCOURCIS (liens) vers les originaux.
  Les raccourcis sont régénérés à chaque passage ; les originaux ne sont jamais touchés.
- Jour de production = date de dernière modification du fichier.
- Un document validé porte « ✅ » devant son nom, et figure aussi dans PRODUCTION_PAR_JOUR/_VALIDES/<dossier>/.
- Un document modifié après sa validation passe au statut « Modifié après validation » (à revalider).
- Le gérant peut aussi changer la colonne Statut dans 00_JOURNAL_DE_PRODUCTION.xlsx : le choix est repris au passage suivant.
Périmètre : DOSSIER CLIENTS et SUPERVISEUR GENERAL ; pdf, docx, xlsx, pptx, html ; hors _OBSOLETE, _SOURCES, TRANSMISSION_ (copies),
pièces reçues, fichiers temporaires."""
import os, sys, json, datetime as dt
from collections import defaultdict
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.hyperlink import Hyperlink

DOCS = '/Users/bilefilsseverin/Documents/'
SG = DOCS + 'SUPERVISEUR GENERAL/'
VUE = SG + 'PRODUCTION_PAR_JOUR/'
JOURNAL = SG + '00_JOURNAL_DE_PRODUCTION.xlsx'
ETAT = SG + '_SOURCES_REGISTRE/etat_validation.json'
ROOTS = ['DOSSIER CLIENTS', 'SUPERVISEUR GENERAL', 'FORMATION LMDC', 'DOCUMENTS_RECUS_PAR_MAIL', 'BASE DOCUMENTAIRE LMDC']
EXTERNES = {'CONTENUS': '/Users/bilefilsseverin/Desktop/CONTENU_MON_FISCALISTE'}   # contenus Mon Fiscaliste CI (scripts, affiches), hors de Documents
EXT_CONTENUS = {'.md', '.pdf', '.png', '.jpg', '.jpeg', '.html', '.xlsx', '.docx', '.txt'}
EXC = ('MES_LIVRABLES', 'MES_MODELES', '_OBSOLETE', '_SOURCES', 'TRANSMISSION_', 'PIECES_RECUES', 'PIECES_JURIDIQUES_RECUES', 'PRODUCTION_PAR_JOUR', 'node_modules', '.git', 'REVUE_EQUIPE', '_ARCHIVE', 'ARCHIVES')
EXT = {'.pdf', '.docx', '.xlsx', '.pptx', '.html'}
EXT_MAIL = EXT | {'.doc', '.xls', '.jpg', '.jpeg', '.png', '.heic', '.csv', '.zip', '.ppt', '.txt', '.rtf', '.odt', '.ods'}   # pièces reçues par mail seulement
STATUTS = ['À valider', 'Validé', 'À corriger', 'Modifié après validation']
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
METHODE = 'MDC — MÉTHODE (SUPERVISEUR GENERAL)'
import re as _re
S_ = r'[ _.-]?'
CATEGORIES = [  # ordre de priorité : la première règle qui correspond l'emporte
    ('Note méthodologique', r'NOTE' + S_ + 'METHODO|METHODOLOGIQUE|METHODOLOGICAL' + S_ + 'NOTE'),
    ('Proposition financière', r'PROPOSITION' + S_ + 'FINANCI|FINANCIAL' + S_ + 'PROPOSAL|OFFRE' + S_ + 'FINANCI|DEVIS|PROFORMA|COTATION'),
    ('Proposition commerciale', r'PROPOSITION' + S_ + 'COMMERCIALE|COMMERCIAL' + S_ + 'PROPOSAL|PROPALE|PLAQUETTE'),
    ('Honoraires et facturation', r'HONORAIRE|FACTURE' + S_ + 'MDC|APPEL' + S_ + 'DE' + S_ + 'FONDS'),
    ('Obligations légales et notes d\'information', r'OBLIGATION|NOTE' + S_ + "(D'?|DE)" + S_ + '?INFORMATION|BENEFICIAIRES?' + S_ + 'EFFECTIFS?|CALENDRIER' + S_ + 'FISCAL|ECHEANCIER'),
    ('Documentation et textes officiels', r'CODE' + S_ + 'GENERAL|CODE' + S_ + 'DU' + S_ + 'TRAVAIL|(^|[ _-])COURS([ _-]|$)|(^|[ _-])FORMATIONS?([ _-]|$)|(^|[ _-])MODULE|TEXTE|(^|[ _-])LOI([ _-]|$)|DECRET|ARRETE|ACTE' + S_ + 'UNIFORME|BULLETIN' + S_ + 'OFFICIEL|DOCTRINE|ANNEXE' + S_ + 'FISCALE|CONVENTION' + S_ + 'COLLECTIVE'),
    ('Social', r'(^|[ _-])CD[ID]([ _-]|$)|CERTIFICAT' + S_ + 'DE' + S_ + '?TRAVAIL|CERTIFICAT' + S_ + 'TRAVAIL|CONTRAT' + S_ + 'DE' + S_ + 'TRAVAIL|CNPS|CNSS|PAIE|BULLETIN|REGLEMENT' + S_ + 'INTERIEUR|DELEGUE|DETACHEMENT|ORDRE' + S_ + 'DE' + S_ + 'MISSION|AVENANT' + S_ + 'DE' + S_ + 'MISSION|INSPECTION|AEJ|SOCIAL|PERSONNEL|SALARI|NON' + S_ + 'REMPLACEMENT|SOLDE' + S_ + 'DE' + S_ + '?TOUT' + S_ + 'COMPTE|SOLDE' + S_ + 'TOUT' + S_ + 'COMPTE|RESIDENCE' + S_ + 'FISCALE|REGISTRE' + S_ + 'DE' + S_ + 'PRESENCE|CERTIFICATS?' + S_ + 'DE' + S_ + 'DETACHEMENT'),
    ('Contrat de prestation', r'(^|[ _-])CONTRAT(?!' + S_ + '(CADRE|DE' + S_ + 'TRANSIT|TRANSIT|DE' + S_ + 'MANDAT|MANDAT))|LETTRE' + S_ + 'DE' + S_ + 'MISSION|MC-CONT|SERVICE' + S_ + 'AGREEMENT|ENGAGEMENT' + S_ + 'LETTER'),
    ("Livrables d'entrée (démarrage)", r'DEMANDE' + S_ + '(DE' + S_ + '|DES' + S_ + ')?PIECES|LISTE' + S_ + 'DES' + S_ + 'PIECES|PIECES' + S_ + 'A' + S_ + 'FOURNIR|GUIDE' + S_ + '(DE' + S_ + ')?COLLABORATION|QUESTIONNAIRE|FICHE' + S_ + 'DE' + S_ + 'COLLECTE|CHECK|PROFIL|GUIDE' + S_ + "D'?" + S_ + 'ENTRETIEN|TRAVAUX' + S_ + 'PRELIMINAIRES|PLAN' + S_ + "D'?" + S_ + 'ACTION|INVENTAIRE'),
    ('Méthode MDC (modèles et procédures)', r'MODELE|PROCEDURE|MANUEL|GUIDE|POLITIQUE|CAHIER' + S_ + 'DES' + S_ + 'CHARGES|DIRECTIVE|NOTE' + S_ + 'DE' + S_ + 'SERVICE|KIT'),
    ('Audit et diagnostic', r'AUDIT|DIAGNOSTIC|ANOMALIE|MATRICE|EXPOSITION|REDRESSEMENT|NOTATION|INDICE|(^|[ _-])DEE([ _-]|$)|EXPLICATION' + S_ + 'ECRITE|CONTROLE|REVISION|ANALYSE|ETUDE|CONSTAT|DEPOUILLEMENT|COHERENCE'),
    ('Suivi et comptabilité', r'RAPPORT' + S_ + 'MENSUEL|SUIVI|TABLEAU' + S_ + 'DE' + S_ + 'BORD|BASE' + S_ + 'COMPTABLE|GRAND' + S_ + 'LIVRE|BALANCE|JOURNAL|RAPPROCHEMENT|RELEVE|SAISIE|ECRITURE|RECONSTITUTION|DEBOURS|CAISSE|BILAN|ETATS?' + S_ + 'FINANCIERS|SYNTHESE|POINT|FICHE' + S_ + 'DE' + S_ + 'TACHES|REPORTING|SITUATION|COMPTA|ETAT' + S_ + 'DES'),
    ('Fiscal', r'DECLARATION|IMPOT|IMPO|TVA|(^|[ _-])ITS([ _-]|$)|TIMBRE|ENREGISTREMENT|FISCAL|PATENTE|(^|[ _-])TEE([ _-]|$)|REGULARIS|DGI'),
    ('Juridique et actes à signer', r'CONVENTION|A' + S_ + 'SIGNER|DECISION|STATUTS?([ _-]|$)|PROCES|(^|[ _-])PV([ _-]|$)|AVENANT|ATTESTATION|(^|[ _-])ACTES?([ _-]|$)|RCCM|CONTRAT|(^|[ _-])MANDAT|RECONNAISSANCE|CERTIFICAT|RECUEIL'),
    ('Courriers et transmissions', r'LETTRE|COURRIER|MAIL|BORDEREAU|TRANSMISSION|RELANCE'),
    ('Notes et rapports', r'NOTE|RAPPORT|MEMO|FICHE'),
]
CAT_NAMES = ['Contenus et scripts', 'Formations'] + [c for c, _ in CATEGORIES] + ['Pièces et documents du client', 'Autres']
_CRX = [(c, _re.compile(r)) for c, r in CATEGORIES]
_PIECES = _re.compile(r'DOCS?' + S_ + 'ENTREPRISE|PIECES|SCAN|RECUS|DEPUIS' + S_ + 'DOCUMENTS|DOCUMENTS' + S_ + 'CLIENT|RELEVE' + S_ + 'BANCAIRE|EXTRAITS?')

RUBRIQUES = SG + '_SOURCES_REGISTRE/rubriques.json'
PREMIERE_VUE = SG + '_SOURCES_REGISTRE/premiere_vue.json'
DELAI_RANGEMENT = 3   # jours pendant lesquels le gérant range lui-même un nouveau document ; rangement automatique le 4e jour

def rubriques():
    try: return json.load(open(RUBRIQUES, encoding='utf-8'))
    except Exception: return []

def save_rubriques(r):
    json.dump(r, open(RUBRIQUES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def all_categories():
    """Les rubriques créées par le gérant d'abord, puis les catégories de l'Agence."""
    return rubriques() + [c for c in CAT_NAMES if c not in rubriques()]

def premiere_vue(docs):
    """Date à laquelle chaque document est apparu pour la première fois. Au premier passage, la date de production sert de date de
    première vue (les documents existants ne remplissent pas la boîte « À ranger »)."""
    try: pv = json.load(open(PREMIERE_VUE, encoding='utf-8')); first = False
    except Exception: pv = {}; first = True
    today = dt.date.today().isoformat(); changed = first
    for k, g in docs.items():
        if k not in pv:
            pv[k] = dt.date.fromtimestamp(g['mtime']).isoformat() if first else today; changed = True
    if changed: json.dump(pv, open(PREMIERE_VUE, 'w', encoding='utf-8'), ensure_ascii=False)
    return pv

def effective_cat(k, g, st):
    return st.get(k, {}).get('cat') or classify(g['nom'], k)

def classify(nom, rel=''):
    """Catégorie d'un document : d'abord d'après son nom, puis d'après le nom de ses dossiers."""
    if rel.startswith('CONTENUS/'): return 'Contenus et scripts'
    if rel.startswith('FORMATION LMDC/'):
        return 'Documentation et textes officiels' if 'TEXTES_OFFICIELS' in rel else 'Formations'
    if rel.startswith('SUPERVISEUR GENERAL/FORMATION_PERSONNELLE/'): return 'Formations'
    u = nom.upper()
    for c, rx in _CRX:
        if c != 'Notes et rapports' and rx.search(u): return c
    parts = rel.split('/')[:-1]
    path = '/'.join(parts[2:] if parts[:1] == ['DOSSIER CLIENTS'] else parts[1:]).upper()
    if _PIECES.search(path): return 'Pièces et documents du client'
    for c, rx in _CRX:
        if c != 'Notes et rapports' and rx.search(path): return c
    if _CRX[-1][1].search(u): return 'Notes et rapports'
    if rel.startswith('SUPERVISEUR GENERAL'): return 'Méthode MDC (modèles et procédures)'
    return 'Autres'

def scan():
    docs = defaultdict(lambda: {'files': [], 'mtime': 0})
    for nom, base in EXTERNES.items():
        for d, ds, fs in os.walk(base):
            ds[:] = [x for x in ds if not x.startswith(('.', '_OBSOLETE', '_SOURCES', 'node_modules'))]
            for f in fs:
                stem, ext = os.path.splitext(f)
                if f.startswith(('~$', '.')) or ext.lower() not in EXT_CONTENUS: continue
                p = os.path.join(d, f)
                if os.path.islink(p): continue
                parts = os.path.relpath(os.path.join(d, stem), base).split('/')
                if parts[0] == 'PDF' and len(parts) > 1: parts = parts[1:]          # le PDF d'un script rejoint son texte
                rel = nom + '/' + '/'.join(parts)
                theme = parts[0] if len(parts) > 1 else 'GÉNÉRAL'
                g = docs[rel]; g['files'].append(p); g['mtime'] = max(g['mtime'], os.path.getmtime(p))
                g['dossier'] = 'CONTENUS — ' + (theme.lstrip('0123456789_ ').replace('_', ' ').strip() or 'GÉNÉRAL')
                g['nom'] = stem; g['dir'] = d
    for R in ROOTS:
        for d, ds, fs in os.walk(DOCS + R):
            ds[:] = [x for x in ds if not any(x.startswith(e) or e in x for e in EXC)]
            for f in fs:
                stem, ext = os.path.splitext(f)
                if f.startswith('~$') or f.startswith('.') or f == '00_JOURNAL_DE_PRODUCTION.xlsx' or ext.lower() not in (EXT_MAIL if R == 'DOCUMENTS_RECUS_PAR_MAIL' else EXT): continue
                p = os.path.join(d, f)
                if os.path.islink(p): continue
                rel = os.path.relpath(os.path.join(d, stem), DOCS)
                parts = rel.split('/')
                if parts[0] == 'FORMATION LMDC':
                    if len(parts) > 2 and parts[1] in ('PDF', 'WORD', 'MD'): parts = [parts[0]] + parts[2:]   # même cours en PDF et en Word : un seul document
                    rel = '/'.join(parts)
                    theme = parts[1] if len(parts) > 2 else 'GÉNÉRAL'
                    dossier = 'FORMATIONS — ' + theme.lstrip('0123456789_ ').replace('_', ' ').strip()
                elif parts[0] == 'DOCUMENTS_RECUS_PAR_MAIL':
                    dossier = '📨 REÇUS PAR MAIL'
                elif parts[0] == 'SUPERVISEUR GENERAL':
                    dossier = 'FORMATIONS — FORMATION PERSONNELLE' if len(parts) > 2 and parts[1] == 'FORMATION_PERSONNELLE' else METHODE
                else:
                    dossier = parts[1].strip()
                g = docs[rel]; g['files'].append(p); g['mtime'] = max(g['mtime'], os.path.getmtime(p))
                g['dossier'] = dossier
                g['nom'] = stem; g['dir'] = d
    return docs

def load_state():
    try: return json.load(open(ETAT, encoding='utf-8'))
    except Exception: return {}

def save_state(st):
    json.dump(st, open(ETAT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def read_back(st):
    """Reprend les statuts changés à la main dans le journal Excel."""
    if not os.path.exists(JOURNAL): return
    try: ws = load_workbook(JOURNAL)['Journal']
    except Exception: return
    hdr = [c.value for c in ws[4]]
    try: ik, isx, io = hdr.index('Clé'), hdr.index('Statut'), hdr.index('Observations')
    except ValueError: return
    for row in ws.iter_rows(min_row=5, values_only=True):
        k = row[ik]
        if not k: continue
        s, o = row[isx], row[io]
        cur = st.get(k, {})
        if s in STATUTS and s != cur.get('statut', 'À valider'):
            cur['statut'] = s
            if s == 'Validé': cur['valide_le'] = dt.date.today().isoformat(); cur['mtime_validation'] = None
        if (o or '') != cur.get('obs', ''): cur['obs'] = o or ''
        if cur: st[k] = cur

def statut(k, g, st):
    e = st.get(k, {})
    s = e.get('statut', 'À valider')
    if s == 'Validé':
        mv = e.get('mtime_validation')
        if mv is None: e['mtime_validation'] = g['mtime']; st[k] = e
        elif g['mtime'] > mv + 2: s = 'Modifié après validation'
    return s

def clear_view():
    if not os.path.isdir(VUE): return
    for d, ds, fs in os.walk(VUE, topdown=False):
        for f in fs:
            p = os.path.join(d, f)
            if os.path.islink(p): os.unlink(p)
        for x in ds:
            p = os.path.join(d, x)
            if os.path.isdir(p) and not os.path.islink(p) and not os.listdir(p): os.rmdir(p)

def link(target, folder, name, unique=False):
    os.makedirs(folder, exist_ok=True)
    dst = os.path.join(folder, name); i = 2
    if unique and os.path.lexists(dst): return
    while os.path.lexists(dst):
        b, e = os.path.splitext(name); dst = os.path.join(folder, f'{b} ({i}){e}'); i += 1
    os.symlink(target, dst)

def build(docs, st, journal=False, views=False):
    """views=False par défaut : les raccourcis PRODUCTION_PAR_JOUR ne sont plus régénérés (Documents est synchronisé par iCloud,
    les milliers de liens saturaient la synchronisation et bloquaient la plateforme — 15/10/2026). La plateforme les remplace."""
    if views: clear_view()
    rows = []
    for k, g in docs.items():
        day = dt.date.fromtimestamp(g['mtime']); s = statut(k, g, st)
        mois = f'{day:%Y-%m} ({MOIS[day.month-1]})'
        for p in sorted(g['files']):
            name = ('✅ ' if s == 'Validé' else ('⚠️ ' if s in ('À corriger', 'Modifié après validation') else '')) + os.path.basename(p)
            if views: link(p, os.path.join(VUE, mois, day.isoformat(), g['dossier']), name)
            if views: link(p, os.path.join(VUE, '_PAR_DOSSIER', g['dossier'], day.isoformat()), name)
            if views: link(p, os.path.join(VUE, '_PAR_CLASSIFICATION', effective_cat(k, g, st).replace('/', '-'), g['dossier']), name)
            if views and s == 'Validé': link(p, os.path.join(VUE, '_VALIDES', g['dossier']), os.path.basename(p), unique=True)
        rows.append((day, g['dossier'], g['nom'], ', '.join(sorted({os.path.splitext(p)[1][1:].lower() for p in g['files']})),
                     os.path.relpath(g['dir'], DOCS), s, st.get(k, {}).get('valide_le'), st.get(k, {}).get('obs', ''), k, sorted(g['files'])[0]))
    rows.sort(key=lambda r: (r[0], r[1], r[2]), reverse=True)
    if journal:
        if os.path.exists(os.path.join(SG, '~$00_JOURNAL_DE_PRODUCTION.xlsx')):
            print('Journal ouvert dans Excel : non réécrit (raccourcis mis à jour).')
        else:
            write_journal(rows)
    return rows

def write_journal(rows):
    NAVY, PALE, GREEN, RED, ORANGE = '1A1A2E', 'F5E5A5', 'E8F6EE', 'FDECEC', 'FFF1DC'
    thin = Side(style='thin', color='D0D0D8'); B = Border(bottom=thin)
    wb = Workbook(); ws = wb.active; ws.title = 'Journal'; ws.sheet_view.showGridLines = False
    ws.sheet_properties.outlinePr.summaryBelow = False
    ws['A1'] = 'LA MAISON DE LA CONFORMITÉ — JOURNAL DE PRODUCTION DES DOCUMENTS, PAR DOSSIER'; ws['A1'].font = Font(bold=True, size=13, color=NAVY)
    ws['A2'] = ("Une ligne par dossier. Cliquer sur le « + » dans la marge de gauche pour afficher les documents du dossier, du plus récent au plus ancien "
                "(les boutons « 1 » et « 2 » en haut à gauche replient ou déplient tous les dossiers). Pour valider : choisir « Validé » dans la colonne Statut "
                "et enregistrer, ou dire à Claude « je valide … ». Mise à jour automatique toutes les 15 minutes.")
    ws['A2'].alignment = Alignment(wrap_text=True); ws.merge_cells('A2:I2'); ws.row_dimensions[2].height = 44
    H = ['Jour de production', 'Dossier', 'Document', 'Formats', 'Emplacement', 'Statut', 'Validé le', 'Observations', 'Clé']
    W = [13, 30, 62, 12, 60, 22, 12, 40, 10]
    for i, (h, w) in enumerate(zip(H, W), 1):
        c = ws.cell(4, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor=NAVY)
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); ws.column_dimensions[c.column_letter].width = w
    groups = defaultdict(list)
    for x in rows: groups[x[1]].append(x)
    order = sorted(groups, key=lambda d: max(x[0] for x in groups[d]), reverse=True)
    r = 5; doc_ranges = []; anchors = {}
    for d in order:
        g = sorted(groups[d], key=lambda x: (x[0], x[2]), reverse=True)
        nv = sum(x[5] == 'Validé' for x in g); na = sum(x[5] in ('À corriger', 'Modifié après validation') for x in g)
        anchors[d] = r
        ws.cell(r, 1, g[0][0]).number_format = 'DD/MM/YYYY'
        ws.cell(r, 2, d)
        ws.cell(r, 3, f'{len(g)} document(s) — {nv} validé(s), {len(g) - nv - na} à valider' + (f', {na} à corriger ou modifié(s)' if na else ''))
        for i in range(1, 10):
            c = ws.cell(r, i); c.font = Font(bold=True, size=10, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='2E3A59')
        ws.row_dimensions[r].height = 18
        r += 1; start = r
        for x in g:
            vals = [x[0], x[1], x[2], x[3], x[4], x[5], dt.date.fromisoformat(x[6]) if x[6] else None, x[7], x[8]]
            for i, v in enumerate(vals, 1):
                c = ws.cell(r, i, v); c.border = B; c.font = Font(size=9)
                if i in (1, 7): c.number_format = 'DD/MM/YYYY'
            ws.cell(r, 3).hyperlink = 'file://' + x[9].replace(' ', '%20'); ws.cell(r, 3).font = Font(size=9, color='1F4E9A', underline='single')
            ws.cell(r, 5).hyperlink = 'file://' + (DOCS + x[4]).replace(' ', '%20')
            ws.row_dimensions[r].outlineLevel = 1; ws.row_dimensions[r].hidden = True
            r += 1
        doc_ranges.append((start, r - 1))
    last = r - 1
    dv = DataValidation(type='list', formula1='"' + ','.join(STATUTS) + '"', allow_blank=False)
    for a_, b_ in doc_ranges: dv.add(f'F{a_}:F{b_}')
    ws.add_data_validation(dv)
    for val, col in [('Validé', GREEN), ('À corriger', RED), ('Modifié après validation', ORANGE), ('À valider', PALE)]:
        ws.conditional_formatting.add(f'F5:F{last}', CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col)))
    ws.column_dimensions['I'].hidden = True
    ws.freeze_panes = 'A5'
    # Synthèse par jour
    sy = wb.create_sheet('Par jour'); sy.sheet_view.showGridLines = False
    sy['A1'] = 'Production et validation par jour'; sy['A1'].font = Font(bold=True, size=12, color=NAVY)
    hd = ['Jour', 'Documents produits', 'Validés', 'À valider', 'À corriger ou modifiés', 'Dossiers concernés']
    for i, h in enumerate(hd, 1):
        c = sy.cell(3, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor=NAVY)
    for col, w in zip('ABCDEF', [12, 18, 10, 12, 20, 90]): sy.column_dimensions[col].width = w
    agg = defaultdict(lambda: [0, 0, 0, 0, set()])
    for x in rows:
        a = agg[x[0]]; a[0] += 1; a[1] += x[5] == 'Validé'; a[2] += x[5] == 'À valider'; a[3] += x[5] in ('À corriger', 'Modifié après validation'); a[4].add(x[1])
    for r, (d, a) in enumerate(sorted(agg.items(), reverse=True), 4):
        for i, v in enumerate([d, a[0], a[1], a[2], a[3], ', '.join(sorted(a[4]))], 1):
            c = sy.cell(r, i, v); c.font = Font(size=9)
            if i == 1: c.number_format = 'DD/MM/YYYY'
    sy.freeze_panes = 'A4'
    # Synthèse par dossier
    sd = wb.create_sheet('Par dossier'); sd.sheet_view.showGridLines = False
    sd['A1'] = 'Production et validation par dossier'; sd['A1'].font = Font(bold=True, size=12, color=NAVY)
    for i, h in enumerate(['Dossier', 'Documents', 'Validés', 'À valider', 'À corriger ou modifiés', 'Dernière production'], 1):
        c = sd.cell(3, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor=NAVY)
    for col, w in zip('ABCDEF', [42, 12, 10, 12, 20, 18]): sd.column_dimensions[col].width = w
    ad = defaultdict(lambda: [0, 0, 0, 0, None])
    for x in rows:
        a = ad[x[1]]; a[0] += 1; a[1] += x[5] == 'Validé'; a[2] += x[5] == 'À valider'; a[3] += x[5] in ('À corriger', 'Modifié après validation'); a[4] = max(a[4] or x[0], x[0])
    for r, (d, a) in enumerate(sorted(ad.items(), key=lambda t: t[1][4], reverse=True), 4):
        for i, v in enumerate([d] + a, 1):
            c = sd.cell(r, i, v); c.font = Font(size=9)
            if i == 6: c.number_format = 'DD/MM/YYYY'
        c = sd.cell(r, 1); c.hyperlink = Hyperlink(ref=c.coordinate, location=f"'Journal'!B{anchors[d]}"); c.font = Font(size=9, color='1F4E9A', underline='single')
    wb.save(JOURNAL)

def match(docs, motif):
    m = motif.lower().rstrip('/')
    return [k for k, g in docs.items() if m in k.lower() or any(m in p.lower() for p in g['files'])]

if __name__ == '__main__':
    st = load_state(); read_back(st); docs = scan()
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    if cmd in ('valider', 'corriger', 'statut'):
        ks = match(docs, sys.argv[2])
        if not ks: print('Aucun document ne correspond à :', sys.argv[2]); sys.exit(1)
        for k in sorted(ks):
            e = st.get(k, {})
            if cmd == 'valider':
                e.update(statut='Validé', valide_le=dt.date.today().isoformat(), mtime_validation=docs[k]['mtime']); st[k] = e
            elif cmd == 'corriger':
                e.update(statut='À corriger', obs=sys.argv[3] if len(sys.argv) > 3 else e.get('obs', '')); st[k] = e
            print(f"{statut(k, docs[k], st):26} {k}")
        print(f'{len(ks)} document(s).')
    rows = build(docs, st, journal=(cmd == 'export')); save_state(st)
    if cmd in ('build', 'export'):
        n = defaultdict(int)
        for x in rows: n[x[5]] += 1
        print(f'{len(rows)} documents classés ; ' + ' ; '.join(f'{v} {k}' for k, v in n.items()))
