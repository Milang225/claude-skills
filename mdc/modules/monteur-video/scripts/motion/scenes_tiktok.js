// ============================================================================
// SCÈNES TIKTOK — pensées pour le vertical 1080×1920 (chargé par scene_cinema.html)
// Plein écran : scène 1080×1920 (mise à l'échelle si horizontal). Habillages « sur orateur » : accroche,
// commentaire, rec. Zone utile TikTok : y 230 → 1300 (haut = onglets, bas = sous-titres et description).
// Textes : sc.texts ; instants clés : sc.keys.a / sc.keys.b (relatifs au début de la scène).
// ============================================================================
const TK={gold:'#E8B64A',gold2:'#FFD98A',navy:'#16213F',red:'#E5484D',green:'#22B46E',ink:'#16213F',mute:'#7A8499'};
function vstage(kind){
  const el=$(`<div class="scene ${kind==='light'?'light':'dark'}"></div>`);root.appendChild(el);
  if(kind==='navy')el.appendChild($(`<div class="abs" style="inset:0;background:radial-gradient(110% 70% at 50% 35%,#1F2F60 0%,#101A3A 55%,#070C1C 100%)"></div>`));
  if(kind==='dark')el.appendChild($(`<div class="abs" style="inset:0;background:radial-gradient(95% 60% at 50% 40%,#18213D 0%,#080C18 70%,#04060C 100%)"></div>`));
  const st=$(`<div class="abs" style="left:0;top:0;width:1080px;height:1920px;transform-origin:0 0"></div>`);
  const sc=Math.min(W/1080,H/1920);S(st,{transform:`translate(${(W-1080*sc)/2}px,${(H-1920*sc)/2}px) scale(${sc})`});
  el.appendChild(st);el.appendChild($(`<div class="grain" style="opacity:${kind==='light'?.035:.06}"></div>`));
  return {el,st};
}
function vt(st,txt,y,{size=64,w=700,color,gold=false,italic=false,cls='',pad=80,ls='-.01em'}={}){
  const e=$(`<div class="abs ${gold?'goldg':''} ${cls}" style="left:0;right:0;text-align:center;top:${y}px;font-size:${size}px;font-weight:${w};letter-spacing:${ls};${italic?'font-style:italic;':''}${color?`color:${color};`:''}line-height:1.12;padding:0 ${pad}px">${esc(txt)}</div>`);
  st.appendChild(e);return e;
}
const pop=(el,t,t0,d=.45,extra='')=>{const e=oB(P(t,t0,d),1.7);S(el,{opacity:cl(P(t,t0,d*.5)),transform:`${extra} scale(${.4+.6*e})`});return e};
function stamp(st,txt,{x,y,color=TK.red,size=64,rot=-12,w=0}={}){
  const e=$(`<div class="abs" style="left:${x}px;top:${y}px;transform-origin:50% 50%;padding:14px 30px;border:7px solid ${color};border-radius:16px;color:${color};font-weight:900;font-size:${size}px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;${w?`width:${w}px;text-align:center;`:''}mix-blend-mode:multiply;opacity:0">${esc(txt)}</div>`);
  st.appendChild(e);
  return (t,t0)=>{const e2=P(t,t0,.22);S(e,{opacity:e2>0?.92:0,transform:`translate(-50%,-50%) rotate(${rot}deg) scale(${2.2-1.2*oQ(e2)})`})};
}
const kTa=(k,d)=>k.a??d, kTb=(k,d)=>k.b??d;

// ---------------------------------------------------------------- habillages sur orateur
// ACCROCHE — titre d'accroche des 3 premières secondes (textes : l1, l2, style « bande » | « tampon » | « neon »)
B.accroche=(sc)=>{const X=sc.texts||{};const el=$(`<div class="scene"></div>`);root.appendChild(el);
  const style=X.style||'bande';
  const shade=$(`<div class="abs" style="left:0;right:0;top:0;height:${H*.42}px;background:linear-gradient(180deg,rgba(5,9,20,.78) 0%,rgba(5,9,20,.45) 60%,transparent 100%)"></div>`);el.appendChild(shade);
  const box=$(`<div class="abs" style="left:0;right:0;top:${H*.125}px;text-align:center"></div>`);el.appendChild(box);
  const w1=(X.l1||'').split(' ').filter(Boolean).map(w=>{const s=$(`<span style="display:inline-block;margin:0 .14em;font-weight:800;font-size:${V?62:56}px;color:#fff;text-transform:uppercase;letter-spacing:.01em;text-shadow:0 4px 18px rgba(0,0,0,.5)">${esc(w)}</span>`);return s});
  const l1=$(`<div style="padding:0 60px;line-height:1.15"></div>`);w1.forEach(s=>l1.appendChild(s));box.appendChild(l1);
  let l2;
  if(style==='tampon'){l2=$(`<div style="display:inline-block;margin-top:26px;padding:10px 34px;border:7px solid ${TK.gold};border-radius:18px;color:${TK.gold2};font-weight:900;font-size:${V?96:84}px;text-transform:uppercase;letter-spacing:.02em;text-shadow:0 0 30px rgba(232,182,74,.5)">${esc(X.l2||'')}</div>`)}
  else if(style==='neon'){l2=$(`<div style="margin-top:18px;font-weight:900;font-size:${V?110:90}px;color:#FFF3D0;text-transform:uppercase;letter-spacing:.01em;text-shadow:0 0 10px #FFD98A,0 0 30px #E8B64A,0 0 70px rgba(232,150,40,.8)">${esc(X.l2||'')}</div>`)}
  else{l2=$(`<div style="display:inline-block;margin-top:22px;padding:8px 30px 14px;background:linear-gradient(180deg,#F3D77E,#C99A2E);color:${TK.navy};font-weight:900;font-size:${V?96:84}px;text-transform:uppercase;letter-spacing:.01em;border-radius:10px;transform-origin:0 50%">${esc(X.l2||'')}</div>`)}
  box.appendChild(l2);
  return (t,D,k)=>{const x=P(t,D-.35,.35);S(el,{opacity:1-x,filter:x>0?`blur(${x*12}px)`:'none'});
    shade.style.opacity=oQ(P(t,0,.3));
    w1.forEach((s,i)=>{const e=oB(P(t,.05+i*.09,.35),1.6);S(s,{opacity:cl(P(t,.05+i*.09,.15)),transform:`translateY(${(1-e)*40}px) scale(${.7+.3*e})`})});
    const t2=kTa(k,.25+w1.length*.09);
    if(style==='tampon'){const e=P(t,t2,.2);S(l2,{opacity:e>0?1:0,transform:`rotate(-4deg) scale(${2-oQ(e)})`})}
    else if(style==='neon'){const f=Math.floor((t-t2)*24);S(l2,{opacity:t<t2?0:([1,0,1,1,0,1][f]??1)})}
    else{const e=oQ(P(t,t2,.35));S(l2,{opacity:e>0?1:0,clipPath:`inset(0 ${(1-e)*100}% 0 0)`})}};};

// COMMENTAIRE — vignette « réponse à un commentaire » façon TikTok (textes : nom, texte)
B.commentaire=(sc)=>{const X=sc.texts||{};const el=$(`<div class="scene"></div>`);root.appendChild(el);
  const card=$(`<div class="abs" style="left:70px;right:70px;top:${H*.13}px;background:#fff;border-radius:30px;padding:30px 36px 34px;box-shadow:0 24px 60px rgba(0,0,0,.35);transform-origin:20% 0">
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:18px"><div style="width:74px;height:74px;border-radius:50%;background:linear-gradient(135deg,#F3D77E,#C99A2E);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:36px;color:${TK.navy}">${esc((X.nom||'A')[0].toUpperCase())}</div>
    <div style="font-size:30px;color:#8A8F9C;font-weight:600">Réponse au commentaire de <b style="color:#161823">${esc(X.nom||'un abonné')}</b></div></div>
    <div class="txt" style="font-size:44px;line-height:1.25;color:#161823;font-weight:600"></div></div>`);el.appendChild(card);
  const tail=$(`<div class="abs" style="left:120px;top:0;width:40px;height:40px;background:#fff;transform:rotate(45deg)"></div>`);card.appendChild(tail);S(tail,{top:'auto',bottom:'-16px'});
  const words=(X.texte||'').split(' ');const tx=card.querySelector('.txt');
  const spans=words.map(w=>{const s=$(`<span>${esc(w)} </span>`);tx.appendChild(s);return s});
  return (t,D,k)=>{const e=oB(P(t,0,.45),1.5),x=P(t,D-.3,.3);
    S(card,{opacity:cl(P(t,0,.2))*(1-x),transform:`scale(${(.5+.5*e)*(1-.1*x)})`,filter:x>0?`blur(${x*10}px)`:'none'});
    const rate=Math.max(.04,Math.min(.12,(D-1.2)/Math.max(1,words.length)));
    spans.forEach((s,i)=>{s.style.opacity=t>.35+i*rate?1:.12})};};

// REC — viseur de caméra sur l'orateur (textes : label)
B.rec=(sc)=>{const X=sc.texts||{};const el=$(`<div class="scene"></div>`);root.appendChild(el);
  const m=60,top=H*.165,bot=H*.66;
  const corner=(x,y,r)=>$(`<div class="abs" style="left:${x}px;top:${y}px;width:90px;height:90px;border-left:7px solid #fff;border-top:7px solid #fff;border-radius:14px 0 0 0;transform:rotate(${r}deg);filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))"></div>`);
  const cs=[corner(m,top,0),corner(W-m-90,top,90),corner(W-m-90,bot-90,180),corner(m,bot-90,270)];cs.forEach(c=>el.appendChild(c));
  const rec=$(`<div class="abs" style="left:${m+30}px;top:${top+30}px;display:flex;align-items:center;gap:14px;font-weight:800;font-size:40px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.6)"><span class="dot" style="width:30px;height:30px;border-radius:50%;background:#FF3B30;box-shadow:0 0 18px #FF3B30"></span>REC</div>`);el.appendChild(rec);
  const tc=$(`<div class="abs" style="right:${m+30}px;top:${top+34}px;font-family:Menlo,monospace;font-weight:700;font-size:36px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.6)"></div>`);el.appendChild(tc);
  const focus=$(`<div class="abs" style="left:${W/2-110}px;top:${H*.3}px;width:220px;height:220px;border:4px solid ${TK.gold2};border-radius:12px"></div>`);el.appendChild(focus);
  const lab=$(`<div class="abs" style="left:0;right:0;top:${bot+30}px;text-align:center"><span style="display:inline-block;padding:14px 34px;border-radius:50px;background:rgba(10,14,28,.72);color:#fff;font-weight:700;font-size:42px">📱 ${esc(X.label||'garde une trace')}</span></div>`);el.appendChild(lab);
  return (t,D)=>{const e=oQ(P(t,0,.35)),x=P(t,D-.3,.3);S(el,{opacity:e*(1-x)});
    cs.forEach((c,i)=>{const s=1.25-.25*e;c.style.scale=s});
    rec.querySelector('.dot').style.opacity=Math.floor(t*2.4)%2?.25:1;
    const sec=Math.floor(t+11);tc.textContent=`00:00:${String(sec).padStart(2,'0')}`;
    const f=P(t,.15,.6);S(focus,{opacity:f<1?1-f*.85+.15*Math.sin(t*20):.15,transform:`scale(${1.5-.5*oQ(f)})`});
    blurIn(lab,t,.5,.4)};};

// ---------------------------------------------------------------- plein écran
// PREUVES — « tout type de preuve peut servir » (textes : title, items[[emoji, label]…], after ; clés : a = coches, b = after)
B.preuves=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const items=X.items||[["💬","Messages WhatsApp"],["📲","Mobile Money"],["🏦","Virement bancaire"],["📸","Photos / vidéos"],["📧","E-mails"],["👥","Témoins"]];
  const t1=vt(st,X.title??"Tout type de preuve<br>peut servir",270,{size:76,w:800,color:TK.ink});
  const cards=items.map(([ic,lb],i)=>{const c=i%2,r=Math.floor(i/2);
    const e=$(`<div class="abs" style="left:${90+c*470}px;top:${560+r*230}px;width:430px;height:190px;border-radius:30px;background:#fff;border:2px solid #E3E6EE;box-shadow:0 18px 40px rgba(20,30,60,.10);display:flex;align-items:center;gap:22px;padding:0 28px">
      <div style="width:104px;height:104px;flex:none;border-radius:50%;background:#F6F1E4;border:3px solid ${TK.gold};display:flex;align-items:center;justify-content:center;font-size:54px">${ic}</div>
      <div style="font-size:38px;font-weight:700;color:${TK.ink};line-height:1.1">${esc(lb)}</div>
      <div class="ok abs" style="right:-14px;top:-14px;width:60px;height:60px;border-radius:50%;background:${TK.green};color:#fff;font-size:38px;font-weight:900;display:flex;align-items:center;justify-content:center;opacity:0">✓</div></div>`);st.appendChild(e);return e});
  const af=vt(st,X.after??"Absolument tout.",1250,{size:84,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.45);
    cards.forEach((c,i)=>{const a=.25+i*.16;const e=oQ(P(t,a,.5));S(c,{opacity:e,filter:e<1?`blur(${(1-e)*12}px)`:'none',transform:`translate(${(1-e)*(i%2?140:-140)}px,0) rotate(${(1-e)*(i%2?6:-6)}deg)`});
      const ok=c.querySelector('.ok'),o=oB(P(t,kTa(k,1.6)+i*.1,.35),2);S(ok,{opacity:cl(o*3),transform:`scale(${o})`});
      c.style.borderColor=t>kTa(k,1.6)+i*.1?TK.gold:'#E3E6EE'});
    blurIn(af,t,kTb(k,2.4),.5)};};

// DÉCHARGE — feuille de décharge remplie, signée, tamponnée (textes : title ; clés : a = signature, b = tampon)
B.decharge=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"Fais signer une décharge",250,{size:72,w:800,color:TK.ink});
  const paper=$(`<div class="abs" style="left:120px;top:420px;width:840px;height:880px;background:#fff;border-radius:10px;box-shadow:0 40px 90px rgba(20,30,60,.22);padding:60px 64px;color:#1C2236;transform-origin:50% 100%">
    <div style="text-align:center;font-weight:900;font-size:${X.head?44:56}px;letter-spacing:${X.head?'.12em':'.22em'}">${esc(X.head??'DÉCHARGE')}</div>
    <div style="height:3px;background:${TK.gold};margin:22px 120px 40px"></div></div>`);st.appendChild(paper);
  const L=X.lines||["Je soussigné(e) <u>&nbsp;Kouassi&nbsp;Jean&nbsp;</u>","reconnais avoir reçu la somme de","<u>&nbsp;250&nbsp;000&nbsp;FCFA&nbsp;</u> en espèces","de la part de <u>&nbsp;M.&nbsp;Koné&nbsp;</u>","Fait à Abidjan, le <u>&nbsp;05/10/2026&nbsp;</u>"];
  const ls=L.map(l=>{const e=$(`<div style="font-size:38px;line-height:1.55;font-family:Georgia,serif">${l}</div>`);paper.appendChild(e);return e});
  const sigLab=$(`<div style="margin-top:40px;font-size:30px;color:#8A8F9C;text-align:right">Signature</div>`);paper.appendChild(sigLab);
  const sig=$(`<svg class="abs" width="420" height="160" viewBox="0 0 420 160" style="right:60px;bottom:70px;overflow:visible"><path d="M10 110 C 40 20, 70 20, 60 100 S 110 150, 130 70 S 170 20, 185 95 C 195 140, 230 60, 250 80 S 300 120, 330 60 L 400 50" fill="none" stroke="#1C3D8F" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>`);paper.appendChild(sig);
  const sp=sig.querySelector('path');
  const stp=stamp(st,X.stamp??"REÇU",{x:330,y:1120,color:'#1C3D8F',size:70,rot:-14});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);
    const e=oQ(P(t,.1,.55));S(paper,{opacity:e,transform:`translateY(${(1-e)*260}px) rotate(${(1-e)*-4}deg)`});
    ls.forEach((l,i)=>{l.style.opacity=oC(P(t,.45+i*.22,.3))});
    draw(sp,t,kTa(k,1.7),.8);stp(t,kTb(k,2.6))};};

// AIGUILLAGE — l'argent qui entre : chiffre d'affaires par défaut, apport si un document le dit (clé : a = document)
B.aiguillage=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('navy');
  const t1=vt(st,X.title??"Tout ce qui entre<br>dans la société…",250,{size:68,w:700});
  const svg=$(`<svg class="abs" width="1080" height="1920" style="left:0;top:0;overflow:visible">
    <path d="M400 470 L680 470 L590 640 L490 640 Z" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.35)" stroke-width="3"/>
    <line x1="540" y1="640" x2="540" y2="800" stroke="rgba(255,255,255,.25)" stroke-width="40" stroke-linecap="round"/>
    <g class="arm"><line x1="540" y1="800" x2="540" y2="930" stroke="${TK.gold2}" stroke-width="16" stroke-linecap="round"/></g>
    <circle cx="540" cy="800" r="20" fill="${TK.gold}"/></svg>`);st.appendChild(svg);
  const box=(x,lab,sub,col)=>{const e=$(`<div class="abs" style="left:${x}px;top:1040px;width:400px;height:230px;border-radius:26px;border:4px solid ${col};background:rgba(255,255,255,.05);text-align:center;padding-top:36px">
     <div style="font-weight:900;font-size:40px;color:${col};line-height:1.1">${lab}</div><div style="margin-top:12px;font-size:32px;color:rgba(255,255,255,.75)">${sub}</div>
     <div class="n" style="margin-top:10px;font-size:34px;font-weight:800;color:#fff"></div></div>`);st.appendChild(e);return e};
  const bl=box(70,X.left??"CHIFFRE<br>D'AFFAIRES",X.left_sub??"imposé",TK.red), br=box(610,X.right??"APPORT<br>DE L'ASSOCIÉ",X.right_sub??"remboursable",TK.gold2);
  const doc=$(`<div class="abs" style="left:640px;top:700px;padding:16px 24px;border-radius:14px;background:#fff;color:${TK.ink};font-weight:800;font-size:32px;box-shadow:0 20px 40px rgba(0,0,0,.4)">📄 ${esc(X.doc??"Convention d'apport")}</div>`);st.appendChild(doc);
  const N=22,coins=[...Array(N)].map((_,i)=>{const c=$(`<div class="abs" style="left:0;top:0;width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF1C9,#E8B64A 55%,#9A7518);border:3px solid #8C6A14;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:30px;color:#6B4E0E">F</div>`);st.appendChild(c);return c});
  const arm=svg.querySelector('.arm');
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.45);const ka=kTa(k,1.8);
    const sw=iO(P(t,ka+.15,.35));arm.setAttribute('transform',`rotate(${40-80*sw} 540 800)`);
    const de=oB(P(t,ka-.1,.4));S(doc,{opacity:cl(de*2),transform:`translateX(${(1-de)*300}px) rotate(${(1-de)*10}deg)`});
    let nl=0,nr=0;
    const gap=Math.max(.14,(D-1.6)/N);coins.forEach((c,i)=>{const s=.3+i*gap,u=t-s;if(u<0){c.style.opacity=0;return}
      const right=s+.55>ka+.2;const tx=right?810:270;let x,y;
      if(u<.55){x=540+Math.sin(i)*60*(1-u/.55);y=380+u/.55*420}else{const v=Math.min(1,(u-.55)/.45);x=540+(tx-540)*v;y=800+v*v*300}
      if(u>1){right?nr++:nl++;c.style.opacity=0;return}
      S(c,{opacity:1,transform:`translate(${x-32}px,${y-32}px) rotate(${u*300}deg)`})});
    const f=n=>`+${String(n*50000).replace(/\B(?=(\d{3})+(?!\d))/g,' ')} F`;if(X.compteur!==false){bl.querySelector('.n').textContent=nl?f(nl):'';br.querySelector('.n').textContent=nr?f(nr):''}
    blurIn(bl,t,.2,.4);blurIn(br,t,.3,.4);
    S(bl,{boxShadow:nl&&t<ka+.6?`0 0 40px rgba(229,72,77,.45)`:'none'});S(br,{boxShadow:nr?`0 0 40px rgba(255,217,138,.45)`:'none'})};};

// ÉCHÉANCIER — « 1 mois, 2 mois, 3 mois, 15 mois : il faut tout préciser » (textes : title, head, items[[n, u]], after ; clé : b = after)
B.echeancier=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"Remboursé quand ?",270,{size:74,w:800,color:TK.ink});
  const it=X.items||[["1","mois"],["2","mois"],["3","mois"],["15","mois"]];
  const cards=it.map(([n,u],i)=>{const c=i%2,r=Math.floor(i/2);const e=$(`<div class="abs" style="left:${130+c*430}px;top:${500+r*350}px;width:390px;height:310px;border-radius:30px;background:#fff;box-shadow:0 22px 50px rgba(20,30,60,.12);overflow:hidden;text-align:center">
     <div style="height:70px;background:${TK.navy};color:${TK.gold2};font-weight:800;font-size:30px;letter-spacing:.2em;line-height:70px">${esc(X.head??'ÉCHÉANCE')}</div>
     <div style="font-weight:900;font-size:130px;color:${TK.ink};line-height:1.25">${esc(n)}</div><div style="font-size:40px;color:${TK.mute};margin-top:-18px">${esc(u)}</div>
     <div class="ck abs" style="right:22px;top:88px;font-size:52px;color:${TK.green};font-weight:900;opacity:0">✓</div></div>`);st.appendChild(e);return e});
  const af=vt(st,X.after??"Il faut <span class='itgold'>tout préciser</span>.",1270,{size:72,w:800,color:TK.ink});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);
    cards.forEach((c,i)=>{const a=.25+i*.32;const e=oB(P(t,a,.42),1.6);S(c,{opacity:cl(P(t,a,.15)),transform:`translateY(${(1-e)*60}px) rotate(${(1-e)*(i%2?5:-5)}deg) scale(${.8+.2*e})`});
      c.querySelector('.ck').style.opacity=oC(P(t,a+.3,.2))});
    blurIn(af,t,kTb(k,1.9),.5)};};

// DIVIDENDE — l'argent qui ressort sans document devient un dividende (textes : title, from, to, after ; clé : a = bascule)
B.dividende=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const t1=vt(st,X.title??"Sans documentation…",260,{size:66,w:600,color:'rgba(255,255,255,.88)'});
  const bld=$(`<svg class="abs" width="360" height="420" viewBox="0 0 360 420" style="left:90px;top:560px">
    <path d="M20 140 L180 40 L340 140 Z" fill="url(#gGold)"/><rect x="40" y="150" width="280" height="250" rx="6" fill="#1B274A" stroke="url(#gGold)" stroke-width="5"/>
    ${[0,1,2].map(r=>[0,1,2].map(c=>`<rect x="${78+c*78}" y="${180+r*62}" width="46" height="40" rx="4" fill="rgba(255,217,138,.55)"/>`).join('')).join('')}
    <rect x="150" y="340" width="60" height="60" fill="#0B1226" stroke="url(#gGold)" stroke-width="3"/></svg>`);st.appendChild(bld);
  const blab=vt(st,X.company??"la société",1000,{size:36,w:600,color:'rgba(255,255,255,.7)'});S(blab,{left:'90px',right:'auto',width:'360px',padding:0});
  const per=$(`<svg class="abs" width="280" height="340" viewBox="0 0 280 340" style="left:700px;top:640px"><circle cx="140" cy="70" r="58" fill="url(#gGold)"/><path d="M30 330 C 30 200, 70 150, 140 150 C 210 150, 250 200, 250 330 Z" fill="url(#gGold)"/></svg>`);st.appendChild(per);
  const plab=vt(st,X.person??"toi",1000,{size:36,w:600,color:'rgba(255,255,255,.7)'});S(plab,{left:'700px',right:'auto',width:'280px',padding:0});
  const bag=$(`<div class="abs" style="left:0;top:0;text-align:center;width:300px"><div style="font-size:130px">💰</div>
    <div class="lb" style="display:inline-block;margin-top:6px;padding:10px 22px;border-radius:14px;font-weight:900;font-size:36px;white-space:nowrap"></div></div>`);st.appendChild(bag);
  const lb=bag.querySelector('.lb');
  const af=vt(st,X.after??"⚠️ imposé comme un dividende",1180,{size:52,w:800,color:'#FF8A8E'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);blurIn(bld,t,.1,.45);blurIn(blab,t,.2,.4);blurIn(per,t,.25,.45);blurIn(plab,t,.3,.4);
    const ka=kTa(k,1.4);const m=iO(P(t,.5,1.1));S(bag,{opacity:cl(P(t,.45,.2)),transform:`translate(${120+m*470}px,${640-Math.sin(m*Math.PI)*170}px)`});
    const fl=P(t,ka,.3);const red=fl>.5;
    lb.textContent=red?(X.to??"DIVIDENDE"):(X.from??"remboursement ?");
    S(lb,{background:red?TK.red:'rgba(255,255,255,.12)',color:'#fff',transform:`scaleX(${Math.abs(Math.cos(fl*Math.PI))})`});
    blurIn(af,t,ka+.4,.45)};};

// STATUTS — le livret des statuts s'ouvre : rien n'est prévu (textes : title, articles[], stamp ; clés : a = ouverture, b = tampon)
B.statuts=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"Que disent les statuts ?",260,{size:70,w:800,color:TK.ink});
  const page=$(`<div class="abs" style="left:110px;top:430px;width:860px;height:840px;background:#fff;border-radius:12px;box-shadow:0 40px 90px rgba(20,30,60,.2);padding:70px 66px;color:#1C2236;font-family:Georgia,serif"></div>`);st.appendChild(page);
  const arts=X.articles||[["Article 14","Rémunération du gérant"],["Article 15","Indemnité en cas de révocation"]];
  const rows=arts.map(([a,l])=>{const e=$(`<div style="margin-bottom:70px"><div style="font-size:32px;color:#B8862A;font-weight:700;letter-spacing:.08em;text-transform:uppercase">${esc(a)}</div>
     <div style="font-size:44px;font-weight:700;margin:10px 0 18px">${esc(l)}${X.plein?'':' :'}</div><div class="bl" style="height:6px;border-bottom:5px ${X.plein?'solid #E8B64A':'dotted #B9BFCC'};width:0"></div></div>`);page.appendChild(e);return e});
  const cover=$(`<div class="abs" style="left:110px;top:430px;width:860px;height:840px;border-radius:12px;background:linear-gradient(160deg,#1F2F60,#0E1733);border:5px solid ${TK.gold};transform-origin:0 50%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;backface-visibility:hidden">
     ${seal(180)}<div style="font-family:Georgia,serif;font-size:96px;font-weight:700;letter-spacing:.14em;color:${TK.gold2};text-align:center;line-height:1.1;padding:0 40px">${esc(X.cover1??'STATUTS')}</div><div style="font-size:32px;color:rgba(255,255,255,.7);letter-spacing:.2em;text-align:center">${esc(X.cover2??'DE LA SOCIÉTÉ')}</div></div>`);st.appendChild(cover);
  const stp=stamp(st,X.stamp??"RIEN DE PRÉVU",{x:540,y:1120,size:72,rot:-10});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const ka=kTa(k,.9);
    const o=iO(P(t,ka,.6));S(cover,{opacity:cl(P(t,.1,.3))*(o<.98?1:0),transform:`perspective(2400px) rotateY(${-o*100}deg)`});
    page.style.opacity=cl(P(t,.1,.3));
    rows.forEach((r,i)=>{r.querySelector('.bl').style.width=`${oC(P(t,ka+.5+i*.4,.5))*100}%`});
    stp(t,kTb(k,ka+1.8))};};

// PIÈCE — « même 5 F » : une pièce qui tombe, puis barrée (textes : value, unit, after ; clé : a = barre)
B.piece=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const coin=$(`<div class="abs" style="left:290px;top:560px;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF6DC 0%,#F1D27A 30%,#C99A2E 70%,#8C6A14 100%);box-shadow:0 0 0 14px #A9821F inset,0 0 0 20px rgba(255,241,201,.5) inset,0 40px 90px rgba(0,0,0,.6);display:flex;flex-direction:column;align-items:center;justify-content:center;color:#5C430C">
     <div style="font-family:Georgia,serif;font-weight:900;font-size:230px;line-height:.9">${esc(X.value??'5')}</div><div style="font-weight:800;font-size:64px;letter-spacing:.1em">${esc(X.unit??'FRANCS')}</div></div>`);st.appendChild(coin);
  const glow=$(`<div class="abs" style="left:140px;top:410px;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,rgba(255,200,90,.35),transparent 65%)"></div>`);st.insertBefore(glow,coin);
  const x=$(`<svg class="abs" width="620" height="620" viewBox="0 0 620 620" style="left:230px;top:500px;overflow:visible"><line x1="40" y1="40" x2="580" y2="580" stroke="${TK.red}" stroke-width="40" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/><line x1="580" y1="40" x2="40" y2="580" stroke="${TK.red}" stroke-width="40" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/></svg>`);st.appendChild(x);
  const ln=x.querySelectorAll('line');
  const t1=vt(st,X.title??"Même pas",300,{size:76,w:700,color:'rgba(255,255,255,.85)'});
  const af=vt(st,X.after??"tu n'auras rien.",1180,{size:80,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);
    const f=P(t,.1,.7),b=oB(f,1.2);const spin=t*6;
    S(coin,{transform:`translateY(${(1-b)*-700}px) scaleX(${lerp(Math.cos(t*14),1,oQ(P(t,.55,.35)))})`});
    glow.style.opacity=oC(P(t,.7,.4));const ka=kTa(k,1.1);draw(ln[0],t,ka,.2);draw(ln[1],t,ka+.15,.2);
    blurIn(af,t,kTb(k,ka+.4),.45)};};

// PORTE — mis à la porte (textes : title, sign, after ; clé : a = sortie)
B.porte=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('navy');
  const t1=vt(st,X.title??"Les associés décident<br>de te mettre à la porte",250,{size:62,w:700});
  const fr=$(`<div class="abs" style="left:290px;top:520px;width:500px;height:760px;background:linear-gradient(180deg,#FFF6DC,#FFD98A 60%,#E8B64A);box-shadow:0 0 120px rgba(255,200,90,.55);border:14px solid #2A3A6E;border-bottom:none"></div>`);st.appendChild(fr);
  const door=$(`<div class="abs" style="left:304px;top:534px;width:472px;height:746px;background:linear-gradient(90deg,#3A2A18,#5A4126);transform-origin:0 50%;border-radius:4px"><div class="abs" style="right:40px;top:380px;width:26px;height:26px;border-radius:50%;background:${TK.gold}"></div></div>`);st.appendChild(door);
  const sign=$(`<div class="abs" style="left:390px;top:440px;width:300px;padding:10px 0;text-align:center;background:${TK.green};color:#fff;font-weight:900;font-size:40px;letter-spacing:.12em;border-radius:10px">${esc(X.sign??'SORTIE')}</div>`);st.appendChild(sign);
  const man=$(`<div class="abs" style="left:400px;top:900px;font-size:300px;line-height:1">🚶🏿‍♂️</div>`);st.appendChild(man);
  const af=vt(st,X.after??"…sans rien.",1240,{size:76,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.45);blurIn(fr,t,.1,.4);blurIn(sign,t,.25,.35);
    const o=iO(P(t,.4,.6));S(door,{opacity:cl(P(t,.1,.3)),transform:`perspective(1600px) rotateY(${-o*78}deg)`});
    const ka=kTa(k,1.1);const m=iO(P(t,ka,1.1));S(man,{opacity:cl(P(t,ka,.2))*(1-P(t,ka+.9,.3)),transform:`translate(${-m*40}px,${-m*360}px) scale(${1-.55*m})`,filter:`brightness(${1-.7*m})`});
    blurIn(af,t,kTb(k,ka+.8),.45)};};

// DUEL — salarié ≠ gérant (textes : left, right, l_items[], r_items[] ; clé : a = « ≠ »)
B.duel=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const col=(x,head,sub,items,c)=>{const e=$(`<div class="abs" style="left:${x}px;top:330px;width:470px;height:930px;border-radius:34px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.02));border:2px solid ${c};padding:44px 30px;text-align:center">
     <div style="font-size:120px;line-height:1">${head[0]}</div><div style="margin-top:10px;font-weight:900;font-size:58px;letter-spacing:.06em;color:${c}">${esc(head[1])}</div>
     <div style="font-size:30px;color:rgba(255,255,255,.6);margin:6px 0 40px">${esc(sub)}</div></div>`);
    const its=items.map(s=>{const i=$(`<div style="margin:0 0 22px;padding:20px 10px;border-radius:18px;background:rgba(255,255,255,.07);font-size:36px;font-weight:700;color:#fff">${esc(s)}</div>`);e.appendChild(i);return i});
    st.appendChild(e);return [e,its]};
  const [L,li]=col(50,[X.left_icon??"👷🏿",X.left??"SALARIÉ"],X.left_sub??"contrat de travail",X.l_items||["Code du travail","Inspection du travail","Indemnités de licenciement"],'#8FB4FF');
  const [R,ri]=col(560,[X.right_icon??"💼",X.right??"GÉRANT"],X.right_sub??"mandat social",X.r_items||["Statuts","Décision des associés","Rien d'automatique"],TK.gold2);
  const ne=$(`<div class="abs" style="left:460px;top:420px;width:160px;height:160px;border-radius:50%;background:${TK.red};color:#fff;font-weight:900;font-size:110px;line-height:148px;text-align:center;box-shadow:0 0 0 12px rgba(229,72,77,.25),0 20px 50px rgba(0,0,0,.5)">≠</div>`);st.appendChild(ne);
  return (t,D,k)=>{sceneFx(el,t,D);
    const a=oQ(P(t,.05,.5));S(L,{opacity:a,transform:`translateX(${(1-a)*-300}px)`});S(R,{opacity:a,transform:`translateX(${(1-a)*300}px)`});
    li.forEach((i,n)=>blurIn(i,t,.45+n*.22,.35));ri.forEach((i,n)=>blurIn(i,t,.55+n*.22,.35));
    pop(ne,t,kTa(k,1.3),.45)};};

// GUICHET — l'inspection du travail : « non concerné » (textes : sign, file, body, stamp ; clé : a = tampon)
B.guichet=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const plaque=$(`<div class="abs" style="left:110px;top:280px;width:860px;padding:34px 0;border-radius:18px;background:${TK.navy};border:5px solid ${TK.gold};text-align:center;color:${TK.gold2};font-weight:900;font-size:58px;letter-spacing:.06em;line-height:1.15">🏛️<br>${esc(X.sign??'INSPECTION<br>DU TRAVAIL')}</div>`);st.appendChild(plaque);
  const file=$(`<div class="abs" style="left:170px;top:720px;width:740px;height:520px;border-radius:16px;background:#F3E3BC;box-shadow:0 30px 70px rgba(20,30,60,.2);padding:50px 56px;color:#3B2F17">
     <div style="font-size:30px;letter-spacing:.2em;font-weight:700;color:#8A7444">DOSSIER</div><div style="font-size:60px;font-weight:900;margin:14px 0 26px">${esc(X.file??'M. le Gérant')}</div>
     <div style="font-size:36px;line-height:1.6">${X.body??'Objet : renvoi<br>Demande : indemnités'}</div></div>`);st.appendChild(file);
  const stp=stamp(st,X.stamp??"NON CONCERNÉ",{x:540,y:1010,size:74,rot:-11});
  return (t,D,k)=>{sceneFx(el,t,D);const p=oB(P(t,.05,.5),1.4);S(plaque,{opacity:cl(P(t,.05,.2)),transform:`translateY(${(1-p)*-120}px)`});
    const f=oQ(P(t,.35,.55));S(file,{opacity:f,transform:`translateX(${(1-f)*900}px) rotate(${(1-f)*8-2}deg)`});stp(t,kTa(k,1.3))};};

// VALISE — « prends tes bagages, rentre à la maison » (textes : title, after ; clé : b = after)
B.valise=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('navy');
  const t1=vt(st,X.title??"Prends tes bagages…",260,{size:72,w:700});
  const sv=$(`<svg class="abs" width="440" height="420" viewBox="0 0 440 420" style="left:90px;top:620px;overflow:visible">
    <rect x="150" y="10" width="140" height="70" rx="26" fill="none" stroke="url(#gGold)" stroke-width="18"/>
    <rect x="20" y="70" width="400" height="330" rx="36" fill="#8C5A2B" stroke="#5C3A18" stroke-width="6"/>
    <rect x="20" y="70" width="400" height="330" rx="36" fill="url(#gGold)" opacity=".18"/>
    <rect x="100" y="70" width="26" height="330" fill="#5C3A18"/><rect x="314" y="70" width="26" height="330" fill="#5C3A18"/></svg>`);st.appendChild(sv);
  const path=$(`<svg class="abs" width="1080" height="1920" style="left:0;top:0;overflow:visible"><path d="M520 900 C 640 760, 760 760, 820 860" fill="none" stroke="${TK.gold2}" stroke-width="8" stroke-dasharray="4 22" stroke-linecap="round"/></svg>`);st.appendChild(path);
  const home=$(`<div class="abs" style="left:700px;top:760px;font-size:230px;line-height:1">🏠</div>`);st.appendChild(home);
  const af=vt(st,X.after??"…et laisse pour toi à Dieu 🙏🏿",1200,{size:64,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const b=oB(P(t,.15,.55),1.3);S(sv,{opacity:cl(P(t,.15,.2)),transform:`translateY(${(1-b)*-500}px) rotate(${(1-b)*-14}deg)`});
    const p=oC(P(t,.7,.6));path.style.clipPath=`inset(0 ${100-p*100}% 0 0)`;pop(home,t,1.1,.45);blurIn(af,t,kTb(k,1.7),.5)};};

// TICKET — ticket de pari, prélèvement à la source (textes : title, rows[[l,v]], gain, rate, after ; clés : a = tampon, b = after)
B.ticket=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"Ton gain dépasse 1 million ?",260,{size:66,w:800,color:TK.ink});
  const zig='polygon(0 0,100% 0,100% 96%,'+[...Array(24)].map((_,i)=>`${100-(i+.5)*100/24}% ${i%2?96:100}%`).join(',')+',0 96%)';
  const tk=$(`<div class="abs" style="left:150px;top:400px;width:780px;height:820px;background:#fff;clip-path:${zig};padding:56px 60px;color:#1C2236;font-family:Menlo,monospace;filter:drop-shadow(0 30px 50px rgba(20,30,60,.2))">
    <div style="text-align:center;font-weight:900;font-size:42px;letter-spacing:.14em;font-family:-apple-system,sans-serif">🎟️ TICKET DE PARI</div>
    <div style="border-top:4px dashed #C9CDD8;margin:30px 0"></div></div>`);st.appendChild(tk);
  const rows=(X.rows||[["Mise","5 000 F"],["Cote","200,00"]]).map(([l,v])=>{const e=$(`<div style="display:flex;justify-content:space-between;font-size:40px;margin-bottom:24px"><span style="color:#7A8499">${esc(l)}</span><b>${esc(v)}</b></div>`);tk.appendChild(e);return e});
  const g=$(`<div style="margin-top:30px;padding:26px 24px;border-radius:14px;background:#FFF5DA;border:3px solid ${TK.gold}"><div style="font-size:32px;color:#7A6A3A">GAIN POTENTIEL</div><div style="font-size:76px;font-weight:900;color:${TK.ink}">${esc(X.gain??'1 000 000 F')}</div></div>`);tk.appendChild(g);
  const tax=$(`<div style="margin-top:26px;font-size:44px;text-align:center;font-family:-apple-system,sans-serif;font-weight:800;color:${TK.red}">${esc(X.tax??"– 75 000 F pour l'État")}</div>`);tk.appendChild(tax);
  const stp=stamp(st,X.rate??"Prélèvement 7,5 %",{x:540,y:1135,size:56,rot:-9,color:TK.red});
  const af=vt(st,X.after??"C'est tout.",1250,{size:72,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const e=oQ(P(t,.1,.55));S(tk,{opacity:e,transform:`translateY(${(1-e)*-300}px)`});
    rows.forEach((r,i)=>{r.style.opacity=oC(P(t,.5+i*.2,.25))});g.style.opacity=oC(P(t,.9,.3));
    const ka=kTa(k,1.6);stp(t,ka);tax.style.opacity=oC(P(t,ka+.35,.3));blurIn(af,t,kTb(k,ka+1),.45)};};

// AGRÉMENT — la plateforme est-elle agréée ? (textes : app, check, after ; clés : a = ✖, b = after)
B.agrement=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const ph=$(`<div class="abs" style="left:300px;top:290px;width:480px;height:880px;border-radius:70px;background:#0B0F1C;border:12px solid #2B3350;box-shadow:0 40px 100px rgba(0,0,0,.6);overflow:hidden">
     <div style="margin:110px auto 0;width:220px;height:220px;border-radius:52px;background:linear-gradient(135deg,#34C759,#0A7D35);display:flex;align-items:center;justify-content:center;font-size:130px">${X.icon??'⚽'}</div>
     <div style="text-align:center;color:#fff;font-weight:800;font-size:46px;margin-top:30px">${esc(X.app??'PARIS 24/7')}</div>
     <div style="text-align:center;color:rgba(255,255,255,.5);font-size:30px;margin-top:8px">${esc(X.app_sub??'Gagne des millions !')}</div></div>`);st.appendChild(ph);
  const q=$(`<div class="abs" style="left:90px;right:90px;top:1060px;padding:30px 34px;border-radius:26px;background:#fff;display:flex;align-items:center;gap:26px;box-shadow:0 30px 60px rgba(0,0,0,.45)">
     <div style="flex:1;font-size:44px;font-weight:800;color:${TK.ink};line-height:1.15">${esc(X.check??'Agréée par la LONACI ?')}</div>
     <div class="bx" style="width:110px;height:110px;flex:none;border-radius:22px;border:5px solid #C9CDD8;display:flex;align-items:center;justify-content:center;font-size:80px;font-weight:900;color:#fff"></div></div>`);st.appendChild(q);
  const bx=q.querySelector('.bx');
  const af=vt(st,X.after??"Sinon, ton argent est exposé.",1270,{size:54,w:800,color:'#FF8A8E'});
  return (t,D,k)=>{sceneFx(el,t,D);const p=oQ(P(t,.05,.5));S(ph,{opacity:p,transform:`translateY(${(1-p)*120}px) scale(${.92+.08*p})`});
    blurIn(q,t,.5,.4);const ka=kTa(k,1.3);const x=oB(P(t,ka,.35),2);
    bx.textContent=t>=ka?'✖':'';S(bx,{background:t>=ka?TK.red:'transparent',borderColor:t>=ka?TK.red:'#C9CDD8',transform:`scale(${t>=ka?x:1})`});
    S(ph,{filter:t>=ka?`grayscale(${oC(P(t,ka,.5))}) brightness(${1-.4*oC(P(t,ka,.5))})`:'none'});blurIn(af,t,kTb(k,ka+.6),.45)};};

// MACHINE — blanchir l'argent « par une société » (textes : title, label, after ; clé : b = after)
B.machine=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('navy');
  const t1=vt(st,X.title??"Blanchir de l'argent…",250,{size:70,w:700});
  const body=$(`<div class="abs" style="left:190px;top:430px;width:700px;height:820px;border-radius:50px;background:linear-gradient(180deg,#F4F6FA,#C9CFDA);box-shadow:0 50px 100px rgba(0,0,0,.55)">
     <div style="height:130px;border-bottom:4px solid #AEB6C6;display:flex;align-items:center;justify-content:space-between;padding:0 50px">
       <div style="padding:10px 26px;border-radius:12px;background:${TK.navy};color:${TK.gold2};font-weight:900;font-size:42px;letter-spacing:.12em">${esc(X.label??'SOCIÉTÉ')}</div>
       <div style="width:70px;height:70px;border-radius:50%;background:#AEB6C6;border:6px solid #8E97AA"></div></div>
     <div class="door abs" style="left:110px;top:220px;width:480px;height:480px;border-radius:50%;background:#2A3350;border:26px solid #9AA3B6;overflow:hidden;box-shadow:inset 0 0 60px rgba(0,0,0,.8)"><div class="drum abs" style="inset:0"></div>
       <div class="abs" style="inset:0;border-radius:50%;background:radial-gradient(circle at 30% 25%,rgba(255,255,255,.35),transparent 45%)"></div></div></div>`);st.appendChild(body);
  const drum=body.querySelector('.drum');
  const notes=[...Array(9)].map((_,i)=>{const n=$(`<div class="abs" style="left:150px;top:190px;width:170px;height:84px;border-radius:8px;background:linear-gradient(135deg,#9BD3A8,#3E8E5A);border:3px solid #2C6B42;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:30px;color:#14391F">10 000 F</div>`);drum.appendChild(n);return n});
  const af=vt(st,X.after??"…par une société.",1240,{size:80,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const b=oQ(P(t,.1,.5));S(body,{opacity:b,transform:`translateY(${(1-b)*200}px) rotate(${Math.sin(t*38)*.6*P(t,.6,.3)}deg)`});
    const sp=t*(2+3*P(t,.5,1.2));notes.forEach((n,i)=>{const a=sp+i*2*Math.PI/notes.length,r=110+30*Math.sin(i*2.1);
      S(n,{transform:`translate(${Math.cos(a)*r}px,${Math.sin(a)*r}px) rotate(${a*57+90}deg)`,opacity:cl(P(t,.3+i*.05,.2))})});
    blurIn(af,t,kTb(k,1.4),.45)};};

// RADAR — l'apport repéré, considéré comme suspect (textes : title, blip, verdict ; clés : a = blip, b = verdict)
B.radar=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const t1=vt(st,X.title??"Tu apportes de l'argent ?",250,{size:66,w:700});
  const cx=540,cy=820,R=380;
  const svg=$(`<svg class="abs" width="1080" height="1920" style="left:0;top:0;overflow:visible">
    <defs><radialGradient id="rdg"><stop offset="0" stop-color="rgba(255,217,138,.16)"/><stop offset="1" stop-color="rgba(255,217,138,0)"/></radialGradient>
    <linearGradient id="swp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="rgba(255,217,138,0)"/><stop offset="1" stop-color="rgba(255,217,138,.55)"/></linearGradient></defs>
    <circle cx="${cx}" cy="${cy}" r="${R}" fill="url(#rdg)" stroke="rgba(255,217,138,.5)" stroke-width="3"/>
    ${[.25,.5,.75].map(f=>`<circle cx="${cx}" cy="${cy}" r="${R*f}" fill="none" stroke="rgba(255,217,138,.22)" stroke-width="2"/>`).join('')}
    <line x1="${cx-R}" y1="${cy}" x2="${cx+R}" y2="${cy}" stroke="rgba(255,217,138,.18)"/><line x1="${cx}" y1="${cy-R}" x2="${cx}" y2="${cy+R}" stroke="rgba(255,217,138,.18)"/>
    <g class="sw"><path d="M${cx} ${cy} L${cx+R} ${cy} A${R} ${R} 0 0 0 ${cx+R*Math.cos(-.6)} ${cy+R*Math.sin(-.6)} Z" fill="url(#swp)"/></g>
    <circle class="bp" cx="${cx+170}" cy="${cy-150}" r="22" fill="${TK.gold2}"/><circle class="ring" cx="${cx+170}" cy="${cy-150}" r="22" fill="none" stroke="${TK.gold2}" stroke-width="4"/></svg>`);st.appendChild(svg);
  const sw=svg.querySelector('.sw'),bp=svg.querySelector('.bp'),ring=svg.querySelector('.ring');
  const tag=$(`<div class="abs" style="left:${cx+90}px;top:${cy-300}px;padding:12px 22px;border-radius:14px;background:rgba(255,255,255,.1);border:2px solid ${TK.gold2};color:#fff;font-weight:800;font-size:34px;white-space:nowrap">${esc(X.blip??'Apport : 500 000 000 F')}</div>`);st.appendChild(tag);
  const vd=vt(st,X.verdict??"⚠️ blanchisseur présumé",1260,{size:62,w:900,color:'#FF6B70'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);svg.style.opacity=oQ(P(t,.05,.4));
    sw.setAttribute('transform',`rotate(${t*220} ${cx} ${cy})`);const ka=kTa(k,1),kb=kTb(k,ka+.8),red=t>=kb;
    const on=P(t,ka,.2);bp.setAttribute('opacity',on);bp.setAttribute('fill',red?TK.red:TK.gold2);
    const rp=((t-ka)%1+1)%1;ring.setAttribute('r',22+rp*90);ring.setAttribute('opacity',on*(1-rp));ring.setAttribute('stroke',red?TK.red:TK.gold2);
    if(!tag.dataset.fit){const w=tag.offsetWidth;if(cx+90+w>1020)tag.style.left=`${Math.max(60,1020-w)}px`;tag.dataset.fit=1}
    blurIn(tag,t,ka+.15,.35);S(tag,{borderColor:red?TK.red:TK.gold2,background:red?'rgba(229,72,77,.25)':'rgba(255,255,255,.1)'});
    const v=oB(P(t,kb,.4),1.8);S(vd,{opacity:cl(P(t,kb,.15)),transform:`scale(${.6+.4*v})`})};};

// CONTRAT — la convention qui protège : clauses cochées une à une (textes : title, doc, clauses[] ; clé : a = 1re coche)
B.contrat=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"La littérature qu'il faut",250,{size:70,w:800,color:TK.ink});
  const doc=$(`<div class="abs" style="left:110px;top:400px;width:860px;height:900px;background:#fff;border-radius:14px;box-shadow:0 40px 90px rgba(20,30,60,.2);padding:54px 56px;color:#1C2236">
     <div style="text-align:center;font-family:Georgia,serif;font-weight:700;font-size:40px;line-height:1.25;letter-spacing:.04em">${esc(X.doc??"CONVENTION DE COMPTE<br>COURANT D'ASSOCIÉ")}</div>
     <div style="height:3px;background:${TK.gold};margin:26px 160px 40px"></div></div>`);st.appendChild(doc);
  const cl_=(X.clauses||["Montant apporté","Origine des fonds","Durée et remboursement","Intérêts éventuels","Signature des associés"]).map(c=>{
    const e=$(`<div style="display:flex;align-items:center;gap:26px;margin-bottom:30px"><div class="bx" style="width:70px;height:70px;flex:none;border-radius:14px;border:4px solid #C9CDD8;display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:900;color:#fff"></div>
      <div style="font-size:42px;font-weight:700">${esc(c)}</div></div>`);doc.appendChild(e);return e});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const e=oQ(P(t,.1,.5));S(doc,{opacity:e,transform:`translateY(${(1-e)*200}px) rotate(${(1-e)*3}deg)`});
    const ka=kTa(k,.8);cl_.forEach((c,i)=>{const a=ka+i*.32;c.style.opacity=.35+.65*oC(P(t,.4+i*.1,.3));const bx=c.querySelector('.bx');const on=t>=a;
      bx.textContent=on?'✓':'';S(bx,{background:on?TK.green:'transparent',borderColor:on?TK.green:'#C9CDD8',transform:`scale(${on?oB(P(t,a,.3),2):1})`})})};};

// ---------------------------------------------------------------- phrases plein écran (couvrir un regard) — en rotation avec « citation »
// SURLIGNE — fond papier, mots en bleu nuit, mots-clés surlignés au feutre doré (clé : words)
B.surligne=(sc)=>{const {el,st}=vstage('light');
  const wrap=$(`<div class="abs" style="left:70px;right:70px;top:520px;text-align:center;font-weight:800;font-size:92px;line-height:1.22;color:${TK.ink};letter-spacing:-.015em"></div>`);st.appendChild(wrap);
  const ws=sc.keys.words.map(x=>{const s=$(`<span style="display:inline-block;position:relative;margin:0 .12em;z-index:1">${x[0]}</span>`);
    if(x[2]==='gold'){const m=$(`<span class="abs" style="left:-6px;right:-6px;bottom:6px;height:44%;background:#FFD98A;border-radius:6px;z-index:-1;transform-origin:0 50%"></span>`);s.appendChild(m);s._m=m}
    wrap.appendChild(s);return s});
  return (t,D,k)=>{sceneFx(el,t,D);ws.forEach((s,i)=>{const t0=Math.max(.08,k.words[i][1]-.05);blurIn(s,t,t0,.35,24);if(s._m)s._m.style.transform=`scaleX(${oC(P(t,t0+.2,.35))})`})};};

// CINÉTIQUE — fond bleu nuit quadrillé, un mot à la fois en grand, les précédents s'estompent (clé : words)
B.cinetique=(sc)=>{const {el,st}=vstage('navy');
  st.appendChild($(`<div class="abs" style="inset:0;background-image:linear-gradient(rgba(140,170,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(140,170,255,.07) 1px,transparent 1px);background-size:72px 72px"></div>`));
  const wrap=$(`<div class="abs" style="left:60px;right:60px;top:460px;text-align:left;font-weight:900;font-size:110px;line-height:1.05;text-transform:uppercase;letter-spacing:-.02em"></div>`);st.appendChild(wrap);
  const ws=sc.keys.words.map(x=>{const s=$(`<span style="display:inline-block;margin:0 .22em .1em 0" class="${x[2]==='gold'?'goldg':''}">${x[0]}</span>`);wrap.appendChild(s);return s});
  return (t,D,k)=>{sceneFx(el,t,D);let last=-1;ws.forEach((s,i)=>{if(t>=Math.max(.05,k.words[i][1]-.05))last=i});
    ws.forEach((s,i)=>{const t0=Math.max(.05,k.words[i][1]-.05);const e=oB(P(t,t0,.3),1.8);
      S(s,{opacity:t<t0?0:(i===last?1:.42),transform:`scale(${.6+.4*e})`,transformOrigin:'0 80%',textShadow:i===last?'0 0 30px rgba(255,217,138,.35)':'none'})})};};

// WHATSAPP — garder une trace : conversation qui confirme le paiement (textes : title, contact, bulles[[côté 'moi'|'lui', texte]], after ; clé : b = after)
B.whatsapp=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const t1=vt(st,X.title??"Garde une trace",250,{size:72,w:800});
  const ph=$(`<div class="abs" style="left:190px;top:390px;width:700px;height:860px;border-radius:60px;background:#0B141A;border:12px solid #2B3350;overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,.6)">
    <div style="height:120px;background:#1F2C34;display:flex;align-items:center;gap:20px;padding:0 30px">
      <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#F3D77E,#C99A2E);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:34px;color:${TK.navy}">${esc((X.contact||'K')[0])}</div>
      <div><div style="color:#E9EDEF;font-weight:700;font-size:34px">${esc(X.contact??'Kouassi (fournisseur)')}</div><div style="color:#8696A0;font-size:24px">en ligne</div></div></div>
    <div class="msgs" style="padding:30px 26px;display:flex;flex-direction:column;gap:20px"></div></div>`);st.appendChild(ph);
  const box=ph.querySelector('.msgs');
  const B_=(X.bulles||[["moi","Je t'envoie les 250 000 F pour la commande 📦"],["lui","Bien reçu, merci 🙏🏿"],["moi","📸 Photo du colis livré"],["lui","✅ Livraison confirmée"]]).map(([who,txt],i)=>{
    const me=who==='moi';const b=$(`<div style="align-self:${me?'flex-end':'flex-start'};max-width:78%;padding:16px 22px 12px;border-radius:22px;${me?'border-top-right-radius:6px;background:#005C4B':'border-top-left-radius:6px;background:#202C33'};color:#E9EDEF;font-size:32px;line-height:1.3">${esc(txt)}<div style="text-align:right;font-size:20px;color:#8FB3A9;margin-top:4px">14:0${2+i} ${me?'<span style="color:#53BDEB">✓✓</span>':''}</div></div>`);box.appendChild(b);return b});
  const af=vt(st,X.after??"Une preuve, ça peut être <span class='itgold'>tout ça</span>.",1270,{size:56,w:700});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const p=oQ(P(t,.1,.5));S(ph,{opacity:p,transform:`translateY(${(1-p)*160}px)`});
    const gap=Math.max(.35,Math.min(.8,(D-1.8)/B_.length));B_.forEach((b,i)=>{const e=oB(P(t,.5+i*gap,.35),1.6);S(b,{opacity:cl(P(t,.5+i*gap,.15)),transform:`scale(${.7+.3*e})`,transformOrigin:i%2?'0 0':'100% 0'})});
    blurIn(af,t,kTb(k,.6+B_.length*gap),.45)};};

// JUMEAUX — même visage, mais chacun son argent (textes : title, left, right, after ; clé : a = séparation)
B.jumeaux=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('navy');
  const t1=vt(st,X.title??"Jumeaux… mais pas le même argent",250,{size:62,w:700});
  const man=(x)=>{const g=$(`<div class="abs" style="left:${x}px;top:470px;width:330px;text-align:center">
     <svg width="330" height="420" viewBox="0 0 330 420"><circle cx="165" cy="95" r="80" fill="url(#gGold)"/><path d="M25 410 C 25 250, 85 190, 165 190 C 245 190, 305 250, 305 410 Z" fill="url(#gGold)"/></svg>
     <div class="w" style="margin:18px auto 0;width:250px;height:150px;border-radius:22px;background:linear-gradient(160deg,#6B4A22,#3D2913);border:4px solid #C99A2E;display:flex;align-items:center;justify-content:center;color:${TK.gold2};font-weight:900;font-size:96px">💰</div></div>`);st.appendChild(g);return g};
  const L=man(110),R=man(640);
  const lL=vt(st,X.left??"son argent",1135,{size:40,w:800,color:TK.gold2});S(lL,{left:'110px',right:'auto',width:'330px',padding:0});
  const lR=vt(st,X.right??"ton argent",1135,{size:40,w:800,color:TK.gold2});S(lR,{left:'640px',right:'auto',width:'330px',padding:0});
  const wall=$(`<div class="abs" style="left:520px;top:440px;width:40px;height:760px;border-radius:20px;background:linear-gradient(180deg,${TK.red},#9E1F25);box-shadow:0 0 40px rgba(229,72,77,.6);transform-origin:50% 0"></div>`);st.appendChild(wall);
  const ne=$(`<div class="abs" style="left:465px;top:740px;width:150px;height:150px;border-radius:50%;background:#fff;color:${TK.red};font-weight:900;font-size:110px;line-height:140px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.5)">≠</div>`);st.appendChild(ne);
  const af=vt(st,X.after??"Chacun ses problèmes.",1250,{size:66,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const a=oQ(P(t,.15,.5));
    S(L,{opacity:a,transform:`translateX(${(1-a)*200}px)`});S(R,{opacity:a,transform:`translateX(${(1-a)*-200}px)`});blurIn(lL,t,.5,.4);blurIn(lR,t,.6,.4);
    const ka=kTa(k,1.2);S(wall,{opacity:t>=ka?1:0,transform:`scaleY(${oQ(P(t,ka,.4))})`});pop(ne,t,ka+.3,.4);
    const pushApart=oQ(P(t,ka,.5))*30;L.style.marginLeft=`${-pushApart}px`;R.style.marginLeft=`${pushApart}px`;blurIn(af,t,kTb(k,ka+.8),.45)};};

// BULLETIN — se fixer un salaire : bulletin de paie du gérant validé (textes : title, head, sub, rows[[l,v]], net_label, net, stamp ; clé : a = tampon)
B.bulletin=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"Fixe-toi un <span class='itgold'>salaire</span>",250,{size:74,w:800,color:TK.ink});
  const doc=$(`<div class="abs" style="left:120px;top:400px;width:840px;height:840px;background:#fff;border-radius:14px;box-shadow:0 40px 90px rgba(20,30,60,.2);padding:50px 56px;color:#1C2236">
     <div style="display:flex;justify-content:space-between;align-items:center"><div style="font-weight:900;font-size:40px;letter-spacing:.08em">${esc(X.head??'BULLETIN DE SALAIRE')}</div>${seal(90)}</div>
     <div style="font-size:30px;color:#7A8499;margin:6px 0 30px">${esc(X.sub??'Fonction : Gérant · Octobre 2026')}</div><div class="rows"></div>
     <div class="net" style="margin-top:26px;padding:24px 28px;border-radius:14px;background:#FFF5DA;border:3px solid ${TK.gold};display:flex;justify-content:space-between;align-items:center">
       <span style="font-size:34px;font-weight:700">${esc(X.net_label??'NET À PAYER')}</span><b style="font-size:58px">${esc(X.net??'500 000 F')}</b></div></div>`);st.appendChild(doc);
  const rows=(X.rows||[["Salaire de base","fixé par les associés"],["Versé","chaque fin de mois"],["Pièce","procès-verbal d'AG"]]).map(([l,v])=>{const e=$(`<div style="display:flex;justify-content:space-between;font-size:36px;padding:18px 0;border-bottom:2px dashed #E3E6EE"><span style="color:#7A8499">${esc(l)}</span><b>${esc(v)}</b></div>`);doc.querySelector('.rows').appendChild(e);return e});
  const net=doc.querySelector('.net');
  const stp=stamp(st,X.stamp??"SALAIRE FIXÉ",{x:600,y:1130,size:60,rot:-10,color:TK.green});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const e=oQ(P(t,.1,.5));S(doc,{opacity:e,transform:`translateY(${(1-e)*220}px) rotate(${(1-e)*-3}deg)`});
    rows.forEach((r,i)=>{r.style.opacity=oC(P(t,.5+i*.25,.3))});net.style.opacity=oC(P(t,1.2,.3));stp(t,kTa(k,1.8))};};

// CAISSE — on puise dans la caisse de l'entreprise : le coffre s'ouvre, les billets s'envolent, puis « INTERDIT »
// (textes : title, label, after, stamp ; clés : a = ouverture, b = tampon)
B.caisse=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('dark');
  const t1=vt(st,X.title??"La caisse de l'entreprise…",250,{size:66,w:700});
  const safe=$(`<div class="abs" style="left:240px;top:470px;width:600px;height:600px;border-radius:40px;background:linear-gradient(160deg,#2A3A6E,#141E3D);border:10px solid #3B4C80;box-shadow:0 50px 100px rgba(0,0,0,.6)">
     <div class="abs" style="left:40px;top:40px;right:40px;bottom:40px;border-radius:24px;background:radial-gradient(circle at 50% 50%,#FFE7A8 0%,#E8B64A 40%,#6B4E0E 100%)"></div>
     <div class="door abs" style="left:30px;top:30px;right:30px;bottom:30px;border-radius:26px;background:linear-gradient(160deg,#33467F,#1A2650);border:6px solid #4A5C94;transform-origin:0 50%;display:flex;align-items:center;justify-content:center">
       <div style="width:200px;height:200px;border-radius:50%;border:14px solid ${TK.gold};background:#101830;display:flex;align-items:center;justify-content:center;color:${TK.gold2};font-weight:900;font-size:34px">${esc(X.label??'CAISSE')}</div></div></div>`);st.appendChild(safe);
  const door=safe.querySelector('.door');
  const notes=[...Array(10)].map((_,i)=>{const n=$(`<div class="abs" style="left:440px;top:700px;width:200px;height:96px;border-radius:8px;background:linear-gradient(135deg,#9BD3A8,#3E8E5A);border:3px solid #2C6B42;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:32px;color:#14391F;opacity:0">10 000 F</div>`);st.appendChild(n);return n});
  const stp=stamp(st,X.stamp??"INTERDIT",{x:540,y:770,size:110,rot:-12});
  const af=vt(st,X.after??"…n'est pas ta tirelire.",1200,{size:70,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const p=oQ(P(t,.05,.45));S(safe,{opacity:p,transform:`scale(${.85+.15*p})`});
    const ka=kTa(k,.8),o=iO(P(t,ka,.5));S(door,{transform:`perspective(1500px) rotateY(${-o*95}deg)`});
    notes.forEach((n,i)=>{const s=ka+.3+i*.12,u=P(t,s,1.1);if(u<=0){n.style.opacity=0;return}const a=(i%2?1:-1)*(0.3+R(i)*0.9);
      S(n,{opacity:1-P(t,s+.8,.3),transform:`translate(${Math.sin(a)*u*520}px,${-u*560+u*u*120}px) rotate(${a*u*240}deg)`})});
    stp(t,kTb(k,ka+1.6));blurIn(af,t,kTb(k,ka+1.6)+.3,.45)};};

// MAISON — loyer déclaré vs valeur locative, puis le voisin (textes : title, loyer, valeur, voisin ; clés : a = valeur locative, b = voisin)
B.maison=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"Ce que le fisc regarde",240,{size:68,w:800,color:TK.ink});
  const house=(x,y,s,col)=>{const h=$(`<svg class="abs" width="${360*s}" height="${330*s}" viewBox="0 0 360 330" style="left:${x}px;top:${y}px;overflow:visible">
     <path d="M20 150 L180 20 L340 150 Z" fill="${col}"/><rect x="50" y="145" width="260" height="175" rx="8" fill="#fff" stroke="${col}" stroke-width="8"/>
     <rect x="80" y="180" width="60" height="55" rx="6" fill="#CFE3F5" stroke="${col}" stroke-width="5"/><rect x="220" y="180" width="60" height="55" rx="6" fill="#CFE3F5" stroke="${col}" stroke-width="5"/>
     <rect x="150" y="235" width="60" height="85" rx="6" fill="${col}"/></svg>`);st.appendChild(h);return h};
  const H1=house(110,420,1.0,TK.navy), H2=house(610,420,1.0,'#8A93A8');
  const tag=(x,y,txt,bg,fg)=>{const e=$(`<div class="abs" style="left:${x}px;top:${y}px;padding:14px 26px;border-radius:16px;background:${bg};color:${fg};font-weight:900;font-size:40px;white-space:nowrap;box-shadow:0 14px 30px rgba(20,30,60,.18)">${txt}</div>`);st.appendChild(e);return e};
  const lab1=vt(st,X.toi??"ta maison",790,{size:34,w:700,color:TK.mute});S(lab1,{left:'110px',right:'auto',width:'360px',padding:0});
  const lab2=vt(st,X.voisin_lab??"le voisin (même maison)",790,{size:34,w:700,color:TK.mute});S(lab2,{left:'610px',right:'auto',width:'360px',padding:0});
  const tL=tag(130,860,`Loyer : ${esc(X.loyer??'20 000 F')}`,'#EEF0F5',TK.ink);
  const strike=$(`<div class="abs" style="left:120px;top:893px;height:7px;width:0;background:${TK.red};border-radius:4px;transform:rotate(-6deg)"></div>`);st.appendChild(strike);
  const tV=tag(110,960,`Valeur locative : ${esc(X.valeur??'100 000 F')}`,`linear-gradient(180deg,#F3D77E,#C99A2E)`,TK.navy);
  const tN=tag(640,860,`Loyer : ${esc(X.voisin??'200 000 F')}`,TK.navy,TK.gold2);
  const af=vt(st,X.after??"Le fisc compare. <span class='itgold'>Pas ton accord.</span>",1170,{size:58,w:800,color:TK.ink});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);const a=oB(P(t,.15,.5),1.3);S(H1,{opacity:cl(P(t,.15,.2)),transform:`translateY(${(1-a)*-120}px)`});blurIn(lab1,t,.4,.3);
    pop(tL,t,.6,.4);const ka=kTa(k,1.6),kb=kTb(k,ka+1.6);strike.style.width=`${oC(P(t,ka,.3))*360}px`;pop(tV,t,ka+.25,.45);
    const b=oB(P(t,kb,.5),1.3);S(H2,{opacity:cl(P(t,kb,.2)),transform:`translateY(${(1-b)*-120}px)`});blurIn(lab2,t,kb+.2,.3);pop(tN,t,kb+.4,.45);blurIn(af,t,kb+1,.45)};};

// VIREMENT — appli bancaire : 10 000 000 F partent du compte de la SOCIÉTÉ vers « Bébé », puis « avec quel argent ? »
// (textes : title, compte, benef, motif, montant, q, opt1, opt2 ; clés : a = alerte, b = croix sur l'option 1)
B.virement=(sc)=>{const X=sc.texts||{};const {el,st}=vstage('light');
  const t1=vt(st,X.title??"« Allô, mon gestionnaire… »",200,{size:64,w:800,color:TK.ink});
  const app=$(`<div class="abs" style="left:150px;top:330px;width:780px;height:900px;border-radius:56px;background:#fff;box-shadow:0 40px 100px rgba(20,30,60,.22);overflow:hidden;color:#1C2236">
     <div style="background:linear-gradient(135deg,#0F6E52,#0B4F3B);color:#fff;padding:38px 46px 30px"><div style="font-size:26px;letter-spacing:.2em;opacity:.8;font-weight:700">MA BANQUE</div>
       <div style="font-size:52px;font-weight:800;margin-top:6px">Virement</div></div>
     <div class="rows" style="padding:20px 46px 0"></div>
     <div class="amt" style="margin:18px 46px 0;padding:26px 30px;border-radius:24px;background:#F3F6F4;text-align:center"><div style="font-size:26px;color:#7A8499;font-weight:700;letter-spacing:.12em">MONTANT</div>
       <div style="font-size:82px;font-weight:900;color:#0B4F3B;line-height:1.1">${esc(X.montant??'10 000 000 F')}</div></div>
     <div class="btn" style="margin:26px 46px 0;padding:26px 0;border-radius:22px;background:#0F6E52;color:#fff;text-align:center;font-size:40px;font-weight:800">Confirmer le virement</div></div>`);st.appendChild(app);
  const rows=[["Compte débité",X.compte??"SOCIÉTÉ — compte pro"],["Bénéficiaire",X.benef??"« Bébé » 💕"],["Motif",X.motif??"décanter la situation"]].map(([l,v],i)=>{
    const e=$(`<div style="display:flex;justify-content:space-between;align-items:center;padding:24px 0;border-bottom:2px solid #EEF1F4;font-size:36px"><span style="color:#7A8499">${esc(l)}</span><b ${i===0?'class="cpt"':''} style="border-radius:12px;padding:4px 10px">${esc(v)}</b></div>`);
    app.querySelector('.rows').appendChild(e);return e});
  const cpt=app.querySelector('.cpt'),btn=app.querySelector('.btn');
  const veil=$(`<div class="abs" style="inset:0;background:rgba(10,16,34,.55)"></div>`);st.appendChild(veil);
  const card=$(`<div class="abs" style="left:110px;top:640px;width:860px;padding:44px 40px 40px;border-radius:40px;background:#fff;box-shadow:0 40px 100px rgba(0,0,0,.4);text-align:center;color:#1C2236">
     <div style="font-size:84px;line-height:1">⚠️</div><div style="font-size:66px;font-weight:900;margin:14px 0 30px">${esc(X.q??'Avec quel argent ?')}</div>
     <div style="display:flex;gap:24px;justify-content:center">
       <div class="o1" style="position:relative;flex:1;padding:26px 10px;border-radius:24px;border:4px solid ${TK.red};font-size:36px;font-weight:800">${esc(X.opt1??"💼 L'argent de l'entreprise")}</div>
       <div class="o2" style="flex:1;padding:26px 10px;border-radius:24px;border:4px solid #C9D1DC;font-size:36px;font-weight:800">${esc(X.opt2??'👛 Ton propre argent')}</div></div></div>`);st.appendChild(card);
  const x=$(`<svg class="abs" width="400" height="160" viewBox="0 0 400 160" style="left:-6px;top:-10px;overflow:visible"><line x1="20" y1="20" x2="380" y2="140" stroke="${TK.red}" stroke-width="16" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/></svg>`);
  card.querySelector('.o1').appendChild(x);const ln=x.querySelector('line');
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.05,.4);
    const e=oQ(P(t,.1,.55));S(app,{opacity:e,transform:`translateY(${(1-e)*260}px)`});
    rows.forEach((r,i)=>{r.style.opacity=oC(P(t,.45+i*.25,.3))});
    const hl=oC(P(t,1.4,.3));cpt.style.background=`rgba(229,72,77,${.16*hl})`;cpt.style.color=hl>.5?TK.red:'#1C2236';
    const ka=kTa(k,2.4);const pr=P(t,ka-.5,.25);S(btn,{transform:`scale(${1-.06*Math.sin(Math.PI*pr)})`});
    veil.style.opacity=oC(P(t,ka,.3));const c=oB(P(t,ka,.5),1.4);S(card,{opacity:cl(P(t,ka,.2)),transform:`scale(${.6+.4*c})`});
    draw(ln,t,kTb(k,ka+1.4),.3)};};
