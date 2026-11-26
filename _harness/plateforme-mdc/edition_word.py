"""Modification d'un Word directement dans la plateforme (02/11/2026).

- Le texte de chaque paragraphe et de chaque cellule de tableau devient modifiable dans le navigateur.
- À l'enregistrement, seul le texte change : en-tête, logo, styles, gras et mise en page du Word sont conservés.
- L'ancienne version du Word et du PDF est archivée dans _OBSOLETE/VERSIONS_MODIFIEES du dossier (rien n'est supprimé).
- Le PDF du même nom est ensuite refait par Microsoft Word, et il l'est aussi quand le Word est modifié dans Word."""
import os, time, difflib, shutil, threading, subprocess, datetime as dt, html as _h
from docx import Document
from docx.oxml.ns import qn

MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
DEMARRAGE = time.time()
VERROU = threading.Lock()
SORTIE_WORD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'pdf_word')


def _hors_zone(el):
    """Paragraphe situé dans une zone de texte ou dans une variante de secours : non modifiable."""
    p = el.getparent()
    while p is not None:
        if p.tag in (qn('w:txbxContent'), f'{{{MC}}}Fallback'): return True
        p = p.getparent()
    return False


def _textes(p):
    """Éléments w:t propres au paragraphe (sans ceux des zones de texte imbriquées)."""
    out = []
    for t in p.iter(qn('w:t')):
        a = t.getparent()
        while a is not None and a.tag != qn('w:p'): a = a.getparent()
        if a is p: out.append(t)
    return out


def paragraphes(doc):
    return [p for p in doc.element.body.iter(qn('w:p')) if not _hors_zone(p)]


def _texte(p):
    return ''.join(t.text or '' for t in _textes(p))


def ouvert_dans_word(path):
    d, n = os.path.split(path)
    try: return any(f.startswith('~$') and f.endswith(n[2:]) for f in os.listdir(d))
    except Exception: return False


def archiver(path):
    """Copie la version actuelle dans _OBSOLETE/VERSIONS_MODIFIEES (horodatée)."""
    if not os.path.exists(path): return
    d, n = os.path.split(path); b, e = os.path.splitext(n)
    arch = os.path.join(d, '_OBSOLETE', 'VERSIONS_MODIFIEES'); os.makedirs(arch, exist_ok=True)
    shutil.copy2(path, os.path.join(arch, f'{b}_AVANT_{dt.datetime.now():%Y-%m-%d_%Hh%M%S}{e}'))


def _remplacer(p, nouveau):
    """Remplace le texte du paragraphe en gardant la mise en forme de chaque partie (gras, italique…)."""
    ts = _textes(p)
    if not ts:
        r = p.makeelement(qn('w:r'), {}); t = r.makeelement(qn('w:t'), {}); r.append(t); p.append(r); ts = [t]
    proprio = [i for i, t in enumerate(ts) for _ in (t.text or '')]
    ancien = ''.join(t.text or '' for t in ts)
    parts = [''] * len(ts)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ancien, nouveau, autojunk=False).get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1): parts[proprio[i1 + k]] += nouveau[j1 + k]
        elif op in ('replace', 'insert'):
            cible = proprio[i1] if i1 < len(proprio) else (proprio[i1 - 1] if proprio else 0)
            if op == 'insert' and i1 > 0 and i1 <= len(proprio): cible = proprio[i1 - 1]
            parts[cible] += nouveau[j1:j2]
    for t, s in zip(ts, parts):
        t.text = s
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


def _nouveau_paragraphe(modele, texte):
    """Paragraphe neuf qui reprend la mise en forme du paragraphe modèle (style, alignement, police)."""
    import copy
    p = copy.deepcopy(modele)
    r0 = next((r for r in p.iter(qn('w:r')) if r.find(qn('w:t')) is not None), None)
    r0 = copy.deepcopy(r0) if r0 is not None else None
    for c in list(p):
        if c.tag != qn('w:pPr'): p.remove(c)
    if r0 is None:
        r0 = p.makeelement(qn('w:r'), {})
    for c in list(r0):
        if c.tag != qn('w:rPr'): r0.remove(c)
    t = r0.makeelement(qn('w:t'), {}); t.text = texte
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r0.append(t); p.append(r0)
    return p


def enregistrer(path, blocs, version, ajouts=(), suppr=()):
    """blocs : {indice: texte} ; ajouts : [{apres: indice, textes: [...]}] ; suppr : [indices]. Renvoie (ok, message)."""
    with VERROU:
        if int(os.path.getmtime(path)) != int(version):
            return False, 'Le document a été modifié entre-temps. Rechargez la page avant d\'enregistrer.'
        if ouvert_dans_word(path):
            return False, 'Le document est ouvert dans Word. Fermez-le dans Word, puis enregistrez ici.'
        doc = Document(path); ps = paragraphes(doc); n = 0
        for i, txt in (blocs or {}).items():
            i = int(i)
            if 0 <= i < len(ps) and _texte(ps[i]) != txt:
                _remplacer(ps[i], txt.replace('\n', ' ')); n += 1
        for a in ajouts or ():
            i = int(a.get('apres', -1))
            if not 0 <= i < len(ps): continue
            ref = ps[i]
            for txt in a.get('textes') or []:
                q = _nouveau_paragraphe(ps[i], str(txt).replace('\n', ' ')); ref.addnext(q); ref = q; n += 1
        for i in suppr or ():
            i = int(i)
            if not 0 <= i < len(ps): continue
            p = ps[i]; par = p.getparent()
            if par.tag == qn('w:tc') and len(par.findall(qn('w:p'))) == 1: _remplacer(p, '')
            else: par.remove(p)
            n += 1
        if not n: return True, 'Aucune modification à enregistrer.'
        archiver(path)
        tmp = path + '.enregistrement'
        doc.save(tmp); os.replace(tmp, path)
        subprocess.run(['xattr', '-d', 'com.apple.quarantine', path], capture_output=True)
        return True, f'{n} modification(s) enregistrée(s).'


def pdf_voisin(path):
    return os.path.splitext(path)[0] + '.pdf'


def pdf_libreoffice(path, dossier):
    """Conversion par LibreOffice (relais du serveur, où Word n'existe pas). Renvoie le PDF produit, ou None."""
    import hashlib
    os.makedirs(dossier, exist_ok=True)
    dst = os.path.join(dossier, hashlib.sha1(path.encode('utf-8')).hexdigest()[:16] + f'_{int(os.path.getmtime(path))}.pdf')
    if os.path.exists(dst): return dst
    tmp = os.path.join(dossier, 'conv_' + hashlib.sha1(path.encode('utf-8')).hexdigest()[:8])
    os.makedirs(tmp, exist_ok=True)
    with VERROU:
        try: subprocess.run(['soffice', '--headless', '-env:UserInstallation=file://' + os.path.join(dossier, 'profil_lo'),
                             '--convert-to', 'pdf', '--outdir', tmp, path], capture_output=True, timeout=180)
        except Exception: return None
    out = os.path.join(tmp, os.path.splitext(os.path.basename(path))[0] + '.pdf')
    if not os.path.exists(out): return None
    shutil.move(out, dst); return dst


def synchroniser_pdf(path):
    """Refait le PDF du même nom à partir du Word, par Microsoft Word. Renvoie (ok, message)."""
    if os.environ.get('MDC_SERVEUR') == '1':
        pdf = pdf_libreoffice(path, os.path.expanduser('~/cache_apercus'))
        if not pdf: return False, 'Le PDF n\'a pas pu être refait sur le serveur ; il le sera par Word au retour du Mac.'
        dst = pdf_voisin(path); archiver(dst); shutil.copy2(pdf, dst); os.utime(dst, None)
        return True, 'PDF mis à jour.'
    if not os.path.isdir('/Applications/Microsoft Word.app'): return False, 'Microsoft Word est introuvable sur le Mac.'
    if ouvert_dans_word(path): return False, 'Le PDF sera mis à jour dès que le document sera fermé dans Word.'
    dst = pdf_voisin(path)
    os.makedirs(SORTIE_WORD, exist_ok=True)          # dossier où Word a le droit d'écrire ; la plateforme range ensuite le PDF
    tmp = os.path.join(SORTIE_WORD, f'{abs(hash(path))}_{int(time.time())}.pdf')
    esc = lambda x: x.replace('\\', '\\\\').replace('"', '\\"')
    script = (f'set src to POSIX file "{esc(path)}"\n'
              'tell application "Microsoft Word"\n'
              '  open src with read only\n'
              f'  set d to document "{esc(os.path.basename(path))}"\n'
              f'  save as d file name "{esc(tmp)}" file format format PDF\n'
              '  close d saving no\n'
              'end tell')
    with VERROU:
        try: r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=150)
        except Exception: r = None
        if not os.path.exists(tmp):
            return False, 'Word n\'a pas pu produire le PDF. Si Word affiche « Octroyer l\'accès », cliquez sur Sélectionner puis Autoriser.'
        archiver(dst); shutil.move(tmp, dst)
        os.utime(dst, None)
        subprocess.run(['xattr', '-d', 'com.apple.quarantine', dst], capture_output=True)
    return True, 'PDF mis à jour.'


def a_synchroniser(path):
    """Vrai si le Word a été modifié (depuis le lancement de la plateforme) après son PDF."""
    try: m = os.path.getmtime(path)
    except Exception: return False
    if m < DEMARRAGE or time.time() - m < 20: return False      # laisser Word finir d'enregistrer
    pdf = pdf_voisin(path)
    return not os.path.exists(pdf) or os.path.getmtime(pdf) < m - 5


def surveiller(lister_docx, journal=print):
    """Boucle : tout Word modifié (dans la plateforme ou dans Word) voit son PDF refait automatiquement."""
    echecs = {}
    while True:
        try:
            for f in lister_docx():
                if os.path.basename(f).startswith('~$') or not a_synchroniser(f): continue
                m = os.path.getmtime(f)
                if echecs.get(f) == m: continue
                ok, msg = synchroniser_pdf(f)
                if not ok and 'fermé' not in msg: echecs[f] = m
                journal(f'{dt.datetime.now():%d/%m %H:%M:%S} PDF {"mis à jour" if ok else "en attente"} : {os.path.basename(f)} {"" if ok else msg}')
        except Exception as ex:
            journal(f'surveillance Word : {ex}')
        time.sleep(30)


EDIT_CSS = '''<style>
body{margin:0;background:#525659;font:13px -apple-system,sans-serif}
.barre{position:sticky;top:0;z-index:5;background:#1a1a2e;color:#fff;padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.barre button{background:#c9a227;color:#1a1a2e;border:0;border-radius:6px;padding:8px 16px;font-weight:600;cursor:pointer;font-size:13px}
.barre button[disabled]{opacity:.5;cursor:default}.barre .aide{opacity:.8}
#etat{font-weight:600}#etat.ok{color:#8fe3a1}#etat.ko{color:#ff9b9b}
.feuille{background:#fff;max-width:800px;margin:18px auto;padding:56px 64px;box-shadow:0 1px 8px rgba(0,0,0,.35);font:11pt/1.5 "Times New Roman",Times,serif;color:#111}
.feuille [data-i]{outline:none;border-radius:3px;padding:1px 3px;margin:0 -3px 8px;min-height:1.2em;white-space:pre-wrap}
.feuille [data-i]:hover{background:#fdf6dc}.feuille [data-i]:focus{background:#fff8d6;box-shadow:0 0 0 1px #c9a227}
.feuille [data-i].modif{background:#eaf6ea}
.feuille .t1{font-size:19px;font-weight:bold;color:#1a1a2e}.feuille .t2{font-size:17px;font-weight:bold;color:#1a1a2e}
.feuille .vide{color:#bbb}
.feuille table{border-collapse:collapse;width:100%;margin:6px 0 14px}.feuille td{border:1px solid #ccc;padding:5px 7px;vertical-align:top}
.feuille td [data-i]{margin-bottom:2px}.feuille b{font-weight:bold}
</style>'''

EDIT_JS = '''<script>
const T=__TOKEN__,K=__KEY__;let V=__VERSION__;const ORIG={},SUPPR=new Set();
const b=document.getElementById('save'),et=document.getElementById('etat');
try{const m=sessionStorage.getItem('mdc_edit_msg');if(m){const o=JSON.parse(m);et.className=o.c;et.textContent=o.t;sessionStorage.removeItem('mdc_edit_msg')}}catch(e){}
function texte(e){return e.innerText.replace(/\\n$/,'')}
function avantCurseur(e){const s=getSelection();if(!s.rangeCount)return texte(e).length;const r=s.getRangeAt(0).cloneRange();r.selectNodeContents(e);r.setEnd(s.getRangeAt(0).startContainer,s.getRangeAt(0).startOffset);return r.toString().length}
function placer(e,fin){e.focus();const r=document.createRange();r.selectNodeContents(e);r.collapse(!fin);const s=getSelection();s.removeAllRanges();s.addRange(r)}
function brancher(e){
 e.addEventListener('keydown',ev=>{
  if(ev.key==='Enter'){ev.preventDefault();const t=texte(e),k=avantCurseur(e);
   e.textContent=t.slice(0,k);const n=document.createElement('div');n.dataset.n='1';n.contentEditable='true';n.spellcheck=true;
   n.className=(e.className||'').replace('modif','').replace('vide','');n.setAttribute('style',e.getAttribute('style')||'');n.classList.add('modif');n.textContent=t.slice(k);
   e.after(n);brancher(n);placer(n,false);if(e.dataset.i!==undefined)e.classList.toggle('modif',texte(e)!==ORIG[e.dataset.i]);maj()}
  else if(ev.key==='Backspace'&&texte(e)===''&&avantCurseur(e)===0){const all=[...document.querySelectorAll('[data-i],[data-n]')];const j=all.indexOf(e);
   if(j>0){ev.preventDefault();if(e.dataset.i!==undefined)SUPPR.add(e.dataset.i);const p=all[j-1];e.remove();placer(p,true);maj()}}});
 e.addEventListener('paste',ev=>{ev.preventDefault();document.execCommand('insertText',false,(ev.clipboardData.getData('text/plain')||'').replace(/\\s*\\n\\s*/g,' '))});
 e.addEventListener('input',()=>{if(e.dataset.i!==undefined)e.classList.toggle('modif',texte(e)!==ORIG[e.dataset.i]);maj()})}
document.querySelectorAll('[data-i]').forEach(e=>{ORIG[e.dataset.i]=texte(e);brancher(e)});
function modifs(){const blocs={},ajouts=[];let der=null,cur=null;
 document.querySelectorAll('[data-i],[data-n]').forEach(e=>{if(e.dataset.i!==undefined){der=e.dataset.i;cur=null;const t=texte(e);if(t!==ORIG[der])blocs[der]=t}
  else if(der!==null){if(!cur){cur={apres:der,textes:[]};ajouts.push(cur)}cur.textes.push(texte(e))}});
 return {blocs,ajouts,suppr:[...SUPPR]}}
function nb(m){return Object.keys(m.blocs).length+m.ajouts.reduce((s,a)=>s+a.textes.length,0)+m.suppr.length}
function maj(){const n=nb(modifs());b.disabled=!n;if(n){et.className='';et.textContent=n+' modification(s) non enregistrée(s)'}else et.textContent=''}
window.addEventListener('beforeunload',ev=>{if(nb(modifs())&&!window._ok){ev.preventDefault();ev.returnValue=''}});
document.addEventListener('keydown',ev=>{if((ev.metaKey||ev.ctrlKey)&&ev.key==='s'){ev.preventDefault();if(!b.disabled)b.click()}});
b.onclick=async()=>{const m=modifs();if(!nb(m))return;b.disabled=true;et.className='';et.textContent='⏳ Enregistrement du Word et mise à jour du PDF…';
 try{const r=await fetch('/api/docx-modifier',{method:'POST',headers:{'X-MDC-Token':T,'Content-Type':'application/json'},body:JSON.stringify({k:K,v:V,...m})});const d=await r.json();
  if(!r.ok||!d.ok){et.className='ko';et.textContent='❌ '+(d.err||'Enregistrement impossible');b.disabled=false;return}
  const h=new Date().toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'});
  const msg={c:d.pdf?'ok':'ko',t:(d.pdf?'✅ Enregistré à '+h+' : Word et PDF à jour.':'✅ Word enregistré à '+h+'. ⚠️ '+d.msg_pdf)};
  try{sessionStorage.setItem('mdc_edit_msg',JSON.stringify(msg))}catch(e){}
  window._ok=1;location.reload()}
 catch(e){et.className='ko';et.textContent='❌ La plateforme n\\'a pas répondu.';b.disabled=false}};
</script>'''


def _style(p):
    s = p.find(qn('w:pPr'))
    s = s.find(qn('w:pStyle')) if s is not None else None
    v = (s.get(qn('w:val')) if s is not None else '') or ''
    v = v.lower()
    if not (v.startswith(('heading', 'titre')) or v == 'title'): return ''
    return 't1' if v in ('title', 'titre', 'heading1', 'titre1') else 't2'


def page_edition(path, cle, token):
    import json
    doc = Document(path); ps = paragraphes(doc); num = {id(p): i for i, p in enumerate(ps)}
    def para(p):
        i = num.get(id(p))
        if i is None: return ''
        txt = _texte(p)
        if not txt and p.find('.//' + qn('w:drawing')) is not None: return ''
        r0 = next((r for r in p.iter(qn('w:r')) if _textes_run(r)), None)
        rpr = r0.find(qn('w:rPr')) if r0 is not None else None
        def on(tag):
            e = rpr.find(qn(tag)) if rpr is not None else None
            return e is not None and (e.get(qn('w:val')) or 'true').lower() not in ('false', '0', 'off')
        css = []
        if on('w:b'): css.append('font-weight:bold')
        if on('w:i'): css.append('font-style:italic')
        col = rpr.find(qn('w:color')) if rpr is not None else None
        if col is not None and (col.get(qn('w:val')) or 'auto') != 'auto': css.append('color:#' + col.get(qn('w:val')))
        sz = rpr.find(qn('w:sz')) if rpr is not None else None
        if sz is not None and (sz.get(qn('w:val')) or '').isdigit():
            css.append(f"font-size:{int(sz.get(qn('w:val'))) / 2:g}pt")
            if int(sz.get(qn('w:val'))) >= 26 and not on('w:b'): css.append('font-weight:bold')
        ppr = p.find(qn('w:pPr'))
        shd = ppr.find(qn('w:shd')) if ppr is not None else None
        if shd is not None and (shd.get(qn('w:fill')) or 'auto') not in ('auto', 'FFFFFF'): css.append('background:#' + shd.get(qn('w:fill')) + ';padding:4px 8px')
        jc = ppr.find(qn('w:jc')) if ppr is not None else None
        if jc is not None and jc.get(qn('w:val')) in ('center', 'right'): css.append('text-align:' + jc.get(qn('w:val')))
        cls = ' '.join(c for c in (_style(p), 'vide' if not txt.strip() else '') if c)
        contenu = _h.escape(txt)
        st = f' style="{";".join(css)}"' if css else ''
        return f'<div data-i="{i}" contenteditable="true" spellcheck="true" class="{cls}"{st}>{contenu}</div>'
    def bloc(el):
        if el.tag == qn('w:p'): return para(el)
        if el.tag == qn('w:tbl'):
            lignes = []
            for tr in el.iter(qn('w:tr')):
                if tr.getparent() is not None and tr.getparent() is not el: continue
                cel = []
                for tc in tr.findall(qn('w:tc')):
                    tp = tc.find(qn('w:tcPr')); sh = tp.find(qn('w:shd')) if tp is not None else None
                    fond = sh.get(qn('w:fill')) if sh is not None else None
                    st = f' style="background:#{fond}"' if fond and fond not in ('auto', 'FFFFFF') else ''
                    cel.append(f'<td{st}>' + ''.join(bloc(x) for x in tc if x.tag in (qn('w:p'), qn('w:tbl'))) + '</td>')
                lignes.append('<tr>' + ''.join(cel) + '</tr>')
            return '<table>' + ''.join(lignes) + '</table>'
        if el.tag == qn('w:sdt'):
            c = el.find(qn('w:sdtContent'))
            return ''.join(bloc(x) for x in c) if c is not None else ''
        return ''
    corps = ''.join(bloc(el) for el in doc.element.body)
    js = (EDIT_JS.replace('__TOKEN__', json.dumps(token)).replace('__KEY__', json.dumps(cle))
          .replace('__VERSION__', str(int(os.path.getmtime(path)))))
    barre = ('<div class="barre"><button id="save" disabled>Enregistrer (⌘S)</button><span id="etat"></span>'
             '<span class="aide">Cliquez dans le texte pour écrire. Entrée crée un nouveau paragraphe ; effacer un paragraphe vide le supprime. '
             'L\'en-tête, le logo et la mise en page sont conservés ; le PDF se met à jour à l\'enregistrement.</span></div>')
    return (f'<!doctype html><html lang="fr"><meta charset="utf-8"><title>{_h.escape(os.path.basename(path))}</title>'
            f'{EDIT_CSS}{barre}<div class="feuille">{corps}</div>{js}</html>')


def _textes_run(r):
    return any((t.text or '').strip() for t in r.findall(qn('w:t')))
