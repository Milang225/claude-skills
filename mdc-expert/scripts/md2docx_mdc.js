// md2docx_mdc.js — Générateur soigné MDC (docx-js) : Markdown -> Word à l'identité MDC
// Usage: NODE_PATH=<global_modules> node md2docx_mdc.js SOURCE.md DEST.docx "Titre" "Client" "Réf"
// Rendu : en-tête à logo + double filet, bandeau-titre navy/or, titres à filet or,
//         tableaux navy/alternés (montants à droite, TOTAL sur or pâle), encadrés crème, pied légal + pagination.
const fs = require("fs");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  BorderStyle, ShadingType, AlignmentType, ImageRun, Header, Footer, PageNumber, VerticalAlign } = D;

const [,, SRC, DEST, TITLE="LIVRABLE", CLIENT="", REF=""] = process.argv;
const NAVY="1A1A2E", GOLD="C9A227", GOLDL="E8C547", GOLDPALE="F5E5A5", CREAM="FFFBE8", PEARL="F4F4F8", RED="C0392B", INK="222222", GREY="666666";
const FONT="Times New Roman", SANS="Calibri", CW=9638;
const LOGO="/Users/bilefilsseverin/.claude/skills/mdc-expert/scripts/logo-mdc.jpg";
const logo = fs.existsSync(LOGO) ? fs.readFileSync(LOGO) : null;

const MOIS=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
const now=new Date(); const DATE=`Abidjan, le ${now.getDate()} ${MOIS[now.getMonth()]} ${now.getFullYear()}`;

const noB={style:BorderStyle.NONE,size:0,color:"FFFFFF"};
const noBorders={top:noB,bottom:noB,left:noB,right:noB,insideHorizontal:noB,insideVertical:noB};
function rule(sz,color){ return new Paragraph({spacing:{before:20,after:0},border:{bottom:{style:BorderStyle.SINGLE,size:sz,color}}}); }
// runs avec **gras**
function runs(text,{color=INK,i=false,sz=22,font=FONT}={}){
  const out=[];
  text=String(text).replace(/(?<=\d)\s+(?=\d)/g," ");  // nombres insécables (« 504 072 » non coupé)
  text.split("**").forEach((seg,bi)=>{                    // ** = gras
    const bold=bi%2===1;
    seg.split("*").forEach((s,ii)=>{                      // * = italique (dont ***gras+italique***)
      if(s) out.push(new TextRun({text:s,bold,italics:i||ii%2===1,size:sz,color,font}));
    });
  });
  return out.length?out:[new TextRun({text:"",size:sz,font})];
}
function isAmount(s){ const t=String(s).replace(/[\s.  %≈\-—()FCFA]/gi,""); return t.length>0 && /^\d+$/.test(t); }

// ---------- Header / Footer ----------
function header(){
  const kids=[];
  const idCell=new TableCell({width:{size:CW-2400,type:WidthType.DXA},borders:noBorders,verticalAlign:VerticalAlign.CENTER,children:[
    new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"LA MAISON DE LA CONFORMITÉ SARL",bold:true,size:20,color:NAVY,font:SANS})]}),
    new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Agence de Notation Administrative — Comptable · Fiscal · Social",italics:true,size:15,color:GOLD,font:SANS})]}),
    new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Abidjan — Côte d'Ivoire · +225 07 19 31 49 04",size:13,color:GREY,font:SANS})]}),
  ]});
  const logoCell=new TableCell({width:{size:2400,type:WidthType.DXA},borders:noBorders,verticalAlign:VerticalAlign.CENTER,children:[
    new Paragraph({children: logo?[new ImageRun({type:"jpg",data:logo,transformation:{width:150,height:61}})]:[new TextRun({text:"MDC",bold:true,color:NAVY})]})]});
  kids.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:[2400,CW-2400],borders:noBorders,rows:[new TableRow({children:[logoCell,idCell]})]}));
  kids.push(rule(14,NAVY)); kids.push(rule(8,GOLD));
  return new Header({children:kids});
}
function footer(){
  return new Footer({children:[
    rule(8,GOLD),
    new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"LA MAISON DE LA CONFORMITÉ SARL — NCC : 2506426B — RCCM : CI-ABJ-03-2025-B13-10831 — Capital : 1 000 000 FCFA",size:13,color:GREY,font:SANS})]}),
    new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"Tél : 07 19 31 49 04 — lamaisondelaconformitesarl@outlook.com — Document confidentiel — Secret professionnel",size:13,color:GREY,font:SANS})]}),
    new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Page ",size:13,italics:true,color:NAVY,font:SANS}),new TextRun({children:[PageNumber.CURRENT],size:13,italics:true,color:NAVY,font:SANS}),new TextRun({text:" / ",size:13,italics:true,color:NAVY,font:SANS}),new TextRun({children:[PageNumber.TOTAL_PAGES],size:13,italics:true,color:NAVY,font:SANS})]}),
  ]});
}

// ---------- Table cell ----------
function cell(text,{w,header=false,total=false,alt=false,align=AlignmentType.LEFT}={}){
  const shade=header?NAVY:(total?GOLDPALE:(alt?PEARL:"FFFFFF"));
  const color=header?"FFFFFF":(total?NAVY:INK);
  const rs=runs(text,{color,sz:18,font:SANS}).map(r=>{ if(header||total){ r.bold=true; } return r; });
  return new TableCell({width:{size:w,type:WidthType.DXA},shading:{type:ShadingType.CLEAR,fill:shade,color:"auto"},
    margins:{top:40,bottom:40,left:90,right:90},verticalAlign:VerticalAlign.CENTER,
    borders:{top:{style:BorderStyle.SINGLE,size:2,color:"C9C9D2"},bottom:{style:BorderStyle.SINGLE,size:2,color:"C9C9D2"},left:noB,right:noB},
    children:[new Paragraph({alignment:align,spacing:{after:0},children:rs})]});
}
function buildTable(rowsRaw){
  const rows=rowsRaw.map(r=>r.split("|").slice(1,-1).map(c=>c.trim()));
  const ncol=rows[0].length;
  // largeurs proportionnelles au contenu (plancher pour éviter les colonnes écrasées)
  const wgt=[];
  for(let ci=0;ci<ncol;ci++){ let L=4; rows.forEach(r=>{ const t=(r[ci]||"").replace(/\*/g,""); if(t.length>L)L=t.length; }); wgt.push(Math.max(4,Math.min(L,42))); }
  const tot=wgt.reduce((a,b)=>a+b,0);
  let widths=wgt.map(x=>Math.round(CW*x/tot));
  const floor=1250;
  for(let k=0;k<ncol;k++){ if(widths[k]<floor){ const need=floor-widths[k]; widths[k]=floor; const mi=widths.indexOf(Math.max(...widths)); widths[mi]-=need; } }
  const diff=CW-widths.reduce((a,b)=>a+b,0); widths[widths.indexOf(Math.max(...widths))]+=diff;
  // colonnes montant
  const amountCol=Array(ncol).fill(0);
  rows.slice(1).forEach(r=>r.forEach((c,i)=>{ if(c&&isAmount(c)) amountCol[i]++; }));
  const bodyN=rows.length-1;
  const isAmt=amountCol.map(n=>n>=Math.max(1,bodyN*0.5));
  const trs=[];
  rows.forEach((r,ri)=>{
    const isTot=/\bTOTAL\b/i.test(r[0]||"");
    trs.push(new TableRow({tableHeader:ri===0,children:r.map((c,i)=>cell(c,{w:widths[i],header:ri===0,total:ri>0&&isTot,alt:ri>0&&!isTot&&ri%2===0,align:isAmt[i]?AlignmentType.RIGHT:AlignmentType.LEFT}))}));
  });
  return new Table({width:{size:CW,type:WidthType.DXA},columnWidths:widths,borders:noBorders,rows:trs});
}

// ---------- Parse markdown ----------
const md=fs.readFileSync(SRC,"utf8").replace(/\r/g,"");
const lines=md.split("\n");
const kids=[];
// bandeau titre
kids.push(new Paragraph({shading:{type:ShadingType.CLEAR,fill:NAVY,color:"auto"},border:{bottom:{style:BorderStyle.SINGLE,size:14,color:GOLD}},alignment:AlignmentType.CENTER,spacing:{after:0},
  children:[new TextRun({text:TITLE,bold:true,size:26,color:"FFFFFF",font:FONT})]}));
const meta=[]; if(CLIENT) meta.push("Client : "+CLIENT); if(REF) meta.push("Réf. : "+REF); meta.push(DATE);
kids.push(new Paragraph({shading:{type:ShadingType.CLEAR,fill:NAVY,color:"auto"},alignment:AlignmentType.CENTER,spacing:{after:140},
  children:[new TextRun({text:meta.join("   |   "),size:16,color:GOLDL,font:SANS})]}));

let i=0;
while(i<lines.length){
  let ln=lines[i];
  if(!ln.trim()){ i++; continue; }
  if(ln.startsWith("|")){
    const blk=[]; while(i<lines.length && lines[i].trim().startsWith("|")){ if(!/^\s*\|[\s:|-]+\|\s*$/.test(lines[i])) blk.push(lines[i]); i++; }
    if(blk.length) kids.push(buildTable(blk)); kids.push(new Paragraph({spacing:{after:80},children:[]})); continue;
  }
  if(ln.startsWith("### ")){ kids.push(new Paragraph({spacing:{before:120,after:20},children:runs(ln.slice(4),{color:NAVY,sz:23})})); i++; continue; }
  if(ln.startsWith("## ")){ kids.push(new Paragraph({spacing:{before:160,after:20},children:runs(ln.slice(3),{color:NAVY,sz:26})})); kids.push(rule(10,GOLD)); i++; continue; }
  if(ln.startsWith("# ")){ kids.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:120,after:40},children:runs(ln.slice(2),{color:NAVY,sz:28})})); i++; continue; }
  if(ln.startsWith("> ")){
    kids.push(new Paragraph({shading:{type:ShadingType.CLEAR,fill:CREAM,color:"auto"},border:{left:{style:BorderStyle.SINGLE,size:18,color:GOLD}},
      indent:{left:150},alignment:AlignmentType.JUSTIFY,spacing:{before:80,after:120,line:264},children:runs(ln.slice(2),{color:NAVY})})); i++; continue;
  }
  if(/^[-*] /.test(ln)){ kids.push(new Paragraph({bullet:{level:0},spacing:{after:40},children:runs(ln.slice(2))})); i++; continue; }
  if(/^(?:<br\s*\/?>\s*)+$/.test(ln.trim())){ kids.push(new Paragraph({spacing:{after:0},children:[]})); i++; continue; }
  // paragraphe (gère <br> en fin)
  ln=ln.replace(/<br>/g," ");
  kids.push(new Paragraph({alignment:AlignmentType.JUSTIFY,spacing:{after:120,line:264},children:runs(ln)}));
  i++;
}

const doc=new Document({creator:"La Maison de la Conformité SARL",title:TITLE,
  styles:{default:{document:{run:{font:FONT,size:22,color:INK}}}},
  sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:2100,bottom:1400,left:1134,right:1134,header:567,footer:567}}},
    headers:{default:header()},footers:{default:footer()},children:kids}]});
Packer.toBuffer(doc).then(buf=>{ fs.writeFileSync(DEST,buf); console.log("GEN_OK",DEST); }).catch(e=>{ console.error("GEN_FAIL",e.message); process.exit(2); });
