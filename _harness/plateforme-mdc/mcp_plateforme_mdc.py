#!/usr/bin/env python3
"""Serveur MCP de la Plateforme MDC (15/10/2026) : permet à un modèle de piloter la plateforme par le chat.

- Il parle à la plateforme locale (http://localhost:8765) avec le jeton écrit par le serveur dans .token : la plateforme doit être lancée.
- Il n'a AUCUN outil d'envoi de mail : il prépare des brouillons Gmail ou un dossier d'envoi ; l'envoi reste un geste du gérant dans la plateforme.
- Il ne supprime aucun document et ne donne accès à aucun identifiant (.env, trousseau, mot de passe d'accès téléphone).
- Protocole : MCP sur stdio, messages JSON-RPC (un par ligne). Bibliothèque standard uniquement."""
import os, sys, json, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'http://localhost:8765'
DOCS = '/Users/bilefilsseverin/Documents'
LISIBLES = {'.md', '.txt', '.csv', '.docx', '.pdf', '.xlsx'}

def _token():
    try: return open(os.path.join(HERE, '.token')).read().strip()
    except Exception: raise RuntimeError("La plateforme n'est pas lancée : ouvrez « Plateforme MDC » sur le Mac.")

def appel(chemin, donnees=None):
    for essai in (1, 2):
        req = urllib.request.Request(BASE + chemin, method='POST' if donnees is not None else 'GET',
            data=json.dumps(donnees).encode('utf-8') if donnees is not None else None,
            headers={'X-MDC-Token': _token(), 'Content-Type': 'application/json', 'Host': 'localhost:8765'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read() or b'{}')
        except urllib.error.HTTPError as e:
            corps = e.read().decode('utf-8', 'ignore')
            try: msg = json.loads(corps).get('err')
            except Exception: msg = None
            if e.code == 403 and essai == 1: continue
            raise RuntimeError(msg or f'La plateforme a refusé la demande (code {e.code})')
        except urllib.error.URLError:
            raise RuntimeError("La plateforme ne répond pas : ouvrez « Plateforme MDC » sur le Mac.")

def _docs(): return appel('/api/docs')

def _resume(d):
    return {'cle': d['k'], 'dossier': d['d'], 'nom': d['n'], 'jour': d['j'], 'formats': d['f'], 'statut': d['s'], 'classification': d['c'],
            'livrable': d['l'], 'modele': d['md'], 'dans_r2': (d['cl'] or None), 'a_ranger': d['in'], 'emplacement': d['e']}

def lister_documents(dossier='', statut='', classification='', recherche='', livrables_seulement=False, a_ranger_seulement=False, limite=40):
    L = _docs()['docs']; r = []
    for d in L:
        if dossier and dossier.lower() not in d['d'].lower(): continue
        if statut and d['s'] != statut: continue
        if classification and classification.lower() not in (d['c'] or '').lower(): continue
        if recherche and recherche.lower() not in (d['n'] + ' ' + d['d']).lower(): continue
        if livrables_seulement and not d['l']: continue
        if a_ranger_seulement and not d['in']: continue
        r.append(d)
    r.sort(key=lambda d: d['j'], reverse=True)
    return {'total': len(r), 'affiches': min(len(r), limite), 'documents': [_resume(d) for d in r[:limite]]}

def synthese():
    D = _docs(); L = D['docs']; c = {}
    for d in L: c[d['s']] = c.get(d['s'], 0) + 1
    dos = {}
    for d in L: dos[d['d']] = dos.get(d['d'], 0) + 1
    return {'documents': len(L), 'par_statut': c, 'livrables': sum(1 for d in L if d['l']), 'a_ranger': sum(1 for d in L if d['in']),
            'dans_r2': sum(1 for d in L if d['cl']), 'classifications': D['cats'], 'rubriques_perso': D['rub'], 'dossiers': dict(sorted(dos.items(), key=lambda x: -x[1])[:25]), 'maj': D['maj']}

def lire_fichier(chemin, max_caracteres=12000):
    p = os.path.realpath(os.path.expanduser(chemin if chemin.startswith('/') else os.path.join(DOCS, chemin)))
    if not p.startswith(DOCS + '/'): raise RuntimeError('Chemin hors de Documents')
    ext = os.path.splitext(p)[1].lower()
    if ext not in LISIBLES: raise RuntimeError('Format non lisible ici (md, txt, csv, docx, pdf, xlsx seulement)')
    if not os.path.isfile(p): raise RuntimeError('Fichier introuvable')
    if ext in ('.md', '.txt', '.csv'): t = open(p, encoding='utf-8', errors='replace').read()
    elif ext == '.docx':
        import docx; t = '\n'.join(x.text for x in docx.Document(p).paragraphs)
    elif ext == '.pdf':
        import fitz; t = '\n'.join(pg.get_text() for pg in fitz.open(p))
    else:
        import openpyxl; wb = openpyxl.load_workbook(p, read_only=True, data_only=True); t = ''
        for ws in wb.worksheets:
            t += f'## {ws.title}\n'
            for row in ws.iter_rows(values_only=True):
                t += ' | '.join('' if v is None else str(v) for v in row) + '\n'
                if len(t) > max_caracteres: break
    return {'chemin': p, 'tronque': len(t) > max_caracteres, 'texte': t[:max_caracteres]}

def trouver_fichiers(cle):
    """Chemins des fichiers d'un document (pour lire_fichier)."""
    d = next((x for x in _docs()['docs'] if x['k'] == cle), None)
    if not d: raise RuntimeError('Document introuvable')
    base = os.path.join(DOCS, d['e']) if not d['e'].startswith('~') else os.path.expanduser(d['e'])
    fs = sorted(f for f in os.listdir(base) if os.path.splitext(f)[0] == d['n'] or f.startswith(d['n'])) if os.path.isdir(base) else []
    return {'dossier': base, 'fichiers': [os.path.join(base, f) for f in fs]}

def valider(cles, statut, observation=''):
    if statut not in ('À valider', 'Validé', 'À corriger'): raise RuntimeError('Statut : « À valider », « Validé » ou « À corriger »')
    appel('/api/statut', {'keys': cles, 'statut': statut, 'obs': observation}); return {'ok': True, 'documents': len(cles), 'statut': statut}

def classer(cles, classification):
    appel('/api/categorie', {'keys': cles, 'cat': classification}); return {'ok': True, 'documents': len(cles), 'classification': classification}

def rubrique(action, nom, nouveau_nom='', cle=''):
    if action not in ('creer', 'renommer', 'supprimer'): raise RuntimeError('Action : creer, renommer ou supprimer')
    appel('/api/rubrique', {'action': action, 'nom': nom, 'nouveau': nouveau_nom, 'k': cle or None}); return {'ok': True}

def livrable(cle, actif=True):
    appel('/api/livrable', {'k': cle, 'on': bool(actif)}); return {'ok': True, 'livrable': bool(actif)}

def modele(cle, actif=True):
    appel('/api/modele', {'k': cle, 'on': bool(actif)}); return {'ok': True, 'modele': bool(actif)}

def adresses(): return appel('/api/carnet', {})

def mail_etat(): return appel('/api/mail', {})
def mail_relever(): return appel('/api/mail', {'action': 'importer'})

def preparer_brouillon(cles, destinataires, objet, message, copies='', pieces='pdf'):
    """Dépose un BROUILLON dans Gmail. N'envoie jamais."""
    return appel('/api/envoi', {'keys': cles, 'mode': 'gmail', 'a': ', '.join(destinataires) if isinstance(destinataires, list) else destinataires,
                                'cc': copies, 'objet': objet, 'message': message, 'pref': pieces})

def preparer_dossier_envoi(cles, destinataires, objet, message, pieces='pdf'):
    return appel('/api/envoi', {'keys': cles, 'mode': 'dossier', 'a': ', '.join(destinataires) if isinstance(destinataires, list) else destinataires,
                                'objet': objet, 'message': message, 'pref': pieces})

def cloud_etat(): return appel('/api/r2', {})
def cloud_envoyer(cles): return appel('/api/r2-envoi', {'keys': cles})
def cloud_auto(): return appel('/api/r2', {'action': 'auto'})
def cloud_pause(): return appel('/api/r2', {'action': 'pause'})

def actualiser(): return appel('/api/docs?refresh=1') and {'ok': True}

S = lambda t, **p: {'type': t, **p}
def schema(props, req=()): return {'type': 'object', 'properties': props, 'required': list(req)}
CLES = S('array', items=S('string'), description='Clés des documents (champ « cle » de lister_documents)')
TOOLS = [
 ('synthese', 'Vue d\'ensemble : nombre de documents par statut, livrables, à ranger, dans R2, classifications et dossiers.', schema({}), synthese),
 ('lister_documents', 'Liste les documents de la plateforme avec filtres (dossier, statut, classification, mot de recherche, livrables, à ranger).',
  schema({'dossier': S('string'), 'statut': S('string', description='À valider, Validé, À corriger, Modifié après validation'), 'classification': S('string'), 'recherche': S('string'),
          'livrables_seulement': S('boolean'), 'a_ranger_seulement': S('boolean'), 'limite': S('integer')}), lister_documents),
 ('trouver_fichiers', 'Donne les chemins des fichiers d\'un document, à passer à lire_fichier.', schema({'cle': S('string')}, ['cle']), trouver_fichiers),
 ('lire_fichier', 'Lit le texte d\'un fichier (md, txt, csv, docx, pdf, xlsx) situé dans Documents.', schema({'chemin': S('string'), 'max_caracteres': S('integer')}, ['chemin']), lire_fichier),
 ('valider_documents', 'Change le statut de documents : À valider, Validé ou À corriger (avec observation facultative).', schema({'cles': CLES, 'statut': S('string'), 'observation': S('string')}, ['cles', 'statut']), valider),
 ('classer_documents', 'Range des documents dans une classification ou une rubrique personnelle existante.', schema({'cles': CLES, 'classification': S('string')}, ['cles', 'classification']), classer),
 ('gerer_rubrique', 'Crée, renomme ou supprime une rubrique personnelle (les documents ne sont jamais supprimés). « cle » facultative : range ce document dans la nouvelle rubrique.',
  schema({'action': S('string', description='creer, renommer ou supprimer'), 'nom': S('string'), 'nouveau_nom': S('string'), 'cle': S('string')}, ['action', 'nom']), rubrique),
 ('marquer_livrable', 'Coche ou décoche « bon » (★) : le document entre dans Mes livrables et devient transmissible vers le cloud.', schema({'cle': S('string'), 'actif': S('boolean')}, ['cle']), livrable),
 ('marquer_modele', 'Ajoute ou retire un document de Mes modèles (⭐).', schema({'cle': S('string'), 'actif': S('boolean')}, ['cle']), modele),
 ('carnet_adresses', 'Liste les adresses e-mail connues (carnet) avec leurs dossiers.', schema({}), adresses),
 ('mail_etat', 'État de l\'import des mails reçus.', schema({}), mail_etat),
 ('mail_relever', 'Relève maintenant les pièces jointes des mails reçus (lecture seule).', schema({}), mail_relever),
 ('preparer_brouillon_gmail', 'Prépare un BROUILLON Gmail avec les documents choisis. N\'envoie jamais : le gérant relit puis envoie lui-même.',
  schema({'cles': CLES, 'destinataires': S('array', items=S('string')), 'objet': S('string'), 'message': S('string'), 'copies': S('string'), 'pieces': S('string', description='pdf ou tous')}, ['cles', 'objet', 'message']), preparer_brouillon),
 ('preparer_dossier_envoi', 'Prépare un dossier d\'envoi (pièces + bordereau + zip) à envoyer plus tard.',
  schema({'cles': CLES, 'destinataires': S('array', items=S('string')), 'objet': S('string'), 'message': S('string'), 'pieces': S('string')}, ['cles', 'objet', 'message']), preparer_dossier_envoi),
 ('cloud_etat', 'État du mode cloud Cloudflare R2 (actif, bucket, envoi automatique, derniers envois).', schema({}), cloud_etat),
 ('cloud_envoyer', 'Envoie vers R2 les livrables (★) parmi les documents indiqués ; les autres sont ignorés.', schema({'cles': CLES}, ['cles']), cloud_envoyer),
 ('cloud_basculer_auto', 'Active ou désactive l\'envoi automatique des livrables vers R2.', schema({}), cloud_auto),
 ('cloud_basculer_pause', 'Met le mode cloud en pause ou le reprend.', schema({}), cloud_pause),
 ('actualiser', 'Relit les dossiers et met la plateforme à jour.', schema({}), actualiser),
]
PAR_NOM = {t[0]: t for t in TOOLS}

def repondre(msg):
    m, i = msg.get('method'), msg.get('id')
    if m == 'initialize':
        return {'jsonrpc': '2.0', 'id': i, 'result': {'protocolVersion': (msg.get('params') or {}).get('protocolVersion', '2024-11-05'),
                'capabilities': {'tools': {}}, 'serverInfo': {'name': 'plateforme-mdc', 'version': '1.0'},
                'instructions': "Pilote la Plateforme MDC. Aucun envoi de mail possible : seulement des brouillons. Rien n'est supprimé. Les clés R2 et mots de passe ne sont jamais accessibles."}}
    if m == 'ping': return {'jsonrpc': '2.0', 'id': i, 'result': {}}
    if m == 'tools/list':
        return {'jsonrpc': '2.0', 'id': i, 'result': {'tools': [{'name': n, 'description': d, 'inputSchema': s} for n, d, s, _ in TOOLS]}}
    if m == 'tools/call':
        p = msg.get('params') or {}; t = PAR_NOM.get(p.get('name'))
        if not t: return {'jsonrpc': '2.0', 'id': i, 'error': {'code': -32602, 'message': 'Outil inconnu'}}
        try:
            res = t[3](**(p.get('arguments') or {})); err = False
            txt = json.dumps(res, ensure_ascii=False, indent=1)
        except Exception as ex: txt, err = f'Erreur : {ex}', True
        return {'jsonrpc': '2.0', 'id': i, 'result': {'content': [{'type': 'text', 'text': txt}], 'isError': err}}
    if i is not None: return {'jsonrpc': '2.0', 'id': i, 'error': {'code': -32601, 'message': 'Méthode inconnue'}}

if __name__ == '__main__':
    for ligne in sys.stdin:
        ligne = ligne.strip()
        if not ligne: continue
        try: r = repondre(json.loads(ligne))
        except Exception as ex: r = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': str(ex)}}
        if r: sys.stdout.write(json.dumps(r, ensure_ascii=False) + '\n'); sys.stdout.flush()
