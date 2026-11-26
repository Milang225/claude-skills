import fitz, os, subprocess, sys, time, tempfile
from concurrent.futures import ThreadPoolExecutor

OCR_BIN = os.path.expanduser("~/.claude/skills/mdc-expert/scripts/mdc-ocr")
desk = "/Users/bilefilsseverin/Desktop"
base = next(os.path.join(desk,d) for d in os.listdir(desk) if "FISCALIT" in d.upper())
OUT  = os.path.join(base, "_OCR_TEXTE")
os.makedirs(OUT, exist_ok=True)
LOG  = os.path.join(OUT, "_progress.log")

BOOKS = ["comptabilite.pdf","fiscalie.pdf","IMPOT SUR LES BENEFICES.pdf","traitemznt.pdf"]
DPI = 190
WORKERS = 8

def log(m):
    line=f"[{time.strftime('%H:%M:%S')}] {m}"
    with open(LOG,"a") as fh: fh.write(line+"\n")
    print(line, flush=True)

def ocr_png(png):
    try:
        r = subprocess.run([OCR_BIN, png], capture_output=True, text=True, timeout=120)
        return r.stdout
    except Exception as e:
        return f"[OCR_ERR {e}]"

def process_book(book):
    path = os.path.join(base, book)
    stem = os.path.splitext(book)[0].replace(" ","_")
    pages_dir = os.path.join(OUT, stem+"_pages")
    os.makedirs(pages_dir, exist_ok=True)
    combined = os.path.join(OUT, stem+".txt")
    doc = fitz.open(path)
    n = doc.page_count
    log(f"START {book}: {n} pages")
    done_marker = os.path.join(OUT, stem+".DONE")
    if os.path.exists(done_marker):
        log(f"SKIP {book} (already done)"); doc.close(); return
    CH = WORKERS
    with open(combined,"w") as cf:
        for start in range(0, n, CH):
            batch = list(range(start, min(start+CH, n)))
            pngs = {}
            for p in batch:
                pg = doc[p]
                pix = pg.get_pixmap(dpi=DPI)
                fp = os.path.join(tempfile.gettempdir(), f"{stem}_{p}.png")
                pix.save(fp); pngs[p]=fp
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                results = dict(zip(batch, ex.map(lambda p: ocr_png(pngs[p]), batch)))
            for p in batch:
                txt = results[p]
                with open(os.path.join(pages_dir, f"p{p+1:04d}.txt"),"w") as pf:
                    pf.write(txt)
                cf.write(f"\n\n===== PAGE {p+1} =====\n{txt}")
                try: os.remove(pngs[p])
                except: pass
            if start % 40 == 0:
                log(f"  {book}: {min(start+CH,n)}/{n}")
    doc.close()
    open(done_marker,"w").write(time.strftime("%Y-%m-%d %H:%M:%S"))
    log(f"DONE {book} -> {combined} ({os.path.getsize(combined)//1024} KB)")

if __name__=="__main__":
    log("="*50)
    log("OCR ORCHESTRATOR START")
    t0=time.time()
    order = sys.argv[1:] if len(sys.argv)>1 else BOOKS
    for b in order:
        try: process_book(b)
        except Exception as e: log(f"FAIL {b}: {e}")
    log(f"ALL DONE in {(time.time()-t0)/60:.1f} min")
