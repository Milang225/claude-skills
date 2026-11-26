// ============================================================================
// SCÈNES CRÉATIVES — une métaphore visuelle par idée (chargé par scene_cinema.html)
// Toutes dessinées sur une « scène » de 1920×1080 (mise à l'échelle en vertical).
// Textes : sc.texts ; instants clés : sc.keys.a / sc.keys.b (relatifs au début de la scène).
// ============================================================================
function stage(kind){
  const el=$(`<div class="scene ${kind==='light'?'light':'dark'}"></div>`);root.appendChild(el);
  if(kind==='blue'){el.style.background='radial-gradient(120% 90% at 50% 38%,#1C2C58 0%,#0E1733 58%,#060B1A 100%)';
    el.appendChild($(`<div class="abs" style="inset:0;background-image:linear-gradient(rgba(140,170,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(140,170,255,.07) 1px,transparent 1px);background-size:64px 64px;-webkit-mask-image:radial-gradient(80% 70% at 50% 45%,#000 30%,transparent 90%)"></div>`))}
  if(kind==='dark'){el.appendChild($(`<div class="abs" style="inset:0;background:radial-gradient(90% 70% at 50% 40%,#16203C 0%,#070B18 70%,#04060C 100%)"></div>`))}
  const st=$(`<div class="abs" style="left:0;top:0;width:1920px;height:1080px;transform-origin:0 0"></div>`);
  const sc=V?Math.min(W/1920,(H*.6)/1080)*1.0:1, ox=V?(W-1920*sc)/2:0, oy=V?H*.15:0;
  S(st,{transform:`translate(${ox}px,${oy}px) scale(${sc})`});el.appendChild(st);
  el.appendChild($(`<div class="grain" style="opacity:${kind==='light'?.035:.06}"></div>`));
  return {el,st,light:kind==='light'};
}
function ttl(st,txt,y,{size=64,w=600,color,italic=false,gold=false,cls=''}={}){
  const e=$(`<div class="abs ${gold?'goldg':''} ${cls}" style="left:0;right:0;text-align:center;top:${y}px;font-size:${size}px;font-weight:${w};${italic?'font-style:italic;':''}${color?`color:${color};`:''}line-height:1.12;padding:0 90px">${esc(txt)}</div>`);
  st.appendChild(e);return e;
}
const kA=(k,d=.6)=>k.a??d, kB=(k,d=1.6)=>k.b??d;
const INK='#16213F';

// 1. LABYRINTHE — naviguer dans l'écosystème
B.boussole=(sc)=>{const X=sc.texts||{};const {el,st}=stage('blue');
  const tiles=X.tiles||["TVA","IBIC","Patente","ITS","CNPS","FDFP","Délais","IMF","Contrôles","Déclarations","Pénalités","Échéances"];
  const cols=6,rows=3,tw=210,th=110,gx=1920/2-(cols*tw+(cols-1)*40)/2,gy=300;
  const ts=tiles.slice(0,cols*rows).map((t,i)=>{const c=i%cols,r=Math.floor(i/cols);
    const d=$(`<div class="abs" style="left:${gx+c*(tw+40)}px;top:${gy+r*(th+50)}px;width:${tw}px;height:${th}px;border-radius:16px;border:1.5px solid rgba(160,190,255,.35);background:rgba(40,60,110,.35);display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:600;color:#D8E2FF">${t}</div>`);st.appendChild(d);return d});
  const pts=[[gx-120,gy+th+25]];for(let c=0;c<=cols;c++){const x=gx+c*(tw+40)-20;pts.push([x,gy+((c%2)?-25:th*3+2*50+25)]);pts.push([x,gy+th+25+((c%2)?0:th+50)])}
  pts.push([gx+cols*(tw+40)+120,gy+th+25]);
  const d="M"+pts.map(p=>p.join(' ')).join(" L");
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0;overflow:visible"><path d="${d}" fill="none" stroke="#F3D77E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" filter="url(#soft)" opacity=".5"/><path d="${d}" fill="none" stroke="#FFE7A8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"/><circle class="dot" r="14" fill="#FFF1C9"/></svg>`);st.appendChild(svg);
  const pa=svg.querySelectorAll('path'),dot=svg.querySelector('.dot');let L=0;
  const t1=ttl(st,X.title??"naviguer dans l'écosystème",110,{size:66,w:300});
  return (t,D,k,T)=>{sceneFx(el,t,D);blurIn(t1,t,.1,.5);
    ts.forEach((d,i)=>blurIn(d,t,.2+i*.04,.4,14));
    if(!L)L=pa[1].getTotalLength();const e=iO(P(t,kA(k,.8),Math.max(1.2,D-kA(k,.8)-.4)));
    pa.forEach(p=>p.style.strokeDashoffset=1-e);const pt=pa[1].getPointAtLength(L*e);dot.setAttribute('cx',pt.x);dot.setAttribute('cy',pt.y);dot.setAttribute('opacity',e>0?1:0);
    ts.forEach((d,i)=>{const r=d.getBoundingClientRect();const near=Math.abs(pt.x-(parseFloat(d.style.left)+tw/2))<160&&Math.abs(pt.y-(parseFloat(d.style.top)+th/2))<150;d.style.borderColor=near?'rgba(243,215,126,.9)':'rgba(160,190,255,.35)';d.style.boxShadow=near?'0 0 30px rgba(243,215,126,.35)':'none'})};};

// 2. BALANCE — elles paient plus… et s'en sortent
B.balance=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const svg=$(`<svg class="abs" width="1200" height="620" viewBox="-600 -120 1200 620" style="left:360px;top:190px;overflow:visible">
   <path d="M-40 470 L40 470 L10 60 L-10 60 Z" fill="url(#gGold)"/><circle cx="0" cy="50" r="22" fill="url(#gGold)"/>
   <g class="beam"><rect x="-430" y="40" width="860" height="16" rx="8" fill="url(#gGold)"/>
     <g class="pl"><line x1="-400" y1="48" x2="-470" y2="260" stroke="#C69B2E" stroke-width="3"/><line x1="-400" y1="48" x2="-330" y2="260" stroke="#C69B2E" stroke-width="3"/><path d="M-500 260 Q-400 320 -300 260 Z" fill="url(#gGold)"/>
       ${[0,1,2,3,4,5].map(i=>`<ellipse class="cn" cx="-400" cy="${248-i*18}" rx="58" ry="14" fill="#E9C766" stroke="#9A7518" stroke-width="2"/>`).join('')}</g>
     <g class="pr"><line x1="400" y1="48" x2="330" y2="260" stroke="#C69B2E" stroke-width="3"/><line x1="400" y1="48" x2="470" y2="260" stroke="#C69B2E" stroke-width="3"/><path d="M300 260 Q400 320 500 260 Z" fill="url(#gGold)"/>
       <ellipse cx="400" cy="248" rx="58" ry="14" fill="#E9C766" stroke="#9A7518" stroke-width="2"/></g></g></svg>`);st.appendChild(svg);
  const lL=ttl(st,X.left??"elles",0,{size:40,w:700});S(lL,{left:'330px',right:'auto',width:'440px',top:'640px'});
  const lR=ttl(st,X.right??"nous autres",0,{size:40,w:400,color:'rgba(255,255,255,.7)'});S(lR,{left:'1150px',right:'auto',width:'440px',top:'640px'});
  const t1=ttl(st,X.title??"elles paient beaucoup plus…",90,{size:60,w:300});
  const t2=ttl(st,X.after??"…et elles font fortune.",760,{size:64,w:800,gold:true});
  const beam=svg.querySelector('.beam'),pl=svg.querySelector('.pl'),pr=svg.querySelector('.pr'),cns=[...svg.querySelectorAll('.cn')];
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1,.5);blurIn(lL,t,.5);blurIn(lR,t,.6);
    cns.forEach((c,i)=>c.setAttribute('opacity',t>.5+i*.12?1:0));
    const a=-10*iO(P(t,.5,1.2))*(1-.6*iO(P(t,kB(k,2.2),.8)));beam.setAttribute('transform',`rotate(${a})`);
    pl.setAttribute('transform',`rotate(${-a} -400 48)`);pr.setAttribute('transform',`rotate(${-a} 400 48)`);blurIn(t2,t,kB(k,2.2),.5)};};

// 3. BOUCLE — on sera toujours dans cette même boucle
B.boucle=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const R0=250,cx=960,cy=440;const labs=X.labels||["se plaindre","payer","se plaindre encore"];
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0;overflow:visible"><g class="rot" style="transform-origin:${cx}px ${cy}px">
    <circle cx="${cx}" cy="${cy}" r="${R0}" fill="none" stroke="rgba(243,215,126,.18)" stroke-width="26"/>
    <path d="M${cx+R0} ${cy} A${R0} ${R0} 0 1 1 ${cx+R0*Math.cos(-.5)} ${cy+R0*Math.sin(-.5)}" fill="none" stroke="#F3D77E" stroke-width="10" stroke-linecap="round" filter="url(#soft)" opacity=".6"/>
    <path d="M${cx+R0} ${cy} A${R0} ${R0} 0 1 1 ${cx+R0*Math.cos(-.5)} ${cy+R0*Math.sin(-.5)}" fill="none" stroke="#FFE7A8" stroke-width="6" stroke-linecap="round"/>
    <path d="M${cx+R0*Math.cos(-.5)-30} ${cy+R0*Math.sin(-.5)-10} l 40 -2 l -14 38 z" fill="#FFE7A8"/></g></svg>`);st.appendChild(svg);
  const ls=labs.map((l,i)=>{const a=-Math.PI/2+i*2*Math.PI/labs.length;const e=$(`<div class="abs" style="left:${cx+Math.cos(a)*(R0+150)-200}px;top:${cy+Math.sin(a)*(R0+95)-30}px;width:400px;text-align:center;font-size:40px;font-weight:600;color:#fff">${esc(l)}</div>`);st.appendChild(e);return e});
  const c=ttl(st,X.center??"la même<br>boucle",cy-60,{size:62,w:800,gold:true});
  const rot=svg.querySelector('.rot');
  return (t,D,k)=>{sceneFx(el,t,D);rot.style.transform=`rotate(${t*140}deg)`;ls.forEach((e,i)=>blurIn(e,t,.3+i*.35,.4));blurIn(c,t,kA(k,1.3),.5)};};

// 4. AILLEURS — le problème est ailleurs (loupe qui quitte le terrain connu)
B.ailleurs=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const words=X.pills||["taux","impôts","contrôles","pénalités","l'administration","les lois","la TVA","les délais"];
  const ps=words.map((w,i)=>{const x=180+(i%4)*300+(Math.floor(i/4)%2)*120,y=330+Math.floor(i/4)*180;const e=$(`<div class="abs" style="left:${x}px;top:${y}px;padding:12px 26px;border-radius:40px;background:#fff;border:1.5px solid #D5D9E4;color:#7A8499;font-size:32px;font-weight:600;box-shadow:0 8px 20px rgba(20,30,60,.08)">${w}</div>`);st.appendChild(e);return e});
  const mag=$(`<svg class="abs" width="260" height="260" viewBox="0 0 260 260" style="left:0;top:0;overflow:visible"><circle cx="110" cy="110" r="84" fill="rgba(255,255,255,.35)" stroke="${INK}" stroke-width="14"/><line x1="172" y1="172" x2="240" y2="240" stroke="${INK}" stroke-width="22" stroke-linecap="round"/></svg>`);st.appendChild(mag);
  const t1=ttl(st,X.title??"le problème n'est pas là…",120,{size:58,w:300,color:INK});
  const big=$(`<div class="abs itgold" style="left:1300px;top:560px;font-size:120px">${esc(X.big??'ailleurs.')}</div>`);st.appendChild(big);
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);ps.forEach((p,i)=>blurIn(p,t,.15+i*.05,.4,10));
    const a=kA(k,1.5);const path=[[260,300],[900,330],[480,500],[1100,520],[1450,380]];
    const u=P(t,.3,a+.4)*(path.length-2);const i0=Math.min(path.length-2,Math.floor(u)),f=iO(u-i0);
    let [x,y]=[lerp(path[i0][0],path[i0+1][0],f),lerp(path[i0][1],path[i0+1][1],f)];
    const out=iO(P(t,a+.4,.7));x=lerp(x,1020,out);y=lerp(y,330,out);S(mag,{transform:`translate(${x}px,${y}px)`});
    ps.forEach(p=>p.style.opacity=Math.min(+p.style.opacity||0,1-.6*out));blurIn(big,t,a+.8,.6,20)};};

// 5. RESPIRE — l'administration n'est pas là pour nous étouffer
B.respire=(sc)=>{const X=sc.texts||{};const {el,st}=stage('blue');
  const rings=[0,1,2,3,4].map(i=>{const r=$(`<div class="abs" style="left:960px;top:470px;width:10px;height:10px;border-radius:50%;border:2px solid rgba(243,215,126,.5)"></div>`);st.appendChild(r);return r});
  const l1=ttl(st,X.line1??"l'administration n'est pas là",330,{size:58,w:300});
  const l2=$(`<div class="abs" style="left:0;right:0;text-align:center;top:430px;font-size:96px;font-weight:800"><span class="w" style="position:relative;display:inline-block">${esc(X.strike??'pour nous étouffer')}<span class="bar" style="position:absolute;left:0;top:52%;height:8px;background:#FF6B5E;border-radius:4px;box-shadow:0 0 14px rgba(255,90,70,.8);width:0"></span></span></div>`);st.appendChild(l2);
  const l3=ttl(st,X.after??"",600,{size:64,w:700,gold:true});
  return (t,D,k)=>{sceneFx(el,t,D);rings.forEach((r,i)=>{const p=((t*.45+i/5)%1);const s=60+p*900;S(r,{width:px(s),height:px(s),marginLeft:px(-s/2),marginTop:px(-s/2),opacity:(1-p)*.7})});
    blurIn(l1,t,.15);blurIn(l2,t,.45,.5);l2.querySelector('.bar').style.width=(100*iO(P(t,kA(k,1.4),.45)))+'%';blurIn(l3,t,kA(k,1.4)+.4)};};

// 6. NUMÉRO — grand chiffre tracé (Question 1…)
B.numero=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const svg=$(`<svg class="abs" width="700" height="700" viewBox="0 0 700 700" style="left:130px;top:150px;overflow:visible"><text x="350" y="600" text-anchor="middle" font-family="Didot, serif" font-weight="700" font-size="720" fill="none" stroke="#F3D77E" stroke-width="5" class="n" style="stroke-dasharray:3000;stroke-dashoffset:3000">${esc(X.n??'1')}</text>
   <text x="350" y="600" text-anchor="middle" font-family="Didot, serif" font-weight="700" font-size="720" fill="url(#gGoldV)" class="f" opacity="0">${esc(X.n??'1')}</text></svg>`);st.appendChild(svg);
  const k1=$(`<div class="abs" style="left:880px;top:330px;font-size:46px;font-weight:300;font-style:italic;color:rgba(255,255,255,.8)">${esc(X.kicker??'Question')}</div>`);
  const t1=$(`<div class="abs" style="left:880px;top:400px;width:980px;font-size:58px;font-weight:700;line-height:1.14;text-wrap:balance">${esc(X.title??'')}</div>`);st.append(k1,t1);
  return (t,D,k)=>{sceneFx(el,t,D);svg.querySelector('.n').style.strokeDashoffset=3000*(1-iO(P(t,.1,1.1)));svg.querySelector('.f').setAttribute('opacity',iO(P(t,.9,.6)));blurIn(k1,t,.4);blurIn(t1,t,.6,.6,20)};};

// 7. VAGUE — surfer dans l'écosystème
B.vague=(sc)=>{const X=sc.texts||{};const {el,st}=stage('blue');
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0"><path class="w1" fill="none" stroke="rgba(243,215,126,.35)" stroke-width="3"/><path class="w2" fill="none" stroke="rgba(243,215,126,.6)" stroke-width="4"/><path class="w3" fill="rgba(20,40,90,.55)" stroke="#F3D77E" stroke-width="6"/>
    <g class="board"><path d="M-70 0 Q0 -22 70 0 Q0 16 -70 0 Z" fill="url(#gGold)"/><circle cx="0" cy="-58" r="16" fill="#FFF1C9"/><path d="M0 -42 L0 -12 M0 -34 L-26 -18 M0 -34 L26 -26 M0 -12 L-18 0 M0 -12 L18 0" stroke="#FFF1C9" stroke-width="7" stroke-linecap="round"/></g></svg>`);st.appendChild(svg);
  const k1=ttl(st,X.kicker??'Question 2',120,{size:44,w:300,italic:true,color:'rgba(255,255,255,.8)'});
  const t1=ttl(st,X.title??'',190,{size:66,w:700});
  const wv=(y0,amp,ph,T)=>{let d=`M-20 ${y0}`;for(let x=-20;x<=1940;x+=24)d+=` L${x} ${y0+Math.sin(x/170+T*1.6+ph)*amp+Math.sin(x/61+T*2.3)*amp*.25}`;return d};
  return (t,D,k,T)=>{sceneFx(el,t,D);blurIn(k1,t,.1);blurIn(t1,t,.3,.6,20);const rise=oQ(P(t,0,.8));
    svg.querySelector('.w1').setAttribute('d',wv(760-rise*40,26,0,T));svg.querySelector('.w2').setAttribute('d',wv(720-rise*50,34,1.3,T));
    svg.querySelector('.w3').setAttribute('d',wv(680-rise*60,44,2.2,T)+' L1940 1100 L-20 1100 Z');
    const bx=300+t*(1320/Math.max(D,1)),by=680-rise*60+Math.sin(bx/170+T*1.6+2.2)*44-8,ang=Math.cos(bx/170+T*1.6+2.2)*14;
    svg.querySelector('.board').setAttribute('transform',`translate(${bx} ${by}) rotate(${ang}) scale(2)`);svg.querySelector('.board').setAttribute('opacity',P(t,.5,.3))};};

// 8. CLÉ — comprendre notre administration
B.cle=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const glow=$(`<div class="halo" style="left:960px;top:460px;width:10px;height:10px;background:radial-gradient(circle,rgba(255,240,200,1),rgba(243,215,126,.6) 30%,transparent 70%)"></div>`);st.appendChild(glow);
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0;overflow:visible"><rect x="820" y="300" width="280" height="340" rx="36" fill="url(#gGold)"/><rect x="836" y="316" width="248" height="308" rx="28" fill="#1B274A"/>
    <circle cx="960" cy="440" r="36" fill="#05070E"/><path d="M944 460 L976 460 L990 560 L930 560 Z" fill="#05070E"/>
    <g class="key"><circle cx="0" cy="0" r="46" fill="none" stroke="url(#gGold)" stroke-width="18"/><rect x="40" y="-9" width="240" height="18" rx="9" fill="url(#gGold)"/><rect x="220" y="9" width="18" height="40" fill="url(#gGold)"/><rect x="254" y="9" width="18" height="30" fill="url(#gGold)"/></g></svg>`);st.appendChild(svg);
  const k1=ttl(st,X.kicker??'Question 3 — la plus importante',120,{size:44,w:300,italic:true,color:'rgba(255,255,255,.8)'});
  const t1=ttl(st,X.title??'',700,{size:62,w:700});
  const key=svg.querySelector('.key');
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(k1,t,.1);const e=iO(P(t,.3,1));const turn=iO(P(t,1.35,.5));
    key.setAttribute('transform',`translate(${lerp(1700,960-280,e)} 470) rotate(${turn*-90} 280 0)`);
    const g=oQ(P(t,1.8,.8));const s=40+g*1400;S(glow,{width:px(s),height:px(s),marginLeft:px(-s/2),marginTop:px(-s/2),opacity:g*.9});blurIn(t1,t,1.9,.6,20)};};

// 9. RÉSEAU — un écosystème : ses règles, ses temps, ses interlocuteurs… puis les filiales
B.reseau=(sc)=>{const X=sc.texts||{};const {el,st}=stage('blue');
  const cx=960,cy=450;const n1=X.nodes||["ses règles","ses temps","ses interlocuteurs"],n2=X.branches||["succursales","filiales"];
  const pos1=n1.map((_,i)=>{const a=-Math.PI/2+i*2*Math.PI/n1.length;return [cx+Math.cos(a)*330,cy+Math.sin(a)*230]});
  const pos2=n2.map((_,i)=>[pos1[1][0]+160+i*40,pos1[1][1]+160-i*330]).map((p,i)=>[i?1560:1580,i?250:640]);
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0">${pos1.map((p,i)=>`<line class="e1" x1="${cx}" y1="${cy}" x2="${p[0]}" y2="${p[1]}" stroke="#F3D77E" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>`).join('')}
    ${pos2.map((p,i)=>`<line class="e2" x1="${pos1[1][0]}" y1="${pos1[1][1]}" x2="${p[0]}" y2="${p[1]}" stroke="rgba(243,215,126,.7)" stroke-width="2.5" stroke-dasharray="8 8" opacity="0"/>`).join('')}</svg>`);st.appendChild(svg);
  const node=(x,y,txt,big)=>{const e=$(`<div class="abs" style="left:${x}px;top:${y}px;transform:translate(-50%,-50%);padding:${big?'26px 40px':'16px 28px'};border-radius:999px;background:${big?'linear-gradient(135deg,#F3D77E,#C99A2E)':'rgba(30,50,100,.75)'};color:${big?'#131C38':'#fff'};border:1.5px solid rgba(243,215,126,.7);font-size:${big?46:34}px;font-weight:${big?800:600};white-space:nowrap;box-shadow:0 0 30px rgba(243,215,126,.25)">${esc(txt)}</div>`);st.appendChild(e);return e};
  const c=node(cx,cy,X.center??'écosystème',true);const a1=pos1.map((p,i)=>node(p[0],p[1],n1[i]));const a2=pos2.map((p,i)=>node(p[0],p[1],n2[i]));
  return (t,D,k)=>{sceneFx(el,t,D);popIn(c,t,.1,.5,'translate(-50%,-50%)');
    svg.querySelectorAll('.e1').forEach((l,i)=>l.style.strokeDashoffset=1-iO(P(t,.4+i*.3,.5)));a1.forEach((n,i)=>popIn(n,t,.7+i*.3,.45,'translate(-50%,-50%)'));
    const b=kB(k,2.6);svg.querySelectorAll('.e2').forEach((l,i)=>l.setAttribute('opacity',P(t,b+i*.25,.3)));a2.forEach((n,i)=>popIn(n,t,b+.1+i*.25,.45,'translate(-50%,-50%)'))};};
function popIn(el,t,t0,d=.5,base=''){const e=oB(P(t,t0,d));S(el,{opacity:cl(e*1.5),transform:`${base} scale(${Math.max(0,e)})`});return e}

// 10. BILLETS — ne me dites pas qu'elles ont de l'argent
B.billets=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const notes=[0,1,2,3,4,5,6].map(i=>{const e=$(`<div class="abs" style="left:${760+i*6}px;top:${360-i*14}px;width:400px;height:200px;border-radius:14px;background:linear-gradient(135deg,#E8F1E4,#BFD8B8);border:3px solid #5E8C5A;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:44px;color:#2F5B34;box-shadow:0 10px 20px rgba(20,40,20,.15);transform:rotate(${(i-3)*3}deg)">10 000 FCFA</div>`);st.appendChild(e);return e});
  const slash=$(`<svg class="abs" width="600" height="420" style="left:660px;top:240px;overflow:visible"><circle cx="300" cy="210" r="190" fill="none" stroke="#E5483C" stroke-width="18" pathLength="1" stroke-dasharray="1" class="c"/><line x1="165" y1="345" x2="435" y2="75" stroke="#E5483C" stroke-width="18" stroke-linecap="round" pathLength="1" stroke-dasharray="1" class="l"/></svg>`);st.appendChild(slash);
  const t1=ttl(st,X.title??"« elles ont de l'argent »",110,{size:58,w:400,italic:true,color:INK});
  const t2=ttl(st,X.after??"c'est bien plus que ça.",700,{size:76,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);notes.forEach((n,i)=>{const e=oC(P(t,.2+i*.07,.4));n.style.opacity=e;n.style.marginTop=px((1-e)*-80)});
    const a=kA(k,1.2);slash.querySelector('.c').style.strokeDashoffset=1-iO(P(t,a,.4));slash.querySelector('.l').style.strokeDashoffset=1-iO(P(t,a+.3,.25));blurIn(t2,t,kB(k,a+.8),.5)};};

// 11. ENVELOPPE — corruption, pots-de-vin : faut bouger
B.enveloppe_non=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const desk=$(`<div class="abs" style="left:0;right:0;top:620px;height:460px;background:linear-gradient(180deg,#3A2A1C,#1E150D);box-shadow:0 -10px 40px rgba(0,0,0,.6)"></div>`);st.appendChild(desk);
  const env=$(`<svg class="abs" width="420" height="260" viewBox="0 0 420 260" style="left:0;top:520px;overflow:visible"><rect width="420" height="260" rx="10" fill="#C9A15B"/><path d="M0 0 L210 150 L420 0" fill="none" stroke="#9C7A3C" stroke-width="6"/><text x="300" y="220" font-size="30" font-weight="800" fill="#7A5A24" font-family="Avenir Next">FCFA</text></svg>`);st.appendChild(env);
  const stamp=$(`<svg class="abs" width="420" height="420" style="left:750px;top:300px;overflow:visible"><circle cx="210" cy="210" r="180" fill="rgba(229,72,60,.12)" stroke="#E5483C" stroke-width="22"/><line x1="83" y1="337" x2="337" y2="83" stroke="#E5483C" stroke-width="22" stroke-linecap="round"/></svg>`);st.appendChild(stamp);
  const t1=ttl(st,X.title??"corruption ? pots-de-vin ?",110,{size:60,w:400,italic:true});
  const t2=ttl(st,X.after??"faut bouger.",210,{size:86,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);const e=oC(P(t,.3,.9));S(env,{transform:`translateX(${lerp(-460,750,e)}px) rotate(${(1-e)*-8}deg)`});
    const a=kA(k,1.4);const s=oC(P(t,a,.2));S(stamp,{opacity:t<a?0:1,transform:`scale(${2.2-1.2*s})`});blurIn(t2,t,kB(k,a+.4),.4)};};

// 12. FOULE — elle est à nous (des personnes qui forment le bâtiment)
B.foule=(sc)=>{const X=sc.texts||{};const {el,st}=stage('blue');
  const tg=[];const add=(x,y)=>tg.push([x,y]);
  for(let x=700;x<=1220;x+=26)add(x,300-Math.max(0,120-Math.abs(x-960)*.46));   // fronton
  for(let c=0;c<5;c++)for(let y=330;y<=620;y+=26)add(760+c*100,y);             // colonnes
  for(let x=680;x<=1240;x+=24){add(x,650);add(x,680)}                             // marches
  const ppl=tg.map((p,i)=>{const e=$(`<div class="abs" style="left:0;top:0;width:18px;height:18px;border-radius:50%;background:#F3D77E;box-shadow:0 0 8px rgba(243,215,126,.6)"></div>`);st.appendChild(e);return {e,p,s:[R(i+1)*1920,R(i+7)*1080]}});
  const t1=ttl(st,X.title??'notre administration',110,{size:56,w:300});
  const t2=ttl(st,X.after??'elle est à nous.',760,{size:80,w:800,gold:true});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);ppl.forEach(({e,p,s},i)=>{const f=iO(P(t,.2+R(i+3)*.5,1.3));S(e,{transform:`translate(${lerp(s[0],p[0],f)}px,${lerp(s[1],p[1],f)}px)`,opacity:.3+.7*f})});blurIn(t2,t,kA(k,1.8),.5)};};

// 13. DÉCODAGE — le jargon devient clair
B.decodage=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const jar=X.jargon??"Art. 18-3° : les charges visées à l'alinéa précédent ne sont admises en déduction que sous réserve…";
  const clair=X.clair??"En clair : ce que ça change pour vous.";
  const card=(x,title)=>{const e=$(`<div class="abs" style="left:${x}px;top:280px;width:700px;height:420px;border-radius:24px;background:#fff;border:1.5px solid #D5D9E4;box-shadow:0 20px 50px rgba(20,30,60,.10);padding:40px 44px;color:${INK}"><div style="font-size:24px;letter-spacing:.25em;text-transform:uppercase;color:#8B93A8;font-weight:700">${title}</div><div class="tx" style="margin-top:22px;font-size:40px;line-height:1.3;font-weight:600"></div></div>`);st.appendChild(e);return e};
  const a=card(160,X.label1??'le texte'),b=card(1060,X.label2??'la version claire');
  const arr=$(`<svg class="abs" width="140" height="60" style="left:890px;top:460px"><path d="M0 30 L110 30 M85 8 L112 30 L85 52" stroke="#C99A2E" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" class="p"/></svg>`);st.appendChild(arr);
  const t1=ttl(st,X.title??'',110,{size:60,w:700,color:INK});
  const glyph='§¶†‡#%&@*=+<>/\\|';
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);blurIn(a,t,.2,.5,20);blurIn(b,t,.5,.5,20);
    const n=Math.floor(jar.length*P(t,.3,.9));a.querySelector('.tx').style.fontFamily='Menlo, monospace';a.querySelector('.tx').style.fontSize='30px';
    a.querySelector('.tx').textContent=jar.slice(0,n);arr.querySelector('.p').style.strokeDashoffset=1-iO(P(t,kA(k,1.3),.4));
    const s=P(t,kA(k,1.3)+.3,1.1),m=Math.floor(clair.length*s);let out='';for(let i=0;i<clair.length;i++)out+=i<m?clair[i]:(i<m+6&&s>0?glyph[Math.floor(R(i+Math.floor(t*24))*glyph.length)]:' ');
    b.querySelector('.tx').textContent=out};};

// 14. PRIX — l'information, gratuitement
B.prix=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const tag=$(`<div class="abs" style="left:560px;top:260px;width:800px;height:380px;transform-origin:50% -120px"></div>`);st.appendChild(tag);
  tag.innerHTML=`<svg width="800" height="380" viewBox="0 0 800 380" style="position:absolute;overflow:visible"><line x1="400" y1="-120" x2="400" y2="40" stroke="#C99A2E" stroke-width="4"/><path d="M120 40 L680 40 L760 190 L680 340 L120 340 Q80 340 80 300 L80 80 Q80 40 120 40 Z" fill="url(#gGold)"/><circle cx="400" cy="70" r="16" fill="#131C38"/></svg><div class="v din" style="position:absolute;left:0;right:0;top:130px;text-align:center;font-family:'SF Pro Display',-apple-system;font-weight:900;font-size:130px;color:#131C38;letter-spacing:-.02em"></div>`;
  const t1=ttl(st,X.title??"l'information",90,{size:58,w:300});
  const t2=ttl(st,X.after??"gratuitement.",720,{size:84,w:800,cls:'itgold'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);const sw=Math.sin(t*3)*6*Math.exp(-t*.8);S(tag,{transform:`rotate(${sw}deg)`,opacity:P(t,.1,.3)});
    const p=iO(P(t,.4,Math.max(.6,kA(k,1.4)-.4)));const v=Math.round(25000*(1-p));tag.querySelector('.v').textContent=(v?v.toLocaleString('fr-FR'):'0')+' FCFA';blurIn(t2,t,kA(k,1.4),.5)};};

// 15. CALENDRIER — le jour de ton redressement
B.calendrier=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const cal=$(`<div class="abs" style="left:560px;top:190px;width:800px;height:560px;border-radius:26px;background:#fff;box-shadow:0 30px 60px rgba(20,30,60,.14);overflow:hidden"><div style="height:110px;background:#131C38;color:#F3D77E;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;letter-spacing:.2em">${esc(X.mois??'CONTRÔLE')}</div><div class="g" style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px;padding:26px"></div></div>`);st.appendChild(cal);
  const g=cal.querySelector('.g');const cells=[];for(let i=1;i<=28;i++){const c=$(`<div style="height:88px;border-radius:12px;background:#F2F3F7;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:600;color:#7A8499;position:relative">${i}</div>`);g.appendChild(c);cells.push(c)}
  const tgt=cells[X.jour?X.jour-1:17];tgt.innerHTML+=`<svg width="120" height="110" viewBox="0 0 120 110" style="position:absolute;left:-12px;top:-12px;overflow:visible"><path d="M60 8 C100 6 116 40 108 64 C98 98 30 104 12 74 C-4 46 24 10 70 12" fill="none" stroke="#E5483C" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" class="c"/></svg>`;
  const t1=ttl(st,X.title??"le jour de ton redressement…",90,{size:58,w:400,color:INK});
  const t2=ttl(st,X.after??"trop tard pour découvrir la loi.",800,{size:52,w:700,color:'#E5483C'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);const e=oB(P(t,.2,.6),1.2);S(cal,{opacity:P(t,.1,.3),transform:`translateY(${(1-e)*80}px) rotate(${(1-e)*-4}deg)`});
    cells.forEach((c,i)=>c.style.opacity=.25+.75*P(t,.4+i*.02,.2));tgt.querySelector('.c').style.strokeDashoffset=1-iO(P(t,kA(k,1.3),.6));blurIn(t2,t,kA(k,1.3)+.6,.5)};};

// 16. BOUCLIER — derrière chaque loi, une protection
B.bouclier=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0;overflow:visible">
    <g class="doc"><rect x="800" y="260" width="320" height="420" rx="16" fill="#F6F1E4"/>${[0,1,2,3,4,5,6].map(i=>`<rect x="840" y="${310+i*48}" width="${i%3===2?160:240}" height="14" rx="7" fill="#B9C2D6"/>`).join('')}</g>
    <path class="sh" d="M960 200 L1180 280 C1180 520 1100 640 960 720 C820 640 740 520 740 280 Z" fill="rgba(243,215,126,.08)" stroke="#F3D77E" stroke-width="10" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" filter="url(#glowG)"/></svg>`);st.appendChild(svg);
  const t1=ttl(st,X.title??'derrière chaque loi…',100,{size:58,w:300});
  const t2=ttl(st,X.after??'une protection.',780,{size:84,w:800,gold:true});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);const d=svg.querySelector('.doc');const e=oC(P(t,.2,.5));d.setAttribute('opacity',e*(1-.55*P(t,kA(k,1.2),.6)));
    svg.querySelector('.sh').style.strokeDashoffset=1-iO(P(t,kA(k,1.2),1));blurIn(t2,t,kA(k,1.2)+.7,.5)};};

// 17. FONDATIONS — des bases solides
B.fondations=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const labs=X.labels||["conformité","respect des règles","déclarations à jour","comptes tenus"];
  const bricks=[];for(let r=0;r<4;r++)for(let c=0;c<6;c++){const x=520+c*150+(r%2)*75-(r%2?75:0),y=700-r*70;const e=$(`<div class="abs" style="left:${x}px;top:${y}px;width:146px;height:66px;border-radius:6px;background:linear-gradient(180deg,#E8C27A,#C9974A);border:2px solid #A8742E"></div>`);st.appendChild(e);bricks.push(e)}
  const lab=labs.map((l,i)=>{const e=$(`<div class="abs" style="left:1440px;top:${700-i*70+12}px;font-size:32px;font-weight:700;color:${INK}">${esc(l)}</div>`);st.appendChild(e);return e});
  const house=$(`<svg class="abs" width="900" height="360" style="left:510px;top:120px;overflow:visible"><path d="M40 330 L40 150 L450 20 L860 150 L860 330" fill="none" stroke="${INK}" stroke-width="12" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" class="h"/><rect x="390" y="200" width="120" height="130" fill="none" stroke="${INK}" stroke-width="10" pathLength="1" stroke-dasharray="1" class="h"/></svg>`);st.appendChild(house);
  const t1=ttl(st,X.title??'des bases solides',40,{size:58,w:800,color:INK});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);bricks.forEach((b,i)=>{const e=bnc(P(t,.2+i*.06,.45));S(b,{opacity:t<.2+i*.06?0:1,transform:`translateY(${(1-e)*-300}px)`})});
    lab.forEach((l,i)=>blurIn(l,t,.5+i*.35,.4));house.querySelectorAll('.h').forEach(p=>p.style.strokeDashoffset=1-iO(P(t,kA(k,2),1)))};};
function bnc(x){const n=7.5625,d=2.75;if(x<1/d)return n*x*x;if(x<2/d)return n*(x-=1.5/d)*x+.75;if(x<2.5/d)return n*(x-=2.25/d)*x+.9375;return n*(x-=2.625/d)*x+.984375}

// 18. ICEBERG — une entreprise, ce n'est pas que le volet financier
B.iceberg=(sc)=>{const X=sc.texts||{};const {el,st}=stage('blue');
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0"><defs><linearGradient id="gIce" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9F2FF"/><stop offset="1" stop-color="#7FA6D6"/></linearGradient></defs>
    <path d="M880 340 L960 250 L1040 330 L1010 360 L900 360 Z" fill="url(#gIce)"/>
    <g class="under"><path d="M900 360 L1010 360 L1180 480 L1260 700 L1120 900 L820 940 L640 760 L700 520 Z" fill="rgba(127,166,214,.55)" stroke="rgba(233,242,255,.6)" stroke-width="3"/></g>
    <rect x="0" y="360" width="1920" height="720" fill="rgba(10,30,70,.45)"/><line x1="0" y1="360" x2="1920" y2="360" stroke="#9FC3F0" stroke-width="3"/></svg>`);st.appendChild(svg);
  const top=$(`<div class="abs" style="left:1080px;top:270px;font-size:40px;font-weight:700;color:#fff">${esc(X.tip??'finances')}</div>`);st.appendChild(top);
  const deep=(X.deep||["fiscal","social","juridique","conformité"]).map((l,i)=>{const e=$(`<div class="abs" style="left:${[760,980,820,1010][i%4]}px;top:${[470,560,660,760][i%4]}px;font-size:40px;font-weight:800" class="goldg">${esc(l)}</div>`);e.classList.add('goldg');st.appendChild(e);return e});
  const t1=ttl(st,X.title??"une entreprise, ce n'est pas que…",110,{size:56,w:300});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);blurIn(top,t,.4);const u=svg.querySelector('.under');const r=iO(P(t,kA(k,1.2),1.2));u.setAttribute('opacity',r);
    deep.forEach((d,i)=>blurIn(d,t,kA(k,1.2)+.4+i*.3,.45))};};

// 19. TRIPTYQUE — 3 engagements
B.triptyque=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const items=X.items||[["1","Expliquer les règles","pour de vrai"],["2","Donner la parole","à l'administration"],["3","Montrer","que ça marche"]];
  const cards=items.map((it,i)=>{const e=$(`<div class="abs" style="left:${250+i*480}px;top:260px;width:420px;height:470px;border-radius:26px;background:linear-gradient(160deg,rgba(40,56,100,.9),rgba(16,24,50,.95));border:1.5px solid rgba(243,215,126,.55);padding:40px;box-shadow:0 30px 60px rgba(0,0,0,.45)"><div class="goldg" style="font-family:Didot,serif;font-weight:700;font-size:150px;line-height:1">${it[0]}</div><div style="font-size:40px;font-weight:700;margin-top:30px;line-height:1.15">${esc(it[1])}</div><div class="itgold" style="font-size:36px;margin-top:10px">${esc(it[2])}</div></div>`);st.appendChild(e);return e});
  const t1=ttl(st,X.title??'mes 3 engagements',110,{size:60,w:300});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);cards.forEach((c,i)=>{const e=oB(P(t,.4+i*.35,.6),1.2);S(c,{opacity:cl(e*1.4),transform:`perspective(1200px) rotateY(${(1-e)*-70}deg) translateY(${(1-e)*40}px)`})})};};

// 20. FLUX — des milliers d'entreprises, les mêmes erreurs
B.flux=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const N=140;const ps=[];for(let i=0;i<N;i++){const e=$(`<div class="abs" style="left:0;top:0;width:12px;height:12px;border-radius:50%;background:#9FB3DA"></div>`);st.appendChild(e);ps.push(e)}
  const gate=$(`<div class="abs" style="left:1000px;top:250px;width:10px;height:520px;background:linear-gradient(180deg,transparent,#F3D77E,transparent);box-shadow:0 0 30px rgba(243,215,126,.6)"></div>`);st.appendChild(gate);
  const t1=ttl(st,X.title??"elle voit passer des milliers d'entreprises",110,{size:54,w:300});
  const t2=ttl(st,X.after??'…et les mêmes erreurs.',800,{size:72,w:800,color:'#FF8A7E'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);const red=kA(k,1.6);
    ps.forEach((p,i)=>{const sp=260+R(i)*220, y=280+R(i+50)*480, x=((t*sp+R(i+9)*2200)%2200)-160;const hit=x>1000&&R(i+33)<.45&&t>red;
      S(p,{transform:`translate(${x}px,${y+(hit?Math.sin(x/40)*4:0)}px)`,background:hit?'#FF6B5E':'#9FB3DA',boxShadow:hit?'0 0 12px rgba(255,107,94,.8)':'none'})});blurIn(t2,t,red+.2,.5)};};

// 21. SEMAINE — une erreur qui revient chaque semaine
B.semaine=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const days=["L","M","M","J","V","S","D"];const g=$(`<div class="abs" style="left:520px;top:250px;display:grid;grid-template-columns:repeat(7,110px);gap:14px"></div>`);st.appendChild(g);
  days.forEach(d=>g.appendChild($(`<div style="text-align:center;font-weight:800;font-size:28px;color:#8B93A8">${d}</div>`)));
  const marks=[];for(let w=0;w<4;w++)for(let d=0;d<7;d++){const c=$(`<div style="height:90px;border-radius:14px;background:#fff;border:1.5px solid #E1E4EC;position:relative"></div>`);g.appendChild(c);if(d===1){const m=$(`<div style="position:absolute;inset:14px;border-radius:50%;background:#E5483C;opacity:0"></div>`);c.appendChild(m);marks.push(m)}}
  const t1=ttl(st,X.title??'pour vous, un accident…',110,{size:56,w:400,color:INK});
  const t2=ttl(st,X.after??'pour elle, une erreur qui revient chaque semaine.',830,{size:48,w:700,color:'#E5483C'});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);blurIn(g,t,.2,.4);marks.forEach((m,i)=>{const e=oB(P(t,kA(k,.9)+i*.35,.35));S(m,{opacity:cl(e),transform:`scale(${e})`})});blurIn(t2,t,kA(k,.9)+1.4,.5)};};

// 22. CROISSANCE — des entreprises en règle qui grandissent
B.croissance=(sc)=>{const X=sc.texts||{};const {el,st}=stage('light');
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0"><path d="M300 760 L1620 760" stroke="#D5D9E4" stroke-width="3"/><path class="ln" d="M300 720 C520 700 640 640 800 600 S1080 520 1200 430 S1480 260 1620 200" fill="none" stroke="#C99A2E" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/></svg>`);st.appendChild(svg);
  const badges=(X.badges||["en règle","financement obtenu","marché gagné"]).map((b,i)=>{const e=$(`<div class="abs" style="left:${[620,1010,1380][i]}px;top:${[520,390,160][i]}px;padding:16px 28px;border-radius:999px;background:#131C38;color:#F3D77E;font-size:32px;font-weight:700;white-space:nowrap;box-shadow:0 12px 30px rgba(20,30,60,.25)">✓ ${esc(b)}</div>`);st.appendChild(e);return e});
  const t1=ttl(st,X.title??'en règle… et elles grandissent',100,{size:58,w:800,color:INK});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);svg.querySelector('.ln').style.strokeDashoffset=1-iO(P(t,.3,Math.max(1.2,D*.6)));
    badges.forEach((b,i)=>popIn(b,t,.6+i*Math.max(.5,D*.2),.5))};};

// 23. BOÎTE À OUTILS — pas d'astuces… des dispositifs prévus par la loi
B.boite_outils=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const hat=$(`<svg class="abs" width="360" height="320" viewBox="0 0 360 320" style="left:300px;top:320px;overflow:visible"><rect x="80" y="40" width="200" height="200" rx="10" fill="#101521" stroke="#3A4560" stroke-width="4"/><rect x="20" y="230" width="320" height="40" rx="20" fill="#101521" stroke="#3A4560" stroke-width="4"/><rect x="80" y="180" width="200" height="30" fill="#E5483C"/><text x="180" y="-10" text-anchor="middle" font-size="42" font-weight="800" fill="#fff" font-family="Avenir Next">astuces ?</text><line class="x" x1="0" y1="300" x2="360" y2="0" stroke="#E5483C" stroke-width="16" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/></svg>`);st.appendChild(hat);
  const box=$(`<svg class="abs" width="620" height="420" viewBox="0 0 620 420" style="left:1000px;top:300px;overflow:visible"><rect x="40" y="170" width="540" height="230" rx="18" fill="url(#gGold)"/><rect x="250" y="130" width="120" height="50" rx="12" fill="none" stroke="#C99A2E" stroke-width="14"/><g class="lid"><rect x="30" y="140" width="560" height="50" rx="14" fill="#E9C766"/></g></svg>`);st.appendChild(box);
  const tools=(X.tools||["exonérations","régimes adaptés","délais de grâce","crédits d'impôt"]).map((l,i)=>{const e=$(`<div class="abs" style="left:${1000+(i%2)*300}px;top:${250-Math.floor(i/2)*70}px;padding:12px 22px;border-radius:999px;background:rgba(255,255,255,.1);border:1.5px solid rgba(243,215,126,.7);font-size:28px;font-weight:600;white-space:nowrap">${esc(l)}</div>`);st.appendChild(e);return e});
  const t1=ttl(st,X.title??"pas d'astuces, pas de combines…",60,{size:56,w:300});
  const t2=ttl(st,X.after??'des dispositifs prévus par la loi.',800,{size:60,w:800,gold:true});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);blurIn(hat,t,.2,.4);hat.querySelector('.x').style.strokeDashoffset=1-iO(P(t,.8,.35));
    const b=kB(k,2);blurIn(box,t,b-.4,.4);box.querySelector('.lid').setAttribute('transform',`rotate(${-35*iO(P(t,b,.5))} 30 165)`);tools.forEach((e,i)=>{const f=oB(P(t,b+.3+i*.15,.5));S(e,{opacity:cl(f*1.4),transform:`translateY(${(1-f)*120}px) scale(${Math.max(0,f)})`})});blurIn(t2,t,b+.9,.5)};};

// 24. ORAGE — pas de peur : comprendre
B.orage=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const cloud=$(`<svg class="abs" width="700" height="420" viewBox="0 0 700 420" style="left:610px;top:200px;overflow:visible"><path d="M170 300 C80 300 60 200 140 180 C140 90 260 60 320 120 C360 40 520 60 520 170 C620 170 640 300 540 300 Z" fill="#3A4560"/><path class="bolt" d="M340 300 L300 380 L350 380 L320 460" fill="none" stroke="#F3D77E" stroke-width="12" stroke-linejoin="round"/></svg>`);st.appendChild(cloud);
  const bulb=$(`<svg class="abs" width="300" height="400" viewBox="0 0 300 400" style="left:810px;top:220px;overflow:visible"><circle cx="150" cy="150" r="200" fill="rgba(255,236,170,.18)" filter="url(#soft)"/><path d="M150 30 C70 30 40 100 60 150 C75 190 105 205 105 250 L195 250 C195 205 225 190 240 150 C260 100 230 30 150 30 Z" fill="#FFE7A8"/><rect x="108" y="262" width="84" height="22" rx="8" fill="#C99A2E"/><rect x="116" y="292" width="68" height="20" rx="8" fill="#C99A2E"/></svg>`);st.appendChild(bulb);
  const t1=ttl(st,X.title??'pas de peur…',90,{size:60,w:300});
  const t2=ttl(st,X.after??'comprendre.',770,{size:96,w:800,gold:true});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);const a=kA(k,1.3);const f=P(t,a,.8);
    S(cloud,{opacity:(1-f)*P(t,.1,.3),filter:`blur(${f*20}px)`,transform:`scale(${1+f*.3})`});cloud.querySelector('.bolt').setAttribute('opacity',(Math.sin(t*23)>.3&&t<a)?1:0);
    S(bulb,{opacity:oC(P(t,a+.2,.6)),transform:`scale(${.7+.3*oB(P(t,a+.2,.6))})`});blurIn(t2,t,a+.6,.5)};};

// 25. CONFIDENTIEL — jamais de dossier, jamais de nom
B.confidentiel=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const f=$(`<div class="abs" style="left:620px;top:230px;width:680px;height:460px;border-radius:18px;background:linear-gradient(180deg,#E9C766,#C99A2E);box-shadow:0 30px 60px rgba(0,0,0,.5);padding:50px;color:#131C38"><div style="font-size:26px;letter-spacing:.25em;font-weight:800">DOSSIER</div><div class="nm" style="margin-top:30px;font-size:52px;font-weight:800">Entreprise X — SARL</div><div style="margin-top:24px;font-size:30px;opacity:.7">N° contribuable : 1234567 A</div></div>`);st.appendChild(f);
  const lock=$(`<svg class="abs" width="220" height="260" viewBox="0 0 220 260" style="left:1220px;top:520px;overflow:visible"><path class="sh" d="M50 120 L50 70 C50 20 170 20 170 70 L170 120" fill="none" stroke="#fff" stroke-width="22"/><rect x="20" y="115" width="180" height="140" rx="22" fill="#131C38" stroke="#F3D77E" stroke-width="6"/><circle cx="110" cy="180" r="16" fill="#F3D77E"/></svg>`);st.appendChild(lock);
  const t1=ttl(st,X.title??'jamais un dossier, jamais un nom',90,{size:56,w:300});
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);blurIn(f,t,.2,.5,30);const a=kA(k,1);f.querySelector('.nm').style.filter=`blur(${14*P(t,a,.5)}px)`;
    const l=oB(P(t,a+.4,.5));S(lock,{opacity:cl(l*1.5),transform:`scale(${Math.max(0,l)})`});lock.querySelector('.sh').setAttribute('transform',`translate(0 ${-20*(1-P(t,a+1,.25))})`)};};

// 26. ASSOCIÉ — l'État, votre associé silencieux… il regarde les comptes
B.associe=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const cx=700,cy=470,Rr=230;const arc=(a0,a1)=>{const p=a=>[cx+Math.cos(a)*Rr,cy+Math.sin(a)*Rr];const [x0,y0]=p(a0),[x1,y1]=p(a1);return `M${cx} ${cy} L${x0} ${y0} A${Rr} ${Rr} 0 ${a1-a0>Math.PI?1:0} 1 ${x1} ${y1} Z`};
  const svg=$(`<svg class="abs" width="1920" height="1080" style="left:0;top:0;overflow:visible"><path d="${arc(-Math.PI/2+1.6,-Math.PI/2+2*Math.PI)}" fill="#2B3C68" stroke="#0B1229" stroke-width="4"/><path class="sl" d="${arc(-Math.PI/2,-Math.PI/2+1.6)}" fill="url(#gGold)" stroke="#0B1229" stroke-width="4"/>
    <g class="eye" transform="translate(1340 420)"><path class="lid" d="M-170 0 Q0 -120 170 0 Q0 120 -170 0 Z" fill="#F6F1E4"/><circle r="52" fill="#131C38"/><circle r="22" fill="#F3D77E"/></g></svg>`);st.appendChild(svg);
  const lb=$(`<div class="abs" style="left:${cx+40}px;top:${cy-230}px;font-size:40px;font-weight:800;color:#F3D77E">${esc(X.slice??"l'État")}</div>`);st.appendChild(lb);
  const lr=$(`<div class="abs" style="left:${cx-150}px;top:${cy+260}px;width:300px;text-align:center;font-size:32px;color:rgba(255,255,255,.75)">${esc(X.pie??'votre résultat')}</div>`);st.appendChild(lr);
  const t1=ttl(st,X.title??'votre associé silencieux',90,{size:62,w:700});
  const t2=$(`<div class="abs" style="left:1100px;top:600px;width:520px;text-align:center;font-size:44px;font-weight:700" class="itgold">${esc(X.after??'un jour, il regarde les comptes.')}</div>`);t2.classList.add('itgold');st.appendChild(t2);
  return (t,D,k)=>{sceneFx(el,t,D);blurIn(t1,t,.1);blurIn(lr,t,.3);const s=oB(P(t,.6,.6));svg.querySelector('.sl').setAttribute('transform',`translate(${s*24} ${-s*24})`);blurIn(lb,t,.8);
    const b=kB(k,2.2);const o=iO(P(t,b,.5));svg.querySelector('.eye').setAttribute('opacity',P(t,b-.1,.2));svg.querySelector('.lid').setAttribute('transform',`scale(1 ${Math.max(.05,o)})`);blurIn(t2,t,b+.4,.5)};};

// 27. PARCHEMIN — la règle de base
B.parchemin=(sc)=>{const X=sc.texts||{};const {el,st}=stage('dark');
  const sc2=$(`<div class="abs" style="left:460px;top:170px;width:1000px;height:620px;overflow:hidden"><div class="pp" style="position:absolute;left:0;right:0;top:0;height:620px;border-radius:14px;background:linear-gradient(180deg,#F6EBCF,#EAD7A8);box-shadow:inset 0 0 60px rgba(150,110,40,.35);padding:70px 90px;color:#3A2A10;text-align:center">
    <div style="font-size:26px;letter-spacing:.3em;font-weight:800;color:#8C6A14">${esc(X.kicker??'LA RÈGLE DE BASE')}</div>
    <div style="margin-top:40px;font-family:Didot,serif;font-size:56px;line-height:1.25">${esc(X.rule??"Ce que vous n'accepteriez pas d'un associé, ne l'acceptez pas de lui.")}</div></div></div>`);st.appendChild(sc2);
  const rodT=$(`<div class="abs" style="left:430px;top:150px;width:1060px;height:40px;border-radius:20px;background:linear-gradient(180deg,#8C6A14,#E9C766,#8C6A14)"></div>`),rodB=$(`<div class="abs" style="left:430px;top:150px;width:1060px;height:40px;border-radius:20px;background:linear-gradient(180deg,#8C6A14,#E9C766,#8C6A14)"></div>`);st.append(rodT,rodB);
  const seal=$(`<div class="abs" style="left:1330px;top:640px">${seal0(150)}</div>`);st.appendChild(seal);
  return (t,D,k)=>{sceneFx(el,t,D);const u=iO(P(t,.2,1.1));sc2.style.height=px(620*u);rodB.style.top=px(150+620*u);S(rodT,{opacity:P(t,0,.2)});S(rodB,{opacity:P(t,0,.2)});
    const s=oB(P(t,kA(k,1.6),.5));S(seal,{opacity:cl(s*1.4),transform:`rotate(${(1-s)*-90}deg) scale(${Math.max(0,s)})`})};};
function seal0(sz){return seal(sz)}
