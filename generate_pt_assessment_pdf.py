#!/usr/bin/env python3
"""Generate Geriatric PT Outcome Measures Assessment Booklet PDF (v2).

Changes vs v1:
  - Added 一、病史记录 (history-taking) section
  - Added 九-F、Berg 平衡量表 (BBS) — additional balance scale
  - Removed cover subtitle "首次评估与效果跟进 Outcome Measure 集合"
  - Visual refresh: accent-color banner headers, colored table headers,
    zebra row striping, refined cover & footer
"""

import os
import argparse
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

# ── Fonts ──
SONGTI_TTC = '/System/Library/Fonts/Supplemental/Songti.ttc'
HEITI_TTC  = '/System/Library/Fonts/STHeiti Medium.ttc'

def _register_fonts():
    """Register Chinese fonts with real bold; family name == normal name."""
    try:
        pdfmetrics.registerFont(TTFont('ChineseR', SONGTI_TTC, subfontIndex=6))  # Regular
        pdfmetrics.registerFont(TTFont('ChineseB', SONGTI_TTC, subfontIndex=1))  # Bold
        registerFontFamily('ChineseR', normal='ChineseR', bold='ChineseB',
                           italic='ChineseR', boldItalic='ChineseB')
        return 'ChineseR', 'ChineseB'
    except Exception:
        pass
    try:
        pdfmetrics.registerFont(TTFont('ChineseR', HEITI_TTC, subfontIndex=1))
        pdfmetrics.registerFont(TTFont('ChineseB', HEITI_TTC, subfontIndex=1))
        registerFontFamily('ChineseR', normal='ChineseR', bold='ChineseB',
                           italic='ChineseR', boldItalic='ChineseB')
        return 'ChineseR', 'ChineseB'
    except Exception:
        pass
    return 'Helvetica', 'Helvetica-Bold'

BASE_FONT, BOLD_FONT = _register_fonts()

# ── Palette ──
ACCENT       = colors.HexColor('#1F5C6B')   # professional teal
ACCENT_DARK  = colors.HexColor('#15414C')
ACCENT_LIGHT = colors.HexColor('#EAF1F3')   # very light tint for zebra rows
GREY_LINE    = colors.HexColor('#B8C4C8')
GREY_TEXT    = colors.HexColor('#555555')
TABLE_GREY   = colors.HexColor('#E0E0E0')

PAGE_W, PAGE_H = A4
FULL_W = 174 * mm  # A4 width minus 18mm margins each side

# ── Styles ──
def _style(name, fontSize=10, leading=14, alignment=TA_LEFT,
           textColor=colors.black, fontName=None, **kw):
    return ParagraphStyle(
        name,
        fontName=fontName or BASE_FONT,
        fontSize=fontSize, leading=leading, alignment=alignment,
        textColor=textColor,
        spaceAfter=kw.pop('spaceAfter', 4),
        spaceBefore=kw.pop('spaceBefore', 2),
        **kw,
    )

s_cover_title    = _style('CoverTitle',   fontSize=30, leading=38, alignment=TA_CENTER,
                          textColor=ACCENT_DARK, spaceAfter=4)
s_cover_sub      = _style('CoverSub',     fontSize=12, leading=18, alignment=TA_CENTER,
                          textColor=GREY_TEXT, spaceAfter=20)
s_banner         = _style('Banner',       fontSize=15, leading=20, alignment=TA_LEFT,
                          textColor=colors.white, spaceAfter=0, spaceBefore=0)
s_sub            = _style('Sub',          fontSize=12.5, leading=17, spaceAfter=4,
                          spaceBefore=6, textColor=ACCENT_DARK)
s_body           = _style('Body',         fontSize=10, leading=15)
s_small          = _style('Small',        fontSize=9,  leading=13)
s_large          = _style('Large',        fontSize=12, leading=18)
s_th             = _style('TH',           fontSize=9,  leading=12, alignment=TA_CENTER,
                          textColor=colors.white, fontName=BOLD_FONT)
s_td             = _style('TD',           fontSize=9,  leading=12)
s_td_c           = _style('TDc',          fontSize=9,  leading=12, alignment=TA_CENTER)
s_note           = _style('Note',         fontSize=8,  leading=11, textColor=GREY_TEXT)
s_field          = _style('Field',        fontSize=10, leading=16)
s_strip          = _style('Strip',        fontSize=11, leading=15,
                          textColor=colors.white, fontName=BOLD_FONT, alignment=TA_CENTER)

# ── Helpers ──
def P(text, style=None): return Paragraph(text, style or s_body)
def SP(h=6):             return Spacer(1, h)
def HR(color=GREY_LINE, t=0.5, after=6):
    return HRFlowable(width='100%', thickness=t, color=color, spaceAfter=after)

def section_banner(num, text, toc=True):
    """Colored banner header for a section. toc=True registers a TOC entry."""
    title = f'{num}、{text}' if num else text
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

def note(text):  return P(text, s_note)

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
            ('BACKGROUND', (0, 0), (-1, header_rows - 1), ACCENT),
            ('FONTNAME',   (0, 0), (-1, header_rows - 1), BOLD_FONT),
            ('ALIGN',      (0, 0), (-1, header_rows - 1), 'CENTER'),
            ('TEXTCOLOR',  (0, 0), (-1, header_rows - 1), colors.white),
            ('LINEBELOW',  (0, header_rows - 1), (-1, header_rows - 1), 1.4, ACCENT_DARK),
            ('TOPPADDING', (0, 0), (-1, header_rows - 1), 6),
            ('BOTTOMPADDING',(0,0), (-1, header_rows - 1), 6),
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

# ── Page numbering canvas with accent footer ──
class NumberedCanvas(canvas.Canvas):
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
        # accent rule above footer
        self.setStrokeColor(ACCENT)
        self.setLineWidth(0.6)
        self.line(15 * mm, 16 * mm, PAGE_W - 15 * mm, 16 * mm)
        self.setFont(BASE_FONT, 8)
        self.setFillColor(GREY_TEXT)
        self.drawString(15 * mm, 11 * mm, '老年物理治疗评估工具手册')
        self.drawCentredString(PAGE_W / 2, 11 * mm, f'— {self._pageNumber} / {total} —')
        self.drawRightString(PAGE_W - 15 * mm, 11 * mm, '版本 3.0  |  2026')
        self.setFillColor(colors.black)


class TocDocTemplate(SimpleDocTemplate):
    """SimpleDocTemplate that collects section page numbers for the TOC."""
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'toc_entry'):
            level, label = flowable.toc_entry
            self.notify('TOCEntry', (level, label, self.page))


# ═══════════════════════════════════════════════════════════════════════════
#  DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════

def build_story():
    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    story.append(SP(35 * mm))
    story.append(P('老年物理治疗评估工具手册', s_cover_title))
    story.append(SP(4))
    # decorative double rule
    story.append(HRFlowable(width='55%', thickness=2, color=ACCENT,
                            hAlign='CENTER', spaceAfter=3))
    story.append(HRFlowable(width='40%', thickness=0.6, color=ACCENT,
                            hAlign='CENTER', spaceAfter=18))
    story.append(P('Geriatric Physical Therapy Outcome Measures', s_cover_sub))
    story.append(SP(8))

    info = [
        [P('患者基本信息', s_strip), '', '', ''],
        [P('<b>姓  名</b>', s_large), P('_________________', s_large),
         P('<b>性  别</b>', s_large), P('□ 男   □ 女', s_large)],
        [P('<b>年  龄</b>', s_large), P('_________________', s_large),
         P('<b>诊  断</b>', s_large), P('_________________', s_large)],
        [P('<b>评估日期</b>', s_large), P('_________________', s_large),
         P('<b>治 疗 师</b>', s_large), P('_________________', s_large)],
    ]
    info_tbl = Table(info, colWidths=cols(4, 7, 4, 7))
    info_tbl.setStyle(TableStyle([
        ('SPAN',         (0, 0), (-1, 0)),
        ('BACKGROUND',   (0, 0), (-1, 0), ACCENT),
        ('BACKGROUND',   (0, 1), (-1, -1), ACCENT_LIGHT),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',   (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING',(0, 0), (-1, 0), 6),
        ('TOPPADDING',   (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING',(0, 1), (-1, -1), 9),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX',          (0, 0), (-1, -1), 0.8, ACCENT),
        ('LINEBELOW',    (0, 1), (-1, -2), 0.3, GREY_LINE),
    ]))
    story.append(info_tbl)
    story.append(SP(14))
    story.append(P('评估类型：  □ 首次评估　　　□ 后续跟进（第 ___ 次）', s_large))
    story.append(SP(20))
    story.append(P('本手册整合了国际通用、经验证适用于老年人群的主观与客观评估工具，', s_small))
    story.append(P('便于临床操作与治疗效果追踪。各量表均附有评分说明与临床意义解读。', s_small))
    story.append(PageBreak())

    # ── 目录 ─────────────────────────────────────────────────────────────────
    story.extend(section_banner('', '目  录', toc=False))
    story.append(SP(6))
    toc = TableOfContents()
    toc.dotsMinLevel = 0
    toc.levelStyles = [
        ParagraphStyle('TOC1', fontName=BASE_FONT, fontSize=11, leading=22,
                       leftIndent=0, firstLineIndent=0, rightIndent=0,
                       spaceBefore=0, spaceAfter=0),
    ]
    story.append(toc)
    story.append(PageBreak())

    # ── 一、病史记录 ─────────────────────────────────────────────────────────
    story.extend(section_banner('一', '病史记录'))
    story.append(SP(4))

    story.extend(sub_header('主诉'))
    story.append(P('起病时间：__________   部位：__________   性质：□钝痛 □刺痛 □酸胀 □麻木 □其他____', s_field))
    story.append(P('持续 / 间歇：□持续 □间歇    加重因素：________________    缓解因素：________________', s_field))
    story.append(SP(4))

    story.extend(sub_header('现病史'))
    for _ in range(3):
        story.append(P('_' * 64, s_field))
    story.append(SP(4))

    story.extend(sub_header('既往史（可多选）'))
    pmh = [
        '□ 高血压', '□ 糖尿病', '□ 冠心病', '□ 心律失常', '□ 骨质疏松',
        '□ 脑卒中', '□ 帕金森病', '□ 关节炎', '□ 慢性肺病', '□ 视力/听力下降',
        '□ 认知障碍', '□ 泌尿系统疾病', '□ 其他：____________',
    ]
    # render in 2 columns via table
    pmh_rows = []
    for i in range(0, len(pmh), 2):
        left = P(pmh[i], s_field)
        right = P(pmh[i+1] if i+1 < len(pmh) else '', s_field)
        pmh_rows.append([left, right])
    pmh_tbl = Table(pmh_rows, colWidths=cols(1, 1))
    pmh_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(pmh_tbl)
    story.append(SP(4))

    story.extend(sub_header('跌倒史（过去 12 个月）'))
    fall = [
        [P('跌倒次数', s_td), P('□ 0 次   □ 1 次   □ 2 次以上（____次）', s_td),
         P('受伤情况', s_td), P('□ 无 □ 软组织伤 □ 骨折 □ 头部外伤', s_td)],
        [P('跌倒恐惧', s_td), P('□ 无 □ 轻度 □ 中度 □ 重度（限制活动）', s_td),
         P('求助情况', s_td), P('□ 可自行起身 □ 需他人协助', s_td)],
    ]
    story.append(make_table(fall, col_widths=cols(2, 5, 2, 5), header_rows=0, zebra=False))
    story.append(SP(4))

    story.extend(sub_header('用药与手术史'))
    story.append(P('长期用药：□ 抗凝药  □ 降压药  □ 降糖药  □ 镇静/安眠药  □ 镇痛药  □ 其他：____________', s_field))
    story.append(P('手术史：____________________________________________________________________', s_field))
    story.append(SP(4))

    story.extend(sub_header('生活与功能状况'))
    life = [
        [P('居住情况', s_td), P('□ 独居 □ 与家人同住 □ 机构', s_td),
         P('辅助器具', s_td), P('□ 无 □ 拐杖 □ 助行器 □ 轮椅', s_td)],
        [P('运动习惯', s_td), P('□ 无 □ 偶尔 □ 规律（____次/周）', s_td),
         P('吸烟/饮酒', s_td), P('□ 无 □ 吸烟 □ 饮酒', s_td)],
        [P('既往康复', s_td), P('□ 无 □ 有：____________', s_td),
         P('患者期望', s_td), P('________________________', s_td)],
    ]
    story.append(make_table(life, col_widths=cols(2, 5, 2, 5), header_rows=0))
    story.append(SP(4))

    story.extend(sub_header('过敏史与家族史'))
    story.append(P('过敏史：□ 无  □ 药物（________）  □ 食物/其他（________）', s_field))
    story.append(P('家族史：□ 无特殊  □ 有：________（如骨质疏松、心脑血管病、退行性神经病等）', s_field))
    story.append(SP(4))

    story.extend(sub_header('红旗征筛查（任一阳性需警惕，必要时转介）'))
    redflag = [
        [P('□ 夜间剧痛 / 休息痛', s_td), P('□ 不明原因体重下降 > 5 kg', s_td)],
        [P('□ 近期外伤 / 跌倒史', s_td), P('□ 持续发热 / 盗汗', s_td)],
        [P('□ 肠道 / 膀胱功能改变', s_td), P('□ 既往恶性肿瘤史', s_td)],
        [P('□ 进行性肌无力 / 萎缩', s_td), P('□ 凝血异常 / 长期抗凝', s_td)],
    ]
    rf_tbl = Table(redflag, colWidths=cols(1, 1))
    rf_tbl.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    story.append(rf_tbl)
    story.append(SP(4))

    story.extend(sub_header('神经系统症状'))
    neuro = [
        [P('麻木/刺痛', s_td), P('□ 无  □ 上肢  □ 下肢  □ 其他____', s_td),
         P('肌力下降', s_td), P('□ 无  □ 上肢  □ 下肢', s_td)],
        [P('头晕/眩晕', s_td), P('□ 无  □ 偶发  □ 频发  □ 体位相关', s_td),
         P('视力变化', s_td), P('□ 无  □ 复视  □ 模糊', s_td)],
        [P('言语/吞咽', s_td), P('□ 无  □ 有：________', s_td),
         P('步态异常', s_td), P('□ 无  □ 拖步  □ 摇摆', s_td)],
    ]
    story.append(make_table(neuro, col_widths=cols(2, 5, 2, 5), header_rows=0))
    story.append(SP(4))

    story.extend(sub_header('日常生活活动（ADL）基线'))
    adl = [
        [P('<b>项目</b>', s_th), P('<b>独立</b>', s_th),
         P('<b>需部分协助</b>', s_th), P('<b>完全依赖</b>', s_th)],
        ['进食', '□', '□', '□'],
        ['洗澡', '□', '□', '□'],
        ['穿衣', '□', '□', '□'],
        ['如厕', '□', '□', '□'],
        ['床椅转移', '□', '□', '□'],
        ['平地行走', '□', '□', '□'],
        ['上下楼梯', '□', '□', '□'],
        ['购物/做饭（IADL）', '□', '□', '□'],
    ]
    story.append(make_table(adl, col_widths=cols(4, 2, 3, 3)))
    story.append(SP(4))

    story.extend(sub_header('居家环境与康复目标'))
    env = [
        [P('居家风险', s_td), P('□ 地毯/门槛易绊倒  □ 卫生间无扶手  □ 照明不足  □ 楼梯陡峭  □ 无', s_td)],
        [P('SMART 目标', s_td), P('____________________________________________________', s_td)],
    ]
    story.append(make_table(env, col_widths=cols(1, 9), header_rows=0))
    story.append(PageBreak())

    # ── 二、NPRS ─────────────────────────────────────────────────────────────
    story.extend(section_banner('二', '数字疼痛评定量表（NPRS）'))
    story.append(P('请患者用 0–10 的数值描述疼痛程度。0 = 无痛，10 = 所能想象的最剧烈疼痛。'))
    story.append(SP(6))

    pain_scale = [
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        ['无痛', '', '', '', '', '中度', '', '', '', '', '最剧烈'],
    ]
    pt = Table(pain_scale, colWidths=[FULL_W / 11] * 11)
    pt.setStyle(TableStyle([
        ('GRID',       (0, 0), (-1, -1), 0.5, GREY_LINE),
        ('BACKGROUND', (0, 0), (-1, 0),  ACCENT),
        ('TEXTCOLOR',  (0, 0), (-1, 0),  colors.white),
        ('FONTNAME',   (0, 0), (-1, 0),  BOLD_FONT),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME',   (0, 1), (-1, 1),  BASE_FONT),
        ('FONTSIZE',   (0, 0), (-1, 0),  13),
        ('FONTSIZE',   (0, 1), (-1, 1),  9),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
    ]))
    story.append(pt)
    story.append(SP(10))

    pain_rec = [
        [P('<b>时间点</b>', s_th), P('<b>疼痛评分（0–10）</b>', s_th)],
        ['现在（静息时）', ''],
        ['过去24小时内最轻', ''],
        ['过去24小时内最重', ''],
        ['活动时', ''],
    ]
    story.append(make_table(pain_rec, col_widths=cols(3, 2)))
    story.append(SP(8))

    story.extend(sub_header('疼痛部位标记图'))
    story.append(P('请在图中标记疼痛部位（阴影 = 疼痛，X = 最痛点）：'))
    body_diag = [
        [P('<b>前 面</b>', s_td_c), P('<b>后 面</b>', s_td_c)],
        [P('（患者在此区域标注疼痛位置）', s_note),
         P('（患者在此区域标注疼痛位置）', s_note)],
    ]
    bt = Table(body_diag, colWidths=cols(1, 1), rowHeights=[18, 180])
    bt.setStyle(TableStyle([
        ('GRID',       (0, 0), (-1, -1), 0.5, GREY_LINE),
        ('VALIGN',     (0, 0), (-1, 0),  'MIDDLE'),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0),  ACCENT_LIGHT),
        ('FONTNAME',   (0, 0), (-1, -1), BASE_FONT),
    ]))
    story.append(bt)
    story.append(SP(4))
    story.append(note('MCID：疼痛降低 ≥ 2 分视为有效改善。'))
    story.append(PageBreak())

    # ── 三、EQ-5D-5L ─────────────────────────────────────────────────────────
    story.extend(section_banner('三', '欧洲五维健康量表（EQ-5D-5L）'))
    story.append(P('请在以下每个维度中，勾选最能描述您<b>今天</b>健康状况的那一项：'))
    story.append(SP(6))

    eq_dims = [
        ('行动能力', ['我可以四处走动，没有困难','我四处走动有一些困难','我四处走动有中度的困难',
                      '我四处走动有严重的困难','我因健康问题无法四处走动']),
        ('自我照顾', ['我自己洗澡或穿衣没有困难','我自己洗澡或穿衣有一些困难','我自己洗澡或穿衣有中度的困难',
                      '我自己洗澡或穿衣有严重的困难','我无法自己洗澡或穿衣']),
        ('日常活动', ['我进行日常活动没有困难（如工作、学习、家务、休闲活动）','我进行日常活动有一些困难',
                      '我进行日常活动有中度的困难','我进行日常活动有严重的困难','我无法进行日常活动']),
        ('疼痛或不适', ['我没有疼痛或不适','我有一些疼痛或不适','我有中度的疼痛或不适',
                        '我有严重的疼痛或不适','我有非常严重的疼痛或不适']),
        ('焦虑或抑郁', ['我没有焦虑或抑郁','我有一点焦虑或抑郁','我有中度的焦虑或抑郁',
                        '我有严重的焦虑或抑郁','我有非常严重的焦虑或抑郁']),
    ]
    for dim_name, opts in eq_dims:
        story.append(P(f'<b>{dim_name}</b>', s_large))
        for opt in opts:
            story.append(P(f'　　□  {opt}'))
        story.append(SP(2))

    story.append(SP(8))
    story.append(note('EQ-5D-5L 五维组合可转化为健康效用指数（0–1）。MCID：效用值 ↑ 0.05–0.08。'))
    story.append(PageBreak())

    # ── 五、握力 ─────────────────────────────────────────────────────────────

    # ── 四、握力 ─────────────────────────────────────────────────────────────
    story.extend(section_banner('四', '握力测试（Handgrip Strength）'))
    story.append(P('<b>仪器：</b>Jamar 或同等液压握力计，调整至第二档位。'))
    story.append(P('<b>体位：</b>坐位，肩内收中立位，肘屈 90°，前臂中立位，腕 0–30° 背伸。'))
    story.append(P('<b>方法：</b>左右手交替，各测 3 次，每次间隔 ≥ 30 秒。鼓励最大用力。'))
    story.append(SP(8))
    grip = [
        [P('', s_th), P('<b>第 1 次 (kg)</b>', s_th), P('<b>第 2 次 (kg)</b>', s_th),
         P('<b>第 3 次 (kg)</b>', s_th), P('<b>最佳值 (kg)</b>', s_th)],
        [P('<b>左手</b>', s_td_c), '', '', '', ''],
        [P('<b>右手</b>', s_td_c), '', '', '', ''],
        [P('<b>双手均值</b>', s_td_c), '—', '—', '—', ''],
    ]
    story.append(make_table(grip, col_widths=cols(3, 4, 4, 4, 4)))
    story.append(SP(8))
    story.extend(sub_header('参考值（亚洲人群 AWGS 2019）'))
    cutoff = [
        [P('<b>性别</b>', s_th), P('<b>肌少症风险截断值</b>', s_th), P('<b>备注</b>', s_th)],
        ['男性', '< 26 kg', ''],
        ['女性', '< 18 kg', ''],
    ]
    story.append(make_table(cutoff, col_widths=cols(2, 4, 5)))
    story.append(SP(4))
    story.append(P('<b>MCID：</b>握力增加 ≥ 5–6 kg 视为有临床意义的改善。'))
    story.append(PageBreak())

    # ── 五、SPPB ─────────────────────────────────────────────────────────────
    story.extend(section_banner('五', '简易体能状况量表（SPPB）'))
    story.append(P('SPPB 包含三个子测试，总分 0–12 分。≤ 8 分提示衰弱 / 高跌倒风险。'))
    story.append(SP(6))

    # ── 客观测试通用安全守则（适用于 SPPB / TUG / BBS / 2MST）──
    safety = [
        [P('<b>客观测试通用安全守则</b>', s_td)],
        [P('• 治疗师全程站于患者侧后方近身保护，防止跌倒。', s_small)],
        [P('• 出现胸痛胸闷、严重呼吸困难、头晕/共济失调、大汗苍白、SpO<sub>2</sub> &lt; 85% 或患者要求停止 → 立即终止测试。', s_small)],
        [P('• 耐力测试（2MST）前：静息 SBP &gt; 180 或 DBP &gt; 110、SpO<sub>2</sub> &lt; 90% → 暂缓。', s_small)],
    ]
    sf_tbl = Table(safety, colWidths=[FULL_W])
    sf_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), ACCENT_LIGHT),
        ('BOX',           (0, 0), (-1, -1), 0.8, ACCENT),
        ('BACKGROUND',    (0, 0), (0, 0),   ACCENT),
        ('TEXTCOLOR',     (0, 0), (0, 0),   colors.white),
        ('FONTNAME',      (0, 0), (0, 0),   BOLD_FONT),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('TOPPADDING',    (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(sf_tbl)
    story.append(SP(8))

    story.extend(sub_header('A. 站立平衡测试'))
    story.append(P('<b>要求：</b>患者不使用辅助器具站立。每项计时最多 10 秒。'))
    bal = [
        [P('<b>测试姿势</b>', s_th), P('<b>能否完成</b>', s_th),
         P('<b>计时（秒）</b>', s_th), P('<b>得分</b>', s_th)],
        ['1. 双脚并拢站立', '□ 能 / □ 不能', '', '□ 0分 / □ 1分'],
        ['2. 半串联站立\n（一脚脚跟放在另一脚大脚趾旁）', '□ 能 / □ 不能', '', '□ 0分 / □ 1分'],
        [P('3. 串联站立\n（一脚脚跟紧贴另一脚脚尖）', s_td), '□ 能 / □ 不能',
         P('10秒=2分\n3–9.99秒=1分\n<3秒=0分\n记录秒数：____ 秒', s_small),
         P('□ 2分\n□ 1分\n□ 0分', s_small)],
    ]
    story.append(make_table(bal, col_widths=cols(4, 3, 3, 3)))
    story.append(note('如姿势 1 不能 → 0 分停止；如姿势 2 不能 → 1 分，进入步行测试。'))
    story.append(SP(8))

    story.extend(sub_header('B. 4米步行速度测试'))
    story.append(P('<b>要求：</b>以平常速度行走 4 米（可用辅助器具），测 2 次，取较快一次。'))
    gait = [[P('', s_th), P('<b>第 1 次</b>', s_th), P('<b>第 2 次</b>', s_th)],
            ['步行时间（秒）', '', '']]
    story.append(make_table(gait, col_widths=cols(1, 1, 1)))
    story.append(SP(4))
    gait_score = [
        [P('<b>时间</b>', s_th), P('<b>≤ 4.82 秒</b>', s_th), P('<b>4.83–6.20 秒</b>', s_th),
         P('<b>6.21–8.70 秒</b>', s_th), P('<b>> 8.70 秒</b>', s_th), P('<b>不能</b>', s_th)],
        ['得分', '4 分', '3 分', '2 分', '1 分', '0 分'],
    ]
    story.append(make_table(gait_score, col_widths=cols(2, 3, 3.5, 3.5, 3, 2)))
    story.append(SP(2))
    story.append(P('步行速度得分：________ 分'))
    story.append(SP(8))

    story.extend(sub_header('C. 5次坐站测试'))
    story.append(P('<b>要求：</b>双手交叉抱于胸前，从标准椅子（座高约 43–45 cm）完全站起再坐下，重复 5 次，计时。'))
    story.append(P('预备测试：先做 1 次看是否能独立完成。'))
    story.append(SP(4))
    chair_yn = [['能否完成？', '□ 能  完成时间：________ 秒', '□ 不能 → 0 分']]
    story.append(make_table(chair_yn, col_widths=cols(2, 7, 3), header_rows=0, zebra=False))
    chair_score = [
        [P('<b>时间</b>', s_th), P('<b>≤ 11.19 秒</b>', s_th), P('<b>11.20–13.69 秒</b>', s_th),
         P('<b>13.70–16.69 秒</b>', s_th), P('<b>16.70–59.99 秒</b>', s_th), P('<b>> 60 秒</b>', s_th)],
        ['得分', '4 分', '3 分', '2 分', '1 分', '0 分'],
    ]
    story.append(make_table(chair_score, col_widths=cols(2, 3, 3.5, 3.5, 3, 2)))
    story.append(SP(2))
    story.append(P('坐站测试得分：________ 分'))
    story.append(SP(8))
    sppb_total = [
        [P('<b>子测试</b>', s_th), P('<b>A. 平衡（0–4）</b>', s_th),
         P('<b>B. 步行速度（0–4）</b>', s_th), P('<b>C. 坐站（0–4）</b>', s_th),
         P('<b>SPPB 总分（0–12）</b>', s_th)],
        ['得分', '', '', '', ''],
    ]
    story.append(make_table(sppb_total, col_widths=cols(3, 3.5, 4, 3.5, 4)))
    story.append(SP(6))
    story.extend(sub_header('SPPB 解读'))
    story.append(P('• <b>0–3 分</b>：严重受限，跌倒高风险　• <b>4–6 分</b>：中度受限'))
    story.append(P('• <b>7–9 分</b>：轻度受限　• <b>10–12 分</b>：功能良好'))
    story.append(P('• <b>MCID：≥ 1.0 分</b>'))
    story.append(PageBreak())

    # ── 六、TUG ──────────────────────────────────────────────────────────────
    story.extend(section_banner('六', '起立行走计时测试（TUG）'))
    story.extend(sub_header('操作步骤'))
    for s in [
        '1. 患者坐在标准扶手椅（座高约 45 cm），背靠椅背。',
        '2. 在椅子前方 3 米处地面放置标记物（胶带或锥桶）。',
        '3. 指令：「我喊"开始"后，请您站起来，以安全且尽可能快的速度走到 3 米标记处，转身，走回椅子，再坐下。」',
        '4. 计时从说"开始"到患者臀部再次接触椅面。',
        '5. 先做 1 次练习，再做 1–2 次计时测试，取最佳成绩。',
        '6. 患者可使用日常辅助器具（如拐杖）。',
    ]:
        story.append(P(s))
    story.append(SP(6))
    tug = [
        [P('', s_th), P('<b>时间（秒）</b>', s_th), P('<b>使用辅具？</b>', s_th), P('<b>备注</b>', s_th)],
        ['练习（不计分）', '', '□ 是 / □ 否', ''],
        ['计时 1', '', '□ 是 / □ 否', ''],
        ['计时 2（可选）', '', '□ 是 / □ 否', ''],
        [P('<b>最佳成绩</b>', s_td), '', '', ''],
    ]
    story.append(make_table(tug, col_widths=cols(3, 3.5, 3, 4.5)))
    story.append(SP(8))
    story.extend(sub_header('解读标准'))
    for txt in [
        '• <b>< 10 秒</b>：正常，可独立自由移动',
        '• <b>10–19 秒</b>：基本独立，但步行和平衡可能有轻度障碍',
        '• <b>≥ 13.5 秒</b>：跌倒风险增高',
        '• <b>≥ 20 秒</b>：明显移动障碍，需要干预',
        '• <b>≥ 30 秒</b>：严重功能障碍，日常生活需要协助',
    ]:
        story.append(P(txt))
    story.append(SP(4))
    story.append(P('<b>MCID：</b>TUG 时间缩短 ≥ 2–3 秒视为有临床意义的改善。'))
    story.append(PageBreak())

    # ── 七、2MST（居家适用，替代 2MWT） ─────────────────────────────────────
    story.extend(section_banner('七', '2分钟原地踏步测试（2MST）— 居家适用'))
    story.append(P('2MST 是 2MWT/6MWT 在<b>空间受限</b>（如居家）时的公认替代方案，仅需立足之地，'
                   '用于评估有氧耐力与下肢耐力。源自 Senior Fitness Test。'))
    story.append(SP(6))
    story.extend(sub_header('场地与器材'))
    for txt in [
        '• 立足之地即可（墙边或稳固椅旁），无需长走道。',
        '• 秒表、墙面胶带或弹力带（用于标记抬膝高度）。',
        '• 血压计、脉搏血氧仪、Borg 量表（RPE 6–20）。',
        '• 稳固座椅 / 助行器供患者单手轻扶维持平衡（仅平衡，不借力上提）。',
    ]:
        story.append(P(txt))
    story.append(SP(6))
    story.extend(sub_header('抬膝高度标记'))
    story.append(P('取<b>髌骨上缘与髂嵴之间中点</b>的高度，在墙面贴胶带，或用弹力带系于两椅之间作参照。'
                   '患者每次踏步需将一侧膝抬至此高度方计为有效步数。'))
    story.append(SP(6))
    story.extend(sub_header('测试前评估'))
    pre = [
        [P('<b>指标</b>', s_th), P('<b>数值</b>', s_th), P('<b>备注</b>', s_th)],
        ['静息心率（HR）', '________ 次/分', '正常 60–100'],
        ['血压（BP）', '________ / ________ mmHg', '静息 SBP > 180 暂缓'],
        [P('血氧饱和度（SpO<sub>2</sub>）', s_td), '________ %', '如 < 90% 需谨慎'],
        ['Borg RPE（静息）', '________ (6–20)', ''],
    ]
    story.append(make_table(pre, col_widths=cols(6, 7, 7)))
    story.append(SP(6))
    story.extend(sub_header('操作指令'))
    story.append(P('"请原地踏步 2 分钟，每次抬膝尽量达到标记高度。目标是 2 分钟内尽可能多地完成正确抬步次数。'
                   '中途可放慢或停顿休息，但计时不停。准备好了吗？开始！"'))
    story.append(SP(4))
    story.append(P('• <b>计数：</b>每完成一次达标抬膝计 1 步（通常计一侧，如右膝），记录 2 分钟总步数。'))
    story.append(P('• 每 30 秒提示时间并标准化鼓励；2 分钟到 → "停！" 记录总步数。'))
    story.append(P('• 测试者须站在患者侧后方保护，防止跌倒。'))
    story.append(SP(8))
    story.extend(sub_header('测试结果'))
    res = [['2 分钟总步数', '________ 步', '达标抬膝高度：________ cm']]
    story.append(make_table(res, col_widths=cols(2, 4, 3), header_rows=0, zebra=False))
    story.append(SP(6))
    story.extend(sub_header('测试后评估'))
    post = [
        [P('<b>指标</b>', s_th), P('<b>数值</b>', s_th), P('<b>备注</b>', s_th)],
        ['心率（HR）', '________ 次/分', ''],
        ['血压（BP）', '________ / ________ mmHg', ''],
        [P('SpO<sub>2</sub>', s_td), '________ %', '如 < 88% 或下降 > 4% 需关注'],
        ['Borg RPE（用力后）', '________ (6–20)', ''],
        ['Borg 呼吸困难', '________ (0–10)', '改良 Borg 呼吸困难量表'],
    ]
    story.append(make_table(post, col_widths=cols(6, 7, 7)))
    story.append(SP(8))
    story.extend(sub_header('年龄与性别参考值（步数，约第 50 百分位）'))
    ref2mst = [
        [P('<b>年龄段</b>', s_th), P('<b>男性（步）</b>', s_th), P('<b>女性（步）</b>', s_th)],
        ['60–69 岁', '85–95', '75–87'],
        ['70–79 岁', '75–87', '65–80'],
        ['80–89 岁', '60–76', '55–68'],
    ]
    story.append(make_table(ref2mst, col_widths=cols(1, 1, 1)))
    story.append(SP(4))
    story.append(P('• <b>明显低于参考值</b> 提示有氧耐力下降，跌倒与失能风险增高。'))
    story.append(P('• <b>MCID：</b>研究尚不统一，建议以改善 ≥ 10 步（或基线的 ~10%）作为参考阈值。'))
    story.append(PageBreak())

    # ── 八-A、ODI ────────────────────────────────────────────────────────────
    story.extend(section_banner('八-A', 'Oswestry 功能障碍指数（ODI）— 腰痛专用'))
    story.append(P('请在每个问题中选择<b>最符合您今天状况</b>的一项。'))
    story.append(SP(6))
    odi_secs = [
        ('1. 疼痛强度', ['（0）我目前不觉得疼痛。','（1）目前疼痛非常轻微。','（2）目前有中度疼痛。',
            '（3）目前疼痛相当严重。','（4）目前疼痛非常严重。','（5）目前疼痛是所能想象的最严重的。']),
        ('2. 自我照顾（洗漱、穿衣等）', ['（0）我能正常照顾自己，不会引起疼痛加重。','（1）我能正常照顾自己，但会引起疼痛加重。',
            '（2）自我照顾时疼痛，我需要缓慢小心地活动。','（3）自我照顾需要一些帮助，但大部分能自己完成。',
            '（4）每天自我照顾的大部分需要帮助。','（5）无法自己穿衣、洗漱，需卧床。']),
        ('3. 提物', ['（0）能提起重物且不加重疼痛。','（1）能提起重物但会加重疼痛。',
            '（2）疼痛使我不能从地面提起重物，但位置方便时可以。','（3）疼痛使我不能提重物，但位置方便时能提轻至中等重量物品。',
            '（4）我只能提起非常轻的物品。','（5）我不能提起或搬运任何物品。']),
        ('4. 行走', ['（0）疼痛不影响行走距离。','（1）疼痛使我步行不超过 1.6 公里（约 20 分钟）。',
            '（2）疼痛使我步行不超过 800 米。','（3）疼痛使我步行不超过 400 米。','（4）我只能借助拐杖行走。',
            '（5）我大部分时间卧床，上厕所都很困难。']),
        ('5. 坐', ['（0）我能长时间坐在任何椅子上。','（1）我只能在我的专用椅子上长时间坐。','（2）疼痛使我坐不超过 1 小时。',
            '（3）疼痛使我坐不超过 30 分钟。','（4）疼痛使我坐不超过 10 分钟。','（5）疼痛使我完全不能坐。']),
        ('6. 站', ['（0）我能站任意长时间而不会加重疼痛。','（1）我能站任意长时间但会加重疼痛。','（2）疼痛使我站不超过 1 小时。',
            '（3）疼痛使我站不超过 30 分钟。','（4）疼痛使我站不超过 10 分钟。','（5）疼痛使我完全不能站。']),
        ('7. 睡眠', ['（0）疼痛不影响我的睡眠。','（1）疼痛偶尔影响睡眠。','（2）由于疼痛，睡眠时间不足 6 小时。',
            '（3）由于疼痛，睡眠时间不足 4 小时。','（4）由于疼痛，睡眠时间不足 2 小时。','（5）疼痛使我完全无法入睡。']),
        ('8. 性生活（如适用）', ['（0）性生活正常，不加重疼痛。','（1）性生活正常，但会加重疼痛。','（2）性生活接近正常，但明显疼痛。',
            '（3）疼痛严重限制性生活。','（4）疼痛使性生活近乎不可能。','（5）疼痛使性生活完全不可能。']),
        ('9. 社交生活', ['（0）社交生活正常，不加重疼痛。','（1）社交生活正常，但疼痛程度增加。',
            '（2）疼痛对社交生活无显著影响，只限制较剧烈的活动（如运动）。','（3）疼痛限制了我的社交生活，我不能频繁外出。',
            '（4）疼痛使我的社交生活仅限于家中。','（5）疼痛使我完全没有社交生活。']),
        ('10. 出行/旅行', ['（0）我能外出旅行而不加重疼痛。','（1）我能外出旅行但疼痛会加重。','（2）疼痛虽重，但能完成 2 小时以上的行程。',
            '（3）疼痛限制我只能完成 1 小时以内的行程。','（4）疼痛限制我只能完成 30 分钟以内的必要出行。','（5）除了去医院就诊，我不能外出。']),
    ]
    for title, stmts in odi_secs:
        story.append(P(f'<b>{title}</b>', s_large))
        for s in stmts:
            story.append(P(f'　　□  {s}', s_small))
        story.append(SP(2))
    story.append(SP(6))
    story.extend(sub_header('ODI 评分'))
    story.append(P('<b>总分：</b>________ / 50'))
    story.append(P('<b>ODI% = (总分 ÷ 50) × 100 = </b>________ %'))
    story.append(P('（如性生活项目不适用，则总分 ÷ 45 × 100）'))
    story.append(SP(4))
    story.append(P('<b>解读：</b>0–20% 轻度  |  21–40% 中度  |  41–60% 重度  |  61–80% 伤残  |  81–100% 卧床'))
    story.append(P('<b>MCID：</b>ODI% 降低 ≥ 10 个百分点视为显著改善。'))
    story.append(PageBreak())

    # ── 八-B、QuickDASH ──────────────────────────────────────────────────────
    story.extend(section_banner('八-B', 'QuickDASH 上肢功能评估'))
    story.append(P('请根据<b>过去一周</b>的状况回答。即使左右手程度不同，也请以整体功能作答。'))
    story.append(SP(6))
    story.extend(sub_header('困难程度（1=无困难，5=不能完成）'))
    qdash_items = [
        '1. 拧开已拧紧的或新的瓶盖','2. 做较重的家务（如擦地板、擦窗户）','3. 提购物袋或公文包',
        '4. 清洗背部','5. 用刀切食物','6. 需要上肢力量或冲击力的娱乐活动（如打羽毛球、打网球）',
    ]
    qd_rows = [[P('<b>项目</b>', s_th), P('<b>1\n无困难</b>', s_th), P('<b>2\n有一点困难</b>', s_th),
                P('<b>3\n中度困难</b>', s_th), P('<b>4\n很大困难</b>', s_th), P('<b>5\n不能完成</b>', s_th)]]
    for item in qdash_items:
        qd_rows.append([P(item, s_td)] + [P('□', s_td_c)] * 5)
    qd_tbl = Table(qd_rows, colWidths=cols(7, 2, 2, 2, 2, 2))
    qd_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),8),
        ('LEADING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    for r in range(1, len(qd_rows)):
        if r % 2 == 0:
            qd_tbl.setStyle(TableStyle([('BACKGROUND',(0,r),(-1,r),ACCENT_LIGHT)]))
    story.append(qd_tbl)
    story.append(SP(8))
    story.extend(sub_header('症状严重程度（过去一周）'))
    symp_items = ['7. 上肢（肩、臂、手）疼痛程度？','8. 当进行某项具体活动时，上肢的疼痛程度？','9. 上肢的麻木或刺痛感（针刺样感觉）程度？']
    sy_rows = [[P('<b>项目</b>', s_th), P('<b>1\n没有</b>', s_th), P('<b>2\n轻微</b>', s_th),
                P('<b>3\n中度</b>', s_th), P('<b>4\n重度</b>', s_th), P('<b>5\n极度</b>', s_th)]]
    for item in symp_items:
        sy_rows.append([P(item, s_td)] + [P('□', s_td_c)] * 5)
    sy_tbl = Table(sy_rows, colWidths=cols(7, 2, 2, 2, 2, 2))
    sy_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),8),
        ('LEADING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(sy_tbl)
    story.append(SP(6))
    story.extend(sub_header('影响（过去一周）'))
    extra = [
        [P('10. 上肢问题是否影响您的工作或日常活动？', s_td),
         P('□ 没有影响  □ 轻度  □ 中度  □ 重度  □ 极度', s_td)],
        [P('11. 上肢问题是否影响您的睡眠？', s_td),
         P('□ 没有影响  □ 轻度  □ 中度  □ 重度  □ 极度', s_td)],
    ]
    story.append(make_table(extra, col_widths=cols(1, 1), header_rows=0, zebra=False))
    story.append(SP(8))
    story.extend(sub_header('评分'))
    story.append(P('<b>QuickDASH = [(各项分数之和 ÷ 项目数) − 1] × 25 = </b>________'))
    story.append(P('（至少需完成 10/11 项才能计算）评分范围 0–100，越高表示障碍越严重。'))
    story.append(P('<b>MCID：</b>减少 ≥ 10–15 分视为有临床意义的改善。'))
    story.append(PageBreak())

    # ── 八-C、ABC Scale ──────────────────────────────────────────────────────
    story.extend(section_banner('八-C', '活动特异性平衡信心量表（ABC Scale）'))
    story.append(P('请评估您完成以下各项活动时，对自己<b>不会失去平衡</b>有多大信心。'))
    story.append(P('从 0%（毫无信心）到 100%（完全有信心）中选择。'))
    story.append(SP(6))
    abc_items = [
        ('1','在屋内走动'),('2','上或下楼梯'),('3','弯腰从地上捡起拖鞋'),
        ('4','伸手去拿放在与眼同高架子上的小罐子'),('5','踮起脚尖去拿高过头顶的物品'),
        ('6','站在椅子上够东西'),('7','扫地'),('8','走出家门，走向停在车道上的车'),
        ('9','进出轿车'),('10','穿过停车场走向商场'),('11','走上或走下斜坡'),
        ('12','在拥挤的商场里快步走过人群'),('13','在人群中行走时被别人撞到'),
        ('14','扶着扶手踏上或踏下自动扶梯'),('15','双手提着东西且不能扶扶手时踏上或踏下自动扶梯'),
        ('16','在结冰的或较滑的人行道上行走'),
    ]
    abc_rows = [[P('<b>序号</b>', s_th), P('<b>活动</b>', s_th), P('<b>信心程度（0–100%）</b>', s_th)]]
    for num, desc in abc_items:
        abc_rows.append([P(num, s_td_c), P(desc, s_td), P('', s_td)])
    abc_tbl = Table(abc_rows, colWidths=cols(1, 11, 3))
    abc_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(2,0),(2,-1),'CENTER'),('FONTNAME',(0,1),(-1,-1),BASE_FONT),
        ('FONTSIZE',(0,0),(-1,-1),9),('LEADING',(0,0),(-1,-1),13),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    for r in range(1, len(abc_rows)):
        if r % 2 == 0:
            abc_tbl.setStyle(TableStyle([('BACKGROUND',(0,r),(-1,r),ACCENT_LIGHT)]))
    story.append(abc_tbl)
    story.append(SP(8))
    story.extend(sub_header('评分'))
    story.append(P('<b>ABC 得分 = 各项目评分的平均值 = </b>________ %'))
    story.append(P('• <b>< 67%</b>：跌倒风险增高　• <b>50–80%</b>：中等功能水平　• <b>> 80%</b>：高功能水平'))
    story.append(P('<b>MCID：</b>提高 ≥ 10 个百分点视为有临床意义的改善。'))
    story.append(PageBreak())

    # ── 八-D、Berg 平衡量表 ───────────────────────────────────────────────────
    story.extend(section_banner('八-D', 'Berg 平衡量表（BBS）'))
    story.append(P('BBS 是老年平衡功能评估的金标准量表，共 14 项，每项 0–4 分，总分 0–56 分。'))
    story.append(P('<b>指导语：</b>请按指令完成以下动作，治疗师根据完成质量评分。需有人保护。'))
    story.append(SP(6))

    bbs_items = [
        '1. 从坐位到站立',
        '2. 从站立到坐位',
        '3. 坐位 ↔ 站立位转移',
        '4. 无支撑站立',
        '5. 无支撑坐位（双脚着地）',
        '6. 闭眼站立',
        '7. 双脚并拢站立',
        '8. 上肢前伸（测量前伸距离 cm）',
        '9. 从地面拾物',
        '10. 转身向后看',
        '11. 原地转身 360°',
        '12. 双脚交替踏台阶',
        '13. 一脚在前一脚在后（串联站姿）',
        '14. 单腿站立（记录支撑时间 秒）',
    ]
    bbs_rows = [[P('<b>序号</b>', s_th), P('<b>测试动作</b>', s_th),
                 P('<b>0</b>', s_th), P('<b>1</b>', s_th), P('<b>2</b>', s_th),
                 P('<b>3</b>', s_th), P('<b>4</b>', s_th), P('<b>得分</b>', s_th)]]
    for item in bbs_items:
        bbs_rows.append([P(item.split('.')[0], s_td_c), P(item.split('. ', 1)[1], s_td)]
                        + [P('□', s_td_c)] * 5 + [P('', s_td_c)])
    bbs_tbl = Table(bbs_rows, colWidths=cols(1.5, 9, 1, 1, 1, 1, 1, 2))
    bbs_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),9),
        ('LEADING',(0,0),(-1,-1),13),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    for r in range(1, len(bbs_rows)):
        if r % 2 == 0:
            bbs_tbl.setStyle(TableStyle([('BACKGROUND',(0,r),(-1,r),ACCENT_LIGHT)]))
    story.append(bbs_tbl)
    story.append(SP(6))
    story.append(P('<b>评分标准：</b>0 = 不能完成 ｜ 1 = 需大量帮助 ｜ 2 = 需少量帮助 ｜ 3 = 独立完成但欠稳 ｜ 4 = 正常独立完成'))
    story.append(SP(4))
    total_row = [[P('<b>BBS 总分</b>', s_td_c), P('________ / 56', s_large)]]
    tt = Table(total_row, colWidths=cols(1, 3))
    tt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),ACCENT_LIGHT),('BOX',(0,0),(-1,-1),0.8,ACCENT),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    story.append(tt)
    story.append(SP(8))
    story.extend(sub_header('解读'))
    story.append(P('• <b>0–20 分</b>：平衡功能差，高跌倒风险（通常需轮椅）'))
    story.append(P('• <b>21–40 分</b>：平衡功能可接受，需辅助器具行走，中度跌倒风险'))
    story.append(P('• <b>41–56 分</b>：平衡功能良好，独立行走，低跌倒风险'))
    story.append(P('• <b>跌倒风险截断值：< 45 分</b> 提示跌倒风险增高（< 50 分亦有报告）'))
    story.append(SP(4))
    story.append(P('<b>MCID：</b>总分提高 ≥ 4 分（一般老年人群）/ ≥ 6 分（脑卒中后）视为有临床意义的改善。'))
    story.append(SP(4))
    story.append(note('提示：完成 BBS 约需 15–20 分钟。若时间有限，可优先使用 SPPB 平衡子测试 + TUG 作快速筛查。'))
    story.append(PageBreak())

    # ── 九、评估总结 ─────────────────────────────────────────────────────────
    story.extend(section_banner('九', '评估总结'))
    story.extend(sub_header('核心测试结果汇总'))
    summary = [
        [P('<b>测试项目</b>', s_th), P('<b>首次评估\n日期：____</b>', s_th),
         P('<b>后续评估\n日期：____</b>', s_th), P('<b>变化</b>', s_th), P('<b>达到 MCID？</b>', s_th)],
        ['NPRS（疼痛 0–10）', '', '', '', '□ Y / □ N'],
        ['EQ-5D-5L（效用值）', '', '', '', '□ Y / □ N'],
        ['握力（最佳值 kg）', '', '', '', '□ Y / □ N'],
        ['SPPB（总分 0–12）', '', '', '', '□ Y / □ N'],
        ['TUG（秒）', '', '', '', '□ Y / □ N'],
        ['2MST（2分钟原地踏步，步数）', '', '', '', '□ Y / □ N'],
        ['BBS（总分 0–56）', '', '', '', '□ Y / □ N'],
        ['专项测试：__________', '', '', '', '□ Y / □ N'],
        ['专项测试：__________', '', '', '', '□ Y / □ N'],
    ]
    story.append(make_table(summary, col_widths=cols(5, 4, 4, 2.5, 3)))
    story.append(SP(10))

    # ── 跌倒风险综合分层框 ──
    story.extend(sub_header('跌倒风险综合分层'))
    story.append(P('勾选以下任一阳性项；综合阳性项数定级。', s_note))
    story.append(SP(2))
    risk_crit = [
        [P('□ SPPB ≤ 8 分', s_field), P('□ TUG ≥ 13.5 秒', s_field)],
        [P('□ 步速 < 1.0 m/s', s_field), P('□ ABC < 67%', s_field)],
        [P('□ BBS < 45 分', s_field), P('□ 过去 12 个月跌倒 ≥ 2 次', s_field)],
    ]
    rc_tbl = Table(risk_crit, colWidths=cols(1, 1))
    rc_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), ACCENT_LIGHT),
        ('BOX',           (0, 0), (-1, -1), 0.8, ACCENT),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
    ]))
    story.append(rc_tbl)
    story.append(SP(4))
    story.append(P('<b>综合跌倒风险等级：</b>　□ 低（0 项）　　□ 中（1–2 项）　　□ 高（≥ 3 项）', s_large))
    story.append(SP(2))
    story.append(P('<b>建议干预：</b>□ 平衡训练　□ 下肢力量训练　□ 辅具评估/调整　□ 居家环境改造转介　□ 药物复核（转医生）　□ 跌倒预防宣教', s_field))
    story.append(SP(10))

    story.extend(sub_header('临床印象'))
    for _ in range(3):
        story.append(HR())
        story.append(SP(2))
    story.append(SP(4))
    story.extend(sub_header('治疗目标'))
    for i in range(1, 4):
        story.append(P(f'{i}. ________________________________________________________________'))
    story.append(SP(8))
    story.extend(sub_header('治疗计划'))
    story.append(P('□ 门诊物理治疗　频率：________ 次/周　预期疗程：________ 周'))
    story.append(P('□ 家庭运动方案　□ 团体训练　□ 社区康复转介　□ 其他：__________'))
    story.append(SP(4))
    for _ in range(2):
        story.append(HR())
        story.append(SP(2))
    story.append(SP(8))
    story.append(P('治疗师签名：________________　　　　日期：________________'))
    story.append(PageBreak())

    # ── 附录 ─────────────────────────────────────────────────────────────────
    story.extend(section_banner('', '附录一、MCID 与截断值速查表'))
    mcid = [
        [P('<b>量表/测试</b>', s_th), P('<b>评分范围</b>', s_th), P('<b>MCID</b>', s_th), P('<b>截断值/高风险阈值</b>', s_th)],
        ['NPRS（疼痛）', '0–10', '↓ ≥ 2 分', '—'],
        ['EQ-5D-5L（效用值）', '0–1', '↑ 0.05–0.08', '—'],
        ['握力（男）', 'kg', '↑ 5–6 kg', '< 26 kg 肌少症风险'],
        ['握力（女）', 'kg', '↑ 5–6 kg', '< 18 kg 肌少症风险'],
        ['SPPB', '0–12', '↑ ≥ 1.0 分', '≤ 8 分 衰弱/高跌倒风险'],
        ['TUG', '秒', '↓ 2–3 秒', '≥ 13.5 秒 跌倒风险增高'],
        ['2MST（2分钟原地踏步）', '步数', '↑ ≥ 10 步', '明显低于同龄参考值提示耐力下降'],
        ['BBS（Berg 平衡）', '0–56', '↑ ≥ 4 分', '< 45 分 跌倒风险增高'],
        ['ODI（腰痛）', '0–100%', '↓ ≥ 10%', '> 40% 重度功能障碍'],
        ['QuickDASH（上肢）', '0–100', '↓ 10–15 分', '—'],
        ['ABC Scale（平衡信心）', '0–100%', '↑ 10%', '< 67% 跌倒风险'],
    ]
    story.append(make_table(mcid, col_widths=cols(5, 2, 3, 6)))
    story.append(SP(6))
    story.extend(sub_header('附录二、Borg 自觉用力评分（RPE 6–20）'))
    borg = [
        [P('<b>分值</b>', s_th), P('<b>描述</b>', s_th)],
        ['6', '毫不费力（安静休息水平）'],
        ['8', '极其轻松'],
        ['9', '非常轻松（可以轻松说话，如慢走）'],
        ['11', '轻松'],
        ['13', '有点困难（说话开始费力）'],
        ['15', '困难'],
        ['17', '非常困难（呼吸急促，只能简短说话）'],
        ['19', '极其困难（接近极限）'],
        ['20', '最大用力（完全力竭）'],
    ]
    story.append(make_table(borg, col_widths=cols(1, 6)))
    story.append(SP(6))
    story.extend(sub_header('附录三、运动处方记录（FITT-VP 原则）'))
    ex = [
        [P('<b>运动类型</b>', s_th), P('<b>强度\n(RPE)</b>', s_th), P('<b>频率\n(次/周)</b>', s_th),
         P('<b>时间\n(min)</b>', s_th), P('<b>组数×次数</b>', s_th), P('<b>备注</b>', s_th)],
        ['有氧运动\n（如步行、功率车）', '', '', '', '', ''],
        ['抗阻训练（下肢）', '', '', '', '', ''],
        ['抗阻训练（上肢）', '', '', '', '', ''],
        ['平衡训练', '', '', '', '', ''],
        ['柔韧性训练（牵伸）', '', '', '', '', ''],
    ]
    story.append(make_table(ex, col_widths=cols(3, 2, 2, 2, 2.5, 3)))
    story.append(SP(6))
    story.extend(sub_header('附录四、评估流程建议（首次评估约 40–50 分钟）'))
    flow = [
        [P('<b>顺序</b>', s_th), P('<b>内容</b>', s_th), P('<b>大约时间</b>', s_th)],
        ['1', '签署知情同意，采集病史（可由患者在候诊时完成问卷）', '5 min'],
        ['2', '主观评估：NPRS + EQ-5D-5L（可由患者在候诊时完成）', '5 min'],
        ['3', 'SPPB（平衡 + 4米步行 + 5次坐站）', '8 min'],
        ['4', '休息 2–3 分钟', '3 min'],
        ['5', 'TUG', '3 min'],
        ['6', '握力测试', '3 min'],
        [P('7', s_td), P('2分钟原地踏步测试（2MST，居家适用；前后测 HR、BP、SpO<sub>2</sub>、RPE）', s_td), '5 min'],
        ['8', 'Berg 平衡量表（如需详细平衡评估）', '15 min'],
        ['9', '选做专项测试（ODI / QuickDASH / ABC / BBS）', '5–10 min'],
        ['10', '评估总结与治疗目标沟通', '5 min'],
        [P('<b>合计</b>', s_td), P('', s_td), P('<b>约 40–60 分钟</b>', s_td)],
    ]
    story.append(make_table(flow, col_widths=cols(1, 8, 2.5)))

    return story


def main():
    parser = argparse.ArgumentParser(description='生成老年物理治疗评估工具手册 PDF (v2)')
    parser.add_argument('-o', '--output',
                        default='/Users/zonghanyang/AI Agents/Physio/老年物理治疗评估工具手册.pdf',
                        help='输出 PDF 路径')
    args = parser.parse_args()

    out = args.output
    doc = TocDocTemplate(out, pagesize=A4,
                         leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=20 * mm, bottomMargin=25 * mm,
                         title='老年物理治疗评估工具手册',
                         author='Physical Therapy Assessment',
                         subject='Geriatric PT Outcome Measures')
    doc.multiBuild(build_story(), canvasmaker=NumberedCanvas)
    print(f'PDF 已生成：{out}')
    print(f'文件大小：{os.path.getsize(out) / 1024:.1f} KB')


if __name__ == '__main__':
    main()
