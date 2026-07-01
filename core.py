#!/usr/bin/env python3
"""Shared layout engine for the Geriatric PT Assessment Booklet generators.

Provides fonts (with a portable fallback chain), colour palette, paragraph
styles, table helpers, a page-numbering canvas, and a TOC-aware doc template.
Both the English and Chinese generators import from this module, so a change
to styling or layout propagates to both booklets.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                 Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfgen import canvas

# ── Font registration (portable fallback chain) ──────────────────────────
# Songti SC has full glyph coverage (□, ≥, –, curly quotes) and a true Bold.
# If unavailable (non-macOS), fall back through common Linux CJK fonts, and
# finally to Helvetica (renders Latin fine but lacks □ / ≥).
_FONT_CANDIDATES = [
    # (label, path, regular_subfont, bold_subfont)
    ('Songti', '/System/Library/Fonts/Supplemental/Songti.ttc', 6, 1),
    ('STHeiti', '/System/Library/Fonts/STHeiti Medium.ttc', 1, 1),
    ('NotoCJK-otc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 0, 0),
    ('NotoCJK-ttc', '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc', 0, 0),
    ('WenQuanYi', '/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc', 0, 0),
]


def _register_fonts():
    """Try candidate fonts in order; return (regular_name, bold_name)."""
    for _label, path, reg_idx, bold_idx in _FONT_CANDIDATES:
        if not os.path.isfile(path):
            continue
        try:
            pdfmetrics.registerFont(TTFont('BodyR', path, subfontIndex=reg_idx))
            pdfmetrics.registerFont(TTFont('BodyB', path, subfontIndex=bold_idx))
            registerFontFamily('BodyR', normal='BodyR', bold='BodyB',
                               italic='BodyR', boldItalic='BodyB')
            return 'BodyR', 'BodyB'
        except Exception:
            continue
    return 'Helvetica', 'Helvetica-Bold'


BASE_FONT, BOLD_FONT = _register_fonts()

# ── Palette ──────────────────────────────────────────────────────────────
ACCENT       = colors.HexColor('#1F5C6B')
ACCENT_DARK  = colors.HexColor('#15414C')
ACCENT_LIGHT = colors.HexColor('#EAF1F3')
GREY_LINE    = colors.HexColor('#B8C4C8')
GREY_TEXT    = colors.HexColor('#555555')

PAGE_W, PAGE_H = A4
FULL_W = 174 * mm  # A4 width minus 18 mm margins each side


# ── Paragraph styles ─────────────────────────────────────────────────────
def _style(name, fontSize=10, leading=14, alignment=TA_LEFT,
           textColor=colors.black, fontName=None, **kw):
    return ParagraphStyle(
        name, fontName=fontName or BASE_FONT,
        fontSize=fontSize, leading=leading, alignment=alignment,
        textColor=textColor,
        spaceAfter=kw.pop('spaceAfter', 4),
        spaceBefore=kw.pop('spaceBefore', 2),
        **kw,
    )


s_cover_title = _style('CoverTitle', fontSize=30, leading=36, alignment=TA_CENTER,
                       textColor=ACCENT_DARK, spaceAfter=4)
s_cover_sub   = _style('CoverSub', fontSize=12, leading=18, alignment=TA_CENTER,
                       textColor=GREY_TEXT, spaceAfter=20)
s_banner      = _style('Banner', fontSize=15, leading=20, alignment=TA_LEFT,
                       textColor=colors.white, spaceAfter=0, spaceBefore=0)
s_sub         = _style('Sub', fontSize=12.5, leading=17, spaceAfter=4,
                       spaceBefore=6, textColor=ACCENT_DARK)
s_body        = _style('Body', fontSize=10, leading=15)
s_small       = _style('Small', fontSize=9, leading=13)
s_large       = _style('Large', fontSize=12, leading=18)
s_th          = _style('TH', fontSize=9, leading=12, alignment=TA_CENTER,
                       textColor=colors.white, fontName=BOLD_FONT)
s_td          = _style('TD', fontSize=9, leading=12)
s_td_c        = _style('TDc', fontSize=9, leading=12, alignment=TA_CENTER)
s_note        = _style('Note', fontSize=8, leading=11, textColor=GREY_TEXT)
s_field       = _style('Field', fontSize=10, leading=16)
s_strip       = _style('Strip', fontSize=11, leading=15,
                       textColor=colors.white, fontName=BOLD_FONT, alignment=TA_CENTER)


# ── Flowable helpers ─────────────────────────────────────────────────────
def P(text, style=None):
    return Paragraph(text, style or s_body)


def SP(h=6):
    return Spacer(1, h)


def HR(color=GREY_LINE, t=0.5, after=6):
    return HRFlowable(width='100%', thickness=t, color=color, spaceAfter=after)


def note(text):
    return P(text, s_note)


def section_banner(num, text, toc=True, sep='. '):
    """Coloured banner header; registers a TOC entry when toc=True."""
    title = f'{num}{sep}{text}' if num else text
    cell = Paragraph(f'<b>{title}</b>', s_banner)
    t = Table([[cell]], colWidths=[FULL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), ACCENT),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    if toc:
        t.toc_entry = (0, title)
    return [t, SP(8)]


def sub_header(text):
    return [P(f'<b>{text}</b>', s_sub),
            HRFlowable(width='100%', thickness=0.8, color=ACCENT, spaceAfter=4)]


def cols(*weights):
    total = sum(weights)
    return [w / total * FULL_W for w in weights]


def make_table(data, col_widths=None, header_rows=1, zebra=True):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    cmds = [
        ('GRID',          (0, 0), (-1, -1), 0.5, GREY_LINE),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
        ('FONTNAME',      (0, 0), (-1, -1), BASE_FONT),
    ]
    if header_rows > 0:
        cmds += [
            ('BACKGROUND',   (0, 0), (-1, header_rows - 1), ACCENT),
            ('FONTNAME',     (0, 0), (-1, header_rows - 1), BOLD_FONT),
            ('ALIGN',        (0, 0), (-1, header_rows - 1), 'CENTER'),
            ('TEXTCOLOR',    (0, 0), (-1, header_rows - 1), colors.white),
            ('LINEBELOW',    (0, header_rows - 1), (-1, header_rows - 1), 1.4, ACCENT_DARK),
            ('TOPPADDING',   (0, 0), (-1, header_rows - 1), 6),
            ('BOTTOMPADDING',(0, 0), (-1, header_rows - 1), 6),
        ]
    if zebra:
        start = header_rows
        for r in range(start, len(data)):
            if (r - start) % 2 == 1:
                cmds.append(('BACKGROUND', (0, r), (-1, r), ACCENT_LIGHT))
    t.setStyle(TableStyle(cmds))
    return t


def fill_lines(label, n_lines=1, line_w=60):
    """Label on first line, then underscore fill lines."""
    out = [P(f'<b>{label}</b>', s_field)]
    for _ in range(n_lines):
        out.append(P('_' * line_w, s_field))
    return out


# ── Page-numbering canvas ────────────────────────────────────────────────
def make_numbered_canvas(booklet_label, version_label):
    """Return a Canvas subclass that draws an accent footer with page X / Y."""
    class _NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            canvas.Canvas.__init__(self, *args, **kwargs)
            self._saved = []

        def showPage(self):
            self._saved.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total = len(self._saved)
            for state in self._saved:
                self.__dict__.update(state)
                self._draw_footer(total)
                canvas.Canvas.showPage(self)
            canvas.Canvas.save(self)

        def _draw_footer(self, total):
            self.setStrokeColor(ACCENT)
            self.setLineWidth(0.6)
            self.line(15 * mm, 16 * mm, PAGE_W - 15 * mm, 16 * mm)
            self.setFont(BASE_FONT, 8)
            self.setFillColor(GREY_TEXT)
            self.drawString(15 * mm, 11 * mm, booklet_label)
            self.drawCentredString(PAGE_W / 2, 11 * mm, f'\u2014 {self._pageNumber} / {total} \u2014')
            self.drawRightString(PAGE_W - 15 * mm, 11 * mm, version_label)
            self.setFillColor(colors.black)

    return _NumberedCanvas


# ── TOC-aware doc template ───────────────────────────────────────────────
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'toc_entry'):
            level, label = flowable.toc_entry
            self.notify('TOCEntry', (level, label, self.page))


def toc_style():
    return ParagraphStyle('TOC1', fontName=BASE_FONT, fontSize=11, leading=22,
                          leftIndent=0, firstLineIndent=0, rightIndent=0,
                          spaceBefore=0, spaceAfter=0)


def default_output(filename):
    """Default output path relative to the repo root (this file's directory)."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
