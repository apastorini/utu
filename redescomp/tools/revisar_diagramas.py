import pathlib
import subprocess
import sys

ROOT = pathlib.Path(r'C:\Utu\utu\redescomp')
sys.path.insert(0, str(ROOT / 'tools'))
import diagramas as D

CSS = """<!DOCTYPE html><html><head><meta charset=utf-8><style>
@page{size:A4;margin:14mm}
svg{display:block;margin:0 auto 14px;page-break-inside:avoid}
div{page-break-inside:avoid;margin-bottom:12px}
</style></head><body>"""


def main():
    nombres = sys.argv[1:] or list(D.DIAGRAMAS)
    partes = [CSS]
    for n in nombres:
        partes.append('<div>' + D.DIAGRAMAS[n]() + '</div>')
    partes.append('</body></html>')
    html = ROOT / '.build' / 'diag_check.html'
    pdf = ROOT / '.build' / 'diag_check.pdf'
    html.write_text(''.join(partes), encoding='utf-8')
    if pdf.exists():
        pdf.unlink()
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    subprocess.run([
        chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
        '--no-pdf-header-footer', '--virtual-time-budget=8000',
        f'--user-data-dir={ROOT}\\.build\\cp4',
        f'--print-to-pdf={pdf}', html.as_uri()],
        capture_output=True, text=True, timeout=200)
    print('pdf:', pdf.exists(), pdf.stat().st_size // 1024 if pdf.exists() else 0, 'KB')
    print('diagramas:', ', '.join(nombres))


if __name__ == '__main__':
    main()
