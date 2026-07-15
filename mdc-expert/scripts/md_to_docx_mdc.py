#!/usr/bin/env python3
"""Convert markdown to docx via HTML and textutil — MDC professional style."""
import sys
import subprocess
from pathlib import Path
import markdown


MDC_HEADER = (
    '<div class="mdc-banner">'
    '<div class="mdc-tagline">LA MAISON DE LA CONFORMITÉ SARL</div>'
    '<div class="mdc-sub">Agence de Notation Administrative — Comptable · Fiscal · Social — Côte d\'Ivoire</div>'
    '</div>'
)

MDC_FOOTER = (
    '<div class="mdc-footer">'
    '<strong>LA MAISON DE LA CONFORMITÉ SARL</strong> &nbsp;|&nbsp; '
    'NCC : 2506426B &nbsp;|&nbsp; RCCM : CI-ABJ-03-2025-B13-10831 &nbsp;|&nbsp; '
    'Capital : 1 000 000 FCFA<br>'
    'Tél : 07 19 31 49 04 &nbsp;|&nbsp; '
    'lamaisondelaconformitesarl@outlook.com &nbsp;|&nbsp; '
    'www.lamaisondelaconformitesarl.net'
    '</div>'
)


def convert(md_path: str, docx_path: str):
    md_text = Path(md_path).read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )
    css = """
    <style>
    @page { size: A4; margin: 2.2cm 2cm; }
    body {
        font-family: "Times New Roman", "Liberation Serif", serif;
        font-size: 11pt;
        line-height: 1.4;
        color: #1a1a1a;
    }
    .mdc-banner {
        background: #1A1A2E;
        color: #E8C547;
        padding: 10px 18px;
        text-align: center;
        margin-bottom: 18pt;
        border-bottom: 4px solid #E8C547;
    }
    .mdc-tagline {
        font-size: 14pt;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .mdc-sub {
        font-size: 9pt;
        font-style: italic;
        color: #FFFFFF;
        margin-top: 2pt;
    }
    .mdc-footer {
        margin-top: 24pt;
        padding: 10px 14px;
        background: #F5F5FA;
        border-top: 2px solid #1A1A2E;
        text-align: center;
        font-size: 8.5pt;
        color: #444;
        font-family: "Calibri", Arial, sans-serif;
    }
    h1 {
        color: #1A1A2E;
        font-size: 18pt;
        font-family: "Calibri", Arial, sans-serif;
        font-weight: bold;
        border-bottom: 3px double #E8C547;
        padding-bottom: 6px;
        margin-top: 8pt;
        margin-bottom: 14pt;
    }
    h2 {
        color: #1A1A2E;
        font-size: 14pt;
        font-family: "Calibri", Arial, sans-serif;
        font-weight: bold;
        margin-top: 18pt;
        margin-bottom: 6pt;
        border-left: 5px solid #E8C547;
        padding-left: 10px;
    }
    h3 {
        color: #2C2C4E;
        font-size: 12pt;
        font-family: "Calibri", Arial, sans-serif;
        font-weight: bold;
        margin-top: 14pt;
        margin-bottom: 4pt;
    }
    h4 {
        color: #2C2C4E;
        font-size: 11pt;
        font-family: "Calibri", Arial, sans-serif;
        font-weight: bold;
        margin-top: 12pt;
        margin-bottom: 3pt;
    }
    p {
        margin: 5pt 0;
        text-align: justify;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 10pt 0;
        font-family: "Calibri", Arial, sans-serif;
        font-size: 10pt;
    }
    th, td {
        border: 1px solid #888;
        padding: 6px 8px;
        vertical-align: top;
    }
    th {
        background-color: #1A1A2E;
        color: #FFFFFF;
        font-weight: bold;
        text-align: left;
    }
    tr:nth-child(even) td {
        background-color: #F4F4F8;
    }
    code, pre {
        font-family: Consolas, "Courier New", monospace;
        background: #F0F0F5;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 9.5pt;
        color: #1A1A2E;
    }
    pre {
        padding: 8pt 12pt;
        border-left: 3px solid #1A1A2E;
        white-space: pre-wrap;
    }
    blockquote {
        border-left: 4px solid #E8C547;
        margin-left: 0;
        padding: 4pt 12pt;
        background: #FFFBE8;
        color: #444;
        font-style: italic;
    }
    hr {
        border: 0;
        border-top: 1px solid #E8C547;
        margin: 16pt 0;
    }
    ul, ol { margin: 6pt 0; padding-left: 24px; }
    li { margin: 2pt 0; }
    strong { color: #1A1A2E; }
    em { color: #444; }
    </style>
    """
    html = (
        f"<!doctype html><html><head><meta charset='utf-8'>{css}</head><body>"
        f"{MDC_HEADER}{html_body}{MDC_FOOTER}"
        f"</body></html>"
    )
    html_path = Path(docx_path).with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    subprocess.run(
        ["textutil", "-convert", "docx", "-output", docx_path, str(html_path)],
        check=True,
    )
    html_path.unlink()
    print(f"OK -> {docx_path}")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
