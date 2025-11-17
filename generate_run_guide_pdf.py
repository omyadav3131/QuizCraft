"""
HEADER_COMMENT_AUTOGEN
FILE: generate_run_guide_pdf.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

INPUT_MD = 'README_RUN.md'
OUTPUT_PDF = 'run_guide.pdf'


def read_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        return f.read()


def draw_text(c, text, x, y, max_width):
    # Simple word-wrap for a monospaced-ish layout
    from reportlab.pdfbase.pdfmetrics import stringWidth
    lines = []
    for paragraph in text.split('\n\n'):
        words = paragraph.split()
        if not words:
            lines.append('')
            continue
        cur = words[0]
        for w in words[1:]:
            if stringWidth(cur + ' ' + w, 'Helvetica', 10) < max_width:
                cur = cur + ' ' + w
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        lines.append('')
    for line in lines:
        c.drawString(x, y, line)
        y -= 12
        if y < 20*mm:
            c.showPage()
            y = A4[1] - 20*mm
    return y


def main():
    if not os.path.exists(INPUT_MD):
        print(f"{INPUT_MD} not found. Make sure you're in the project root.")
        return
    text = read_markdown(INPUT_MD)
    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    width, height = A4
    margin = 20*mm
    x = margin
    y = height - margin
    # Title
    c.setFont('Helvetica-Bold', 16)
    c.drawString(x, y, 'Run Guide — Flask Quiz App')
    y -= 18
    c.setFont('Helvetica', 10)
    y -= 6
    y = draw_text(c, text, x, y, width - 2*margin)
    c.save()
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == '__main__':
    main()
