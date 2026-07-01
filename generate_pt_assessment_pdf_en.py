#!/usr/bin/env python3
"""Generate Geriatric PT Outcome Measures Assessment Booklet PDF — ENGLISH (v3.1).

Mirrors the Chinese booklet with standard English instrument wording.
Shared layout engine lives in core.py.
"""

import os
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable
from reportlab.platypus.tableofcontents import TableOfContents

from core import (
    ACCENT, ACCENT_DARK, ACCENT_LIGHT, GREY_LINE, GREY_TEXT,
    BASE_FONT, BOLD_FONT, PAGE_W, PAGE_H, FULL_W,
    s_cover_title, s_cover_sub, s_banner, s_sub, s_body, s_small,
    s_large, s_th, s_td, s_td_c, s_note, s_field, s_strip,
    P, SP, HR, note, section_banner, sub_header, cols, make_table,
    make_numbered_canvas, TocDocTemplate, toc_style, default_output,
)

def build_story():
    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    story.append(SP(35 * mm))
    story.append(P('Geriatric Physical Therapy<br/>Assessment Booklet', s_cover_title))
    story.append(SP(4))
    story.append(HRFlowable(width='55%', thickness=2, color=ACCENT,
                            hAlign='CENTER', spaceAfter=3))
    story.append(HRFlowable(width='40%', thickness=0.6, color=ACCENT,
                            hAlign='CENTER', spaceAfter=18))
    story.append(P('Outcome Measures for Initial Evaluation &amp; Follow-up', s_cover_sub))
    story.append(SP(8))

    info = [
        [P('Patient Information', s_strip), '', '', ''],
        [P('<b>Name</b>', s_large), P('_________________', s_large),
         P('<b>Sex</b>', s_large), P('□ M   □ F', s_large)],
        [P('<b>Age</b>', s_large), P('_________________', s_large),
         P('<b>Diagnosis</b>', s_large), P('_________________', s_large)],
        [P('<b>Assessment Date</b>', s_large), P('_________________', s_large),
         P('<b>Therapist</b>', s_large), P('_________________', s_large)],
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
    story.append(P('Assessment type:  □ Initial Evaluation    □ Follow-up (Session ___)', s_large))
    story.append(SP(20))
    story.append(P('This booklet compiles internationally validated, age-appropriate subjective and objective', s_small))
    story.append(P('outcome measures for easy clinical use and progress tracking. Each measure includes scoring', s_small))
    story.append(P('instructions and clinical interpretation.', s_small))
    story.append(PageBreak())

    # ── CONTENTS ─────────────────────────────────────────────────────────────
    story.extend(section_banner('', 'Contents', toc=False))
    story.append(SP(6))
    toc = TableOfContents()
    toc.dotsMinLevel = 0
    toc.levelStyles = [
        toc_style(),
    ]
    story.append(toc)
    story.append(PageBreak())

    # ── 1. HISTORY ───────────────────────────────────────────────────────────
    story.extend(section_banner('1', 'Patient History'))
    story.append(SP(4))

    story.extend(sub_header('Chief Complaint'))
    story.append(P('Onset: __________   Location: __________   Quality: □ dull □ sharp □ aching □ numbness □ other____', s_field))
    story.append(P('Duration: □ constant □ intermittent    Aggravating: ______________    Relieving: ______________', s_field))
    story.append(SP(4))

    story.extend(sub_header('History of Present Illness'))
    for _ in range(3):
        story.append(P('_' * 70, s_field))
    story.append(SP(4))

    story.extend(sub_header('Past Medical History (tick all that apply)'))
    pmh = [
        '□ Hypertension', '□ Diabetes', '□ Coronary heart disease', '□ Arrhythmia', '□ Osteoporosis',
        '□ Stroke', '□ Parkinson’s disease', '□ Arthritis', '□ Chronic lung disease', '□ Vision/hearing impairment',
        '□ Cognitive impairment', '□ Urinary condition', '□ Other: ____________',
    ]
    pmh_rows = []
    for i in range(0, len(pmh), 2):
        pmh_rows.append([P(pmh[i], s_field),
                         P(pmh[i+1] if i+1 < len(pmh) else '', s_field)])
    pmh_tbl = Table(pmh_rows, colWidths=cols(1, 1))
    pmh_tbl.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(pmh_tbl)
    story.append(SP(4))

    story.extend(sub_header('Fall History (past 12 months)'))
    fall = [
        [P('No. of falls', s_td), P('□ 0   □ 1   □ ≥2 (____ times)', s_td),
         P('Injury', s_td), P('□ none □ soft tissue □ fracture □ head injury', s_td)],
        [P('Fear of falling', s_td), P('□ none □ mild □ moderate □ severe (limits activity)', s_td),
         P('Getting up', s_td), P('□ independent □ needs assistance', s_td)],
    ]
    story.append(make_table(fall, col_widths=cols(2, 5, 2, 5), header_rows=0, zebra=False))
    story.append(SP(4))

    story.extend(sub_header('Medications & Surgical History'))
    story.append(P('Long-term meds: □ anticoagulant  □ antihypertensive  □ antidiabetic  □ sedative/hypnotic  □ analgesic  □ other: ____________', s_field))
    story.append(P('Surgical history: ____________________________________________________________________', s_field))
    story.append(SP(4))

    story.extend(sub_header('Social & Functional Status'))
    life = [
        [P('Living situation', s_td), P('□ alone □ with family □ facility', s_td),
         P('Assistive device', s_td), P('□ none □ cane □ walker □ wheelchair', s_td)],
        [P('Exercise habit', s_td), P('□ none □ occasional □ regular (____×/week)', s_td),
         P('Smoking / Alcohol', s_td), P('□ none □ smoking □ alcohol', s_td)],
        [P('Prior rehab', s_td), P('□ none □ yes: ____________', s_td),
         P('Patient expectations', s_td), P('________________________', s_td)],
    ]
    story.append(make_table(life, col_widths=cols(2, 5, 2, 5), header_rows=0))
    story.append(SP(4))

    story.extend(sub_header('Allergies & Family History'))
    story.append(P('Allergies: □ none  □ drug (________)  □ food/other (________)', s_field))
    story.append(P('Family history: □ unremarkable  □ yes: ________ (e.g. osteoporosis, cardiovascular, neurodegenerative)', s_field))
    story.append(SP(4))

    story.extend(sub_header('Red Flag Screening (any positive — proceed with caution / refer)'))
    redflag = [
        [P('□ Night pain / pain at rest', s_td), P('□ Unexplained weight loss > 5 kg', s_td)],
        [P('□ Recent trauma / fall', s_td), P('□ Persistent fever / night sweats', s_td)],
        [P('□ Bowel / bladder change', s_td), P('□ History of malignancy', s_td)],
        [P('□ Progressive weakness / atrophy', s_td), P('□ Coagulation disorder / anticoagulant', s_td)],
    ]
    rf_tbl = Table(redflag, colWidths=cols(1, 1))
    rf_tbl.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    story.append(rf_tbl)
    story.append(SP(4))

    story.extend(sub_header('Neurological Symptoms'))
    neuro = [
        [P('Numbness/tingling', s_td), P('□ none □ upper limb □ lower limb □ other____', s_td),
         P('Weakness', s_td), P('□ none □ upper limb □ lower limb', s_td)],
        [P('Dizziness/vertigo', s_td), P('□ none □ occasional □ frequent □ postural', s_td),
         P('Vision change', s_td), P('□ none □ diplopia □ blurred', s_td)],
        [P('Speech/swallow', s_td), P('□ none □ yes: ________', s_td),
         P('Gait abnormality', s_td), P('□ none □ shuffling □ wide-based', s_td)],
    ]
    story.append(make_table(neuro, col_widths=cols(2, 5, 2, 5), header_rows=0))
    story.append(SP(4))

    story.extend(sub_header('ADL Baseline'))
    adl = [
        [P('<b>Task</b>', s_th), P('<b>Independent</b>', s_th),
         P('<b>Partial assist</b>', s_th), P('<b>Dependent</b>', s_th)],
        ['Eating', '□', '□', '□'],
        ['Bathing', '□', '□', '□'],
        ['Dressing', '□', '□', '□'],
        ['Toileting', '□', '□', '□'],
        ['Bed–chair transfer', '□', '□', '□'],
        ['Level walking', '□', '□', '□'],
        ['Stairs', '□', '□', '□'],
        ['Shopping/cooking (IADL)', '□', '□', '□'],
    ]
    story.append(make_table(adl, col_widths=cols(4, 2, 3, 3)))
    story.append(SP(4))

    story.extend(sub_header('Home Environment & Rehab Goal'))
    env = [
        [P('Home hazards', s_td), P('□ loose rugs/thresholds □ no grab bars □ poor lighting □ steep stairs □ none', s_td)],
        [P('SMART goal', s_td), P('____________________________________________________________________', s_td)],
    ]
    story.append(make_table(env, col_widths=cols(1, 9), header_rows=0))
    story.append(PageBreak())

    # ── 2. NPRS ──────────────────────────────────────────────────────────────
    story.extend(section_banner('2', 'Numeric Pain Rating Scale (NPRS)'))
    story.append(P('Rate pain on a 0–10 scale. 0 = no pain, 10 = worst pain imaginable.'))
    story.append(SP(6))
    pain_scale = [
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        ['No pain', '', '', '', '', 'Moderate', '', '', '', '', 'Worst'],
    ]
    pt = Table(pain_scale, colWidths=[FULL_W / 11] * 11)
    pt.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, GREY_LINE),
        ('BACKGROUND', (0,0), (-1,0), ACCENT), ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), BOLD_FONT), ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('FONTNAME', (0,1), (-1,1), BASE_FONT),
        ('FONTSIZE', (0,0), (-1,0), 13), ('FONTSIZE', (0,1), (-1,1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pt)
    story.append(SP(10))
    pain_rec = [
        [P('<b>Time point</b>', s_th), P('<b>Pain score (0–10)</b>', s_th)],
        ['Now (at rest)', ''],
        ['Least in past 24 h', ''],
        ['Worst in past 24 h', ''],
        ['With activity', ''],
    ]
    story.append(make_table(pain_rec, col_widths=cols(3, 2)))
    story.append(SP(8))
    story.extend(sub_header('Pain Location Diagram'))
    story.append(P('Mark the pain site (shade = pain, X = worst point):'))
    body_diag = [
        [P('<b>FRONT</b>', s_td_c), P('<b>BACK</b>', s_td_c)],
        [P('(patient marks pain here)', s_note), P('(patient marks pain here)', s_note)],
    ]
    bt = Table(body_diag, colWidths=cols(1, 1), rowHeights=[18, 180])
    bt.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, GREY_LINE), ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BACKGROUND', (0,0), (-1,0), ACCENT_LIGHT),
        ('FONTNAME', (0,0), (-1,-1), BASE_FONT),
    ]))
    story.append(bt)
    story.append(SP(4))
    story.append(note('MCID: a decrease ≥ 2 points is considered meaningful improvement.'))
    story.append(PageBreak())

    # ── 3. EQ-5D-5L ──────────────────────────────────────────────────────────
    story.extend(section_banner('3', 'EuroQol 5-Dimension 5-Level (EQ-5D-5L)'))
    story.append(P('For each dimension, tick the ONE statement that best describes <b>your health today</b>:'))
    story.append(SP(6))
    eq_dims = [
        ('Mobility', ['I have no problems in walking about','I have slight problems walking about',
            'I have moderate problems walking about','I have severe problems walking about','I am unable to walk about']),
        ('Self-care', ['I have no problems washing or dressing myself','I have slight problems washing or dressing myself',
            'I have moderate problems washing or dressing myself','I have severe problems washing or dressing myself',
            'I am unable to wash or dress myself']),
        ('Usual activities', ['I have no problems doing my usual activities','I have slight problems doing my usual activities',
            'I have moderate problems doing my usual activities','I have severe problems doing my usual activities',
            'I am unable to do my usual activities']),
        ('Pain / discomfort', ['I have no pain or discomfort','I have slight pain or discomfort',
            'I have moderate pain or discomfort','I have severe pain or discomfort','I have extreme pain or discomfort']),
        ('Anxiety / depression', ['I am not anxious or depressed','I am slightly anxious or depressed',
            'I am moderately anxious or depressed','I am severely anxious or depressed','I am extremely anxious or depressed']),
    ]
    for dim_name, opts in eq_dims:
        story.append(P(f'<b>{dim_name}</b>', s_large))
        for opt in opts:
            story.append(P(f'    □  {opt}'))
        story.append(SP(2))
    story.append(SP(8))
    story.append(note('The 5 dimensions can be converted to a health utility index (0–1). MCID: utility ↑ 0.05–0.08.'))
    story.append(PageBreak())

    # ── 4. HANDGRIP ──────────────────────────────────────────────────────────
    story.extend(section_banner('4', 'Handgrip Strength'))
    story.append(P('<b>Instrument:</b> Jamar or equivalent hydraulic dynamometer, handle at position 2.'))
    story.append(P('<b>Position:</b> seated, shoulder adducted and neutral, elbow flexed 90°, forearm neutral, wrist 0–30° extension.'))
    story.append(P('<b>Method:</b> alternate left/right, 3 trials each, ≥ 30 s rest between. Encourage maximal effort.'))
    story.append(SP(8))
    grip = [
        [P('', s_th), P('<b>Trial 1 (kg)</b>', s_th), P('<b>Trial 2 (kg)</b>', s_th),
         P('<b>Trial 3 (kg)</b>', s_th), P('<b>Best (kg)</b>', s_th)],
        [P('<b>Left</b>', s_td_c), '', '', '', ''],
        [P('<b>Right</b>', s_td_c), '', '', '', ''],
        [P('<b>Both avg.</b>', s_td_c), '—', '—', '—', ''],
    ]
    story.append(make_table(grip, col_widths=cols(3, 4, 4, 4, 4)))
    story.append(SP(8))
    story.extend(sub_header('Reference values (AWGS 2019)'))
    cutoff = [
        [P('<b>Sex</b>', s_th), P('<b>Sarcopenia cutoff</b>', s_th), P('<b>Note</b>', s_th)],
        ['Male', '< 26 kg', ''],
        ['Female', '< 18 kg', ''],
    ]
    story.append(make_table(cutoff, col_widths=cols(2, 4, 5)))
    story.append(SP(4))
    story.append(P('<b>MCID:</b> an increase ≥ 5–6 kg is considered a meaningful improvement.'))
    story.append(PageBreak())

    # ── 5. SPPB ──────────────────────────────────────────────────────────────
    story.extend(section_banner('5', 'Short Physical Performance Battery (SPPB)'))
    story.append(P('Three sub-tests; total score 0–12. ≤ 8 indicates frailty / high fall risk.'))
    story.append(SP(6))

    # safety box
    safety = [
        [P('<b>General Safety for Performance Tests (SPPB / TUG / BBS / 2MST)</b>', s_td)],
        [P('• Therapist stands beside and slightly behind the patient throughout to guard against falls.', s_small)],
        [P('• Stop immediately if: chest pain/tightness, severe dyspnoea, dizziness/ataxia, pallor/diaphoresis, SpO₂ &lt; 85%, or the patient asks to stop.', s_small)],
        [P('• Before endurance testing (2MST): defer if resting SBP &gt; 180 or DBP &gt; 110, or SpO₂ &lt; 90%.', s_small)],
    ]
    sf_tbl = Table(safety, colWidths=[FULL_W])
    sf_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_LIGHT), ('BOX', (0,0), (-1,-1), 0.8, ACCENT),
        ('BACKGROUND', (0,0), (0,0), ACCENT), ('TEXTCOLOR', (0,0), (0,0), colors.white),
        ('FONTNAME', (0,0), (0,0), BOLD_FONT),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(sf_tbl)
    story.append(SP(8))

    story.extend(sub_header('A. Standing Balance'))
    story.append(P('<b>Requirement:</b> stand without assistive device. Hold each position up to 10 s.'))
    bal = [
        [P('<b>Position</b>', s_th), P('<b>Able?</b>', s_th), P('<b>Time (s)</b>', s_th), P('<b>Score</b>', s_th)],
        ['1. Feet side-by-side', '□ yes / □ no', '', '□ 0 / □ 1'],
        ['2. Semi-tandem\n(heel of one foot beside\nbig toe of the other)', '□ yes / □ no', '', '□ 0 / □ 1'],
        [P('3. Tandem\n(heel of one foot directly\nin front of toes of other)', s_td), '□ yes / □ no',
         P('10 s = 2\n3–9.99 s = 1\n< 3 s = 0\nRecord: ____ s', s_small),
         P('□ 2\n□ 1\n□ 0', s_small)],
    ]
    story.append(make_table(bal, col_widths=cols(4, 3, 3, 3)))
    story.append(note('If position 1 failed → 0 and stop; if position 2 failed → 1, proceed to gait.'))
    story.append(SP(8))

    story.extend(sub_header('B. 4-Metre Gait Speed'))
    story.append(P('<b>Requirement:</b> walk 4 m at usual pace (assistive device permitted); 2 trials, use the faster.'))
    gait = [[P('', s_th), P('<b>Trial 1</b>', s_th), P('<b>Trial 2</b>', s_th)],
            ['Walking time (s)', '', '']]
    story.append(make_table(gait, col_widths=cols(1, 1, 1)))
    story.append(SP(4))
    gait_score = [
        [P('<b>Time</b>', s_th), P('<b>≤ 4.82 s</b>', s_th), P('<b>4.83–6.20 s</b>', s_th),
         P('<b>6.21–8.70 s</b>', s_th), P('<b>> 8.70 s</b>', s_th), P('<b>Unable</b>', s_th)],
        ['Score', '4', '3', '2', '1', '0'],
    ]
    story.append(make_table(gait_score, col_widths=cols(2, 3, 3.5, 3.5, 3, 2)))
    story.append(SP(2))
    story.append(P('Gait speed score: ________'))
    story.append(SP(8))

    story.extend(sub_header('C. Five Chair Stands'))
    story.append(P('<b>Requirement:</b> arms folded across chest, rise fully from a standard chair (seat ~43–45 cm) and sit back down, 5 times, timed.'))
    story.append(P('Screening trial: do 1 stand first to confirm independence.'))
    story.append(SP(4))
    chair_yn = [['Able?', '□ yes   Time: ________ s', '□ no → 0']]
    story.append(make_table(chair_yn, col_widths=cols(2, 7, 3), header_rows=0, zebra=False))
    chair_score = [
        [P('<b>Time</b>', s_th), P('<b>≤ 11.19 s</b>', s_th), P('<b>11.20–13.69 s</b>', s_th),
         P('<b>13.70–16.69 s</b>', s_th), P('<b>16.70–59.99 s</b>', s_th), P('<b>> 60 s</b>', s_th)],
        ['Score', '4', '3', '2', '1', '0'],
    ]
    story.append(make_table(chair_score, col_widths=cols(2, 3, 3.5, 3.5, 3, 2)))
    story.append(SP(2))
    story.append(P('Chair stand score: ________'))
    story.append(SP(8))
    sppb_total = [
        [P('<b>Sub-test</b>', s_th), P('<b>A. Balance (0–4)</b>', s_th),
         P('<b>B. Gait speed (0–4)</b>', s_th), P('<b>C. Chair stand (0–4)</b>', s_th),
         P('<b>SPPB total (0–12)</b>', s_th)],
        ['Score', '', '', '', ''],
    ]
    story.append(make_table(sppb_total, col_widths=cols(3, 3.5, 4, 3.5, 4)))
    story.append(SP(6))
    story.extend(sub_header('SPPB Interpretation'))
    story.append(P('• <b>0–3</b>: severe limitation, high fall risk　• <b>4–6</b>: moderate limitation'))
    story.append(P('• <b>7–9</b>: mild limitation　• <b>10–12</b>: good function'))
    story.append(P('• <b>MCID: ≥ 1.0 point</b>'))
    story.append(PageBreak())

    # ── 6. TUG ───────────────────────────────────────────────────────────────
    story.extend(section_banner('6', 'Timed Up and Go (TUG)'))
    story.extend(sub_header('Procedure'))
    for s in [
        '1. Patient seated in a standard armchair (seat ~45 cm), back against the chair.',
        '2. Place a marker on the floor 3 m ahead of the chair (tape or cone).',
        '3. Instruction: “On the word ‘go’, stand up, walk to the 3 m marker at a safe and brisk pace, turn, walk back, and sit down again.”',
        '4. Time from “go” to when the patient’s buttocks touch the seat again.',
        '5. One practice trial, then 1–2 timed trials; record the best.',
        '6. The patient may use their usual assistive device (e.g. cane).',
    ]:
        story.append(P(s))
    story.append(SP(6))
    tug = [
        [P('', s_th), P('<b>Time (s)</b>', s_th), P('<b>Assistive device?</b>', s_th), P('<b>Notes</b>', s_th)],
        ['Practice (unscored)', '', '□ yes / □ no', ''],
        ['Trial 1', '', '□ yes / □ no', ''],
        ['Trial 2 (optional)', '', '□ yes / □ no', ''],
        [P('<b>Best</b>', s_td), '', '', ''],
    ]
    story.append(make_table(tug, col_widths=cols(3, 3.5, 3, 4.5)))
    story.append(SP(8))
    story.extend(sub_header('Interpretation'))
    for txt in [
        '• <b>< 10 s</b>: normal, freely mobile',
        '• <b>10–19 s</b>: mostly independent; mild gait/balance impairment possible',
        '• <b>≥ 13.5 s</b>: increased fall risk',
        '• <b>≥ 20 s</b>: obvious mobility impairment — intervention needed',
        '• <b>≥ 30 s</b>: severe impairment; assistance needed for ADLs',
    ]:
        story.append(P(txt))
    story.append(SP(4))
    story.append(P('<b>MCID:</b> a decrease ≥ 2–3 s is considered a meaningful improvement.'))
    story.append(PageBreak())

    # ── 7. 2MST ──────────────────────────────────────────────────────────────
    story.extend(section_banner('7', 'Two-Minute Step Test (2MST) — Home-friendly'))
    story.append(P('The 2MST is the recognised substitute for the 2MWT/6MWT when space is limited (e.g. at home); '
                   'it assesses aerobic and lower-limb endurance. From the Senior Fitness Test.'))
    story.append(SP(6))
    story.extend(sub_header('Setup & equipment'))
    for txt in [
        '• Only a standing spot is needed (beside a wall or sturdy chair); no long corridor.',
        '• Stopwatch; wall tape or a resistance band (to mark knee height).',
        '• Sphygmomanometer, pulse oximeter, Borg scale (RPE 6–20).',
        '• A sturdy chair / walker for the patient to lightly touch for balance (balance only, not for lifting).',
    ]:
        story.append(P(txt))
    story.append(SP(6))
    story.extend(sub_header('Knee-height mark'))
    story.append(P('Mark the midpoint between the upper border of the patella and the iliac crest with wall tape, '
                   'or a band between two chairs. Each step counts only if the knee reaches this height.'))
    story.append(SP(6))
    story.extend(sub_header('Pre-test assessment'))
    pre = [
        [P('<b>Measure</b>', s_th), P('<b>Value</b>', s_th), P('<b>Note</b>', s_th)],
        ['Resting HR', '________ bpm', 'normal 60–100'],
        ['Blood pressure', '________ / ________ mmHg', 'defer if resting SBP > 180'],
        [P('SpO<sub>2</sub>', s_td), '________ %', 'caution if < 90%'],
        ['Borg RPE (rest)', '________ (6–20)', ''],
    ]
    story.append(make_table(pre, col_widths=cols(6, 7, 7)))
    story.append(SP(6))
    story.extend(sub_header('Instructions'))
    story.append(P('“March in place for 2 minutes, lifting each knee up to the mark. Aim to complete as many correct steps '
                   'as possible. You may slow down or pause, but the timer keeps running. Ready? Go!”'))
    story.append(SP(4))
    story.append(P('• <b>Counting:</b> each knee lift reaching the mark counts as 1 step (usually count one side, e.g. right knee); record the 2-min total.'))
    story.append(P('• Prompt time every 30 s with standard encouragement; at 2 min → “Stop!” Record total steps.'))
    story.append(P('• The therapist must stand behind and to the side to guard against falls.'))
    story.append(SP(8))
    story.extend(sub_header('Result'))
    res = [['Total steps in 2 min', '________ steps', 'Knee-height mark: ________ cm']]
    story.append(make_table(res, col_widths=cols(2, 4, 3), header_rows=0, zebra=False))
    story.append(SP(6))
    story.extend(sub_header('Post-test assessment'))
    post = [
        [P('<b>Measure</b>', s_th), P('<b>Value</b>', s_th), P('<b>Note</b>', s_th)],
        ['HR', '________ bpm', ''],
        ['Blood pressure', '________ / ________ mmHg', ''],
        [P('SpO<sub>2</sub>', s_td), '________ %', 'concern if < 88% or drop > 4%'],
        ['Borg RPE (post)', '________ (6–20)', ''],
        ['Borg dyspnoea', '________ (0–10)', 'modified Borg dyspnoea scale'],
    ]
    story.append(make_table(post, col_widths=cols(6, 7, 7)))
    story.append(SP(8))
    story.extend(sub_header('Age- & sex-specific reference (~50th percentile, steps)'))
    ref2mst = [
        [P('<b>Age</b>', s_th), P('<b>Male (steps)</b>', s_th), P('<b>Female (steps)</b>', s_th)],
        ['60–69', '85–95', '75–87'],
        ['70–79', '75–87', '65–80'],
        ['80–89', '60–76', '55–68'],
    ]
    story.append(make_table(ref2mst, col_widths=cols(1, 1, 1)))
    story.append(SP(4))
    story.append(P('• <b>Markedly below the reference</b> indicates reduced aerobic capacity and higher fall/disability risk.'))
    story.append(P('• <b>MCID:</b> not firmly established; ~ ≥ 10 steps (or ~10% of baseline) is suggested as a reference threshold.'))
    story.append(PageBreak())

    # ── 8-A ODI ──────────────────────────────────────────────────────────────
    story.extend(section_banner('8-A', 'Oswestry Disability Index (ODI) — Low Back Pain'))
    story.append(P('For each section, tick the ONE statement that best describes <b>your status today</b>.'))
    story.append(SP(6))
    odi_secs = [
        ('1. Pain intensity', ['(0) I have no pain at the moment.','(1) The pain is very mild at the moment.',
            '(2) The pain is moderate at the moment.','(3) The pain is fairly severe at the moment.',
            '(4) The pain is very severe at the moment.','(5) The pain is the worst imaginable at the moment.']),
        ('2. Personal care (washing, dressing, etc.)', ['(0) I can look after myself normally without causing extra pain.',
            '(1) I can look after myself normally but it causes extra pain.','(2) It is painful to look after myself and I am slow and careful.',
            '(3) I need some help but manage most of my personal care.','(4) I need help every day in most aspects of self-care.',
            '(5) I do not get dressed; I wash with difficulty and stay in bed.']),
        ('3. Lifting', ['(0) I can lift heavy weights without extra pain.','(1) I can lift heavy weights but it gives extra pain.',
            '(2) Pain prevents me lifting heavy weights off the floor, but I can manage if conveniently placed (e.g. on a table).',
            '(3) Pain prevents me lifting heavy weights, but I can manage light-to-medium weights if conveniently placed.',
            '(4) I can lift very light weights.','(5) I cannot lift or carry anything.']),
        ('4. Walking', ['(0) Pain does not prevent me walking any distance.','(1) Pain prevents me walking more than one mile (~1.6 km).',
            '(2) Pain prevents me walking more than ½ mile (~800 m).','(3) Pain prevents me walking more than ¼ mile (~400 m).',
            '(4) I can only walk using a stick or crutches.','(5) I am in bed most of the time.']),
        ('5. Sitting', ['(0) I can sit in any chair as long as I like.','(1) I can only sit in my favourite chair as long as I like.',
            '(2) Pain prevents me sitting more than one hour.','(3) Pain prevents me sitting more than ½ hour.',
            '(4) Pain prevents me sitting more than 10 minutes.','(5) Pain prevents me sitting at all.']),
        ('6. Standing', ['(0) I can stand as long as I want without extra pain.','(1) I can stand as long as I want but it gives extra pain.',
            '(2) Pain prevents me standing more than 1 hour.','(3) Pain prevents me standing more than ½ hour.',
            '(4) Pain prevents me standing more than 10 minutes.','(5) Pain prevents me standing at all.']),
        ('7. Sleeping', ['(0) My sleep is never disturbed by pain.','(1) My sleep is occasionally disturbed by pain.',
            '(2) Because of pain I have less than 6 hours’ sleep.','(3) Because of pain I have less than 4 hours’ sleep.',
            '(4) Because of pain I have less than 2 hours’ sleep.','(5) Pain prevents me from sleeping at all.']),
        ('8. Sex life (if applicable)', ['(0) My sex life is normal and causes no extra pain.','(1) My sex life is normal but causes some extra pain.',
            '(2) My sex life is nearly normal but is very painful.','(3) My sex life is severely restricted by pain.',
            '(4) My sex life is nearly absent because of pain.','(5) Pain prevents any sex life at all.']),
        ('9. Social life', ['(0) My social life is normal and causes no extra pain.','(1) My social life is normal but increases the degree of pain.',
            '(2) Pain has no significant effect on my social life apart from limiting more energetic interests (e.g. sport).',
            '(3) Pain has restricted my social life and I do not go out as often.','(4) Pain has restricted my social life to my home.',
            '(5) I have no social life because of pain.']),
        ('10. Travelling', ['(0) I can travel anywhere without pain.','(1) I can travel anywhere but it gives extra pain.',
            '(2) Pain is bad but I manage journeys over two hours.','(3) Pain restricts me to journeys of less than one hour.',
            '(4) Pain restricts me to short necessary journeys under 30 minutes.','(5) Pain prevents me travelling except to receive treatment.']),
    ]
    for title, stmts in odi_secs:
        story.append(P(f'<b>{title}</b>', s_large))
        for s in stmts:
            story.append(P(f'    □  {s}', s_small))
        story.append(SP(2))
    story.append(SP(6))
    story.extend(sub_header('ODI Scoring'))
    story.append(P('<b>Total:</b> ________ / 50'))
    story.append(P('<b>ODI% = (Total ÷ 50) × 100 = </b>________ %'))
    story.append(P('(If the sex-life item is not applicable, divide by 45 instead.)'))
    story.append(SP(4))
    story.append(P('<b>Interpretation:</b> 0–20% minimal | 21–40% moderate | 41–60% severe | 61–80% crippling | 81–100% bed-bound'))
    story.append(P('<b>MCID:</b> a decrease ≥ 10 percentage points is considered a meaningful improvement.'))
    story.append(PageBreak())

    # ── 8-B QuickDASH ────────────────────────────────────────────────────────
    story.extend(section_banner('8-B', 'QuickDASH Upper-Limb Outcome'))
    story.append(P('Answer based on the <b>past week</b>; rate overall function even if the two arms differ.'))
    story.append(SP(6))
    story.extend(sub_header('Difficulty (1 = no difficulty, 5 = unable)'))
    qdash_items = [
        '1. Open a tight or new jar',
        '2. Do heavy household chores (e.g. wash walls, floors)',
        '3. Carry a shopping bag or briefcase',
        '4. Wash your back',
        '5. Use a knife to cut food',
        '6. Recreational activities taking force/impact through the arm (e.g. racquet sports, hammering)',
    ]
    qd_rows = [[P('<b>Item</b>', s_th), P('<b>1\nNo diff.</b>', s_th), P('<b>2\nSlight</b>', s_th),
                P('<b>3\nModerate</b>', s_th), P('<b>4\nSevere</b>', s_th), P('<b>5\nUnable</b>', s_th)]]
    for item in qdash_items:
        qd_rows.append([P(item, s_td)] + [P('□', s_td_c)] * 5)
    qd_tbl = Table(qd_rows, colWidths=cols(7, 2, 2, 2, 2, 2))
    qd_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('LINEBELOW',(0,0),(-1,0),1.4,ACCENT_DARK),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),8),
        ('LEADING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    for r in range(1, len(qd_rows)):
        if r % 2 == 0:
            qd_tbl.setStyle(TableStyle([('BACKGROUND',(0,r),(-1,r),ACCENT_LIGHT)]))
    story.append(qd_tbl)
    story.append(SP(8))
    story.extend(sub_header('Symptom severity (past week)'))
    symp_items = [
        '7. Pain in your arm, shoulder or hand',
        '8. Pain in your arm, shoulder or hand during a specific activity',
        '9. Tingling (pins and needles) in your arm, shoulder or hand',
    ]
    sy_rows = [[P('<b>Item</b>', s_th), P('<b>1\nNone</b>', s_th), P('<b>2\nSlight</b>', s_th),
                P('<b>3\nModerate</b>', s_th), P('<b>4\nSevere</b>', s_th), P('<b>5\nExtreme</b>', s_th)]]
    for item in symp_items:
        sy_rows.append([P(item, s_td)] + [P('□', s_td_c)] * 5)
    sy_tbl = Table(sy_rows, colWidths=cols(7, 2, 2, 2, 2, 2))
    sy_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('LINEBELOW',(0,0),(-1,0),1.4,ACCENT_DARK),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),8),
        ('LEADING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(sy_tbl)
    story.append(SP(6))
    story.extend(sub_header('Impact (past week)'))
    extra = [
        [P('10. Does your arm/shoulder/hand problem interfere with your work or daily activities?', s_td),
         P('□ not at all  □ slightly  □ moderately  □ severely  □ extremely', s_td)],
        [P('11. Does your arm/shoulder/hand problem interfere with your sleep?', s_td),
         P('□ not at all  □ slightly  □ moderately  □ severely  □ extremely', s_td)],
    ]
    story.append(make_table(extra, col_widths=cols(1, 1), header_rows=0, zebra=False))
    story.append(SP(8))
    story.extend(sub_header('Scoring'))
    story.append(P('<b>QuickDASH = [(sum of item scores ÷ number of items) − 1] × 25 = </b>________'))
    story.append(P('(At least 10/11 items must be completed.) Range 0–100; higher = more disability.'))
    story.append(P('<b>MCID:</b> a decrease ≥ 10–15 points is considered a meaningful improvement.'))
    story.append(PageBreak())

    # ── 8-C ABC Scale ────────────────────────────────────────────────────────
    story.extend(section_banner('8-C', 'Activities-specific Balance Confidence (ABC) Scale'))
    story.append(P('Rate your confidence that you <b>will not lose your balance</b> while performing each activity.'))
    story.append(P('Choose from 0% (no confidence) to 100% (completely confident).'))
    story.append(SP(6))
    abc_items = [
        ('1','Walk around the house'),('2','Walk up or down stairs'),
        ('3','Bend over and pick up a slipper from the floor'),
        ('4','Reach for a small can off a shelf at eye level'),
        ('5','Stand on tiptoes and reach for something above your head'),
        ('6','Stand on a chair and reach for something'),('7','Sweep the floor'),
        ('8','Walk out the front door to a car parked in the driveway'),
        ('9','Get into or out of a car'),('10','Walk across a parking lot to the mall'),
        ('11','Walk up or down a ramp'),('12','Walk through a crowded mall where people walk past quickly'),
        ('13','Are bumped into by people as you walk through the mall'),
        ('14','Step onto or off an escalator while holding the railing'),
        ('15','Step onto or off an escalator while holding parcels (cannot hold the railing)'),
        ('16','Walk outside on icy sidewalks'),
    ]
    abc_rows = [[P('<b>#</b>', s_th), P('<b>Activity</b>', s_th), P('<b>Confidence (0–100%)</b>', s_th)]]
    for num, desc in abc_items:
        abc_rows.append([P(num, s_td_c), P(desc, s_td), P('', s_td)])
    abc_tbl = Table(abc_rows, colWidths=cols(1, 11, 3))
    abc_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('LINEBELOW',(0,0),(-1,0),1.4,ACCENT_DARK),('ALIGN',(2,0),(2,-1),'CENTER'),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),9),('LEADING',(0,0),(-1,-1),13),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    for r in range(1, len(abc_rows)):
        if r % 2 == 0:
            abc_tbl.setStyle(TableStyle([('BACKGROUND',(0,r),(-1,r),ACCENT_LIGHT)]))
    story.append(abc_tbl)
    story.append(SP(8))
    story.extend(sub_header('Scoring'))
    story.append(P('<b>ABC score = mean of all item ratings = </b>________ %'))
    story.append(P('• <b>< 67%</b>: increased fall risk　• <b>50–80%</b>: moderate function　• <b>> 80%</b>: high function'))
    story.append(P('<b>MCID:</b> an increase ≥ 10 percentage points is considered a meaningful improvement.'))
    story.append(PageBreak())

    # ── 8-D BBS ──────────────────────────────────────────────────────────────
    story.extend(section_banner('8-D', 'Berg Balance Scale (BBS)'))
    story.append(P('BBS is the gold-standard balance measure for older adults: 14 items, each scored 0–4, total 0–56.'))
    story.append(P('<b>Instructions:</b> ask the patient to perform each task; score by quality of performance. Guard the patient.'))
    story.append(SP(6))
    bbs_items = [
        '1. Sitting to standing','2. Standing to sitting','3. Transfers','4. Standing unsupported',
        '5. Sitting unsupported','6. Standing with eyes closed','7. Standing with feet together',
        '8. Reaching forward with outstretched arm','9. Retrieving object from floor','10. Turning to look behind',
        '11. Turning 360 degrees','12. Placing alternate foot on stool','13. Standing with one foot in front',
        '14. Standing on one leg',
    ]
    bbs_rows = [[P('<b>#</b>', s_th), P('<b>Task</b>', s_th),
                 P('<b>0</b>', s_th), P('<b>1</b>', s_th), P('<b>2</b>', s_th),
                 P('<b>3</b>', s_th), P('<b>4</b>', s_th), P('<b>Score</b>', s_th)]]
    for item in bbs_items:
        bbs_rows.append([P(item.split('.')[0], s_td_c), P(item.split('. ', 1)[1], s_td)]
                        + [P('□', s_td_c)] * 5 + [P('', s_td_c)])
    bbs_tbl = Table(bbs_rows, colWidths=cols(1.5, 9, 1, 1, 1, 1, 1, 2))
    bbs_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5,GREY_LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(-1,0),ACCENT),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),BOLD_FONT),('ALIGN',(0,0),(-1,0),'CENTER'),
        ('LINEBELOW',(0,0),(-1,0),1.4,ACCENT_DARK),
        ('FONTNAME',(0,1),(-1,-1),BASE_FONT),('FONTSIZE',(0,0),(-1,-1),9),('LEADING',(0,0),(-1,-1),13),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    for r in range(1, len(bbs_rows)):
        if r % 2 == 0:
            bbs_tbl.setStyle(TableStyle([('BACKGROUND',(0,r),(-1,r),ACCENT_LIGHT)]))
    story.append(bbs_tbl)
    story.append(SP(6))
    story.append(P('<b>Scoring:</b> 0 = unable | 1 = needs much help | 2 = needs little help | 3 = independent but unsteady | 4 = normal, independent'))
    story.append(SP(4))
    total_row = [[P('<b>BBS Total</b>', s_td_c), P('________ / 56', s_large)]]
    tt = Table(total_row, colWidths=cols(1, 3))
    tt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),ACCENT_LIGHT),('BOX',(0,0),(-1,-1),0.8,ACCENT),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    story.append(tt)
    story.append(SP(8))
    story.extend(sub_header('Interpretation'))
    story.append(P('• <b>0–20</b>: poor balance, high fall risk (often wheelchair)'))
    story.append(P('• <b>21–40</b>: acceptable balance; needs assistive device; moderate fall risk'))
    story.append(P('• <b>41–56</b>: good balance; independent gait; low fall risk'))
    story.append(P('• <b>Fall-risk cutoff: < 45</b> indicates increased fall risk (some sources use < 50)'))
    story.append(SP(4))
    story.append(P('<b>MCID:</b> an increase ≥ 4 points (general elderly) / ≥ 6 points (post-stroke) is considered meaningful.'))
    story.append(SP(4))
    story.append(note('Tip: the BBS takes ~15–20 min. If time is limited, use the SPPB balance sub-test + TUG for quick screening.'))
    story.append(PageBreak())

    # ── 9. SUMMARY ───────────────────────────────────────────────────────────
    story.extend(section_banner('9', 'Assessment Summary'))
    story.extend(sub_header('Core Outcome Measure Results'))
    summary = [
        [P('<b>Measure</b>', s_th), P('<b>Initial\nDate: ____</b>', s_th),
         P('<b>Follow-up\nDate: ____</b>', s_th), P('<b>Change</b>', s_th), P('<b>Met MCID?</b>', s_th)],
        ['NPRS (pain 0–10)', '', '', '', '□ Y / □ N'],
        ['EQ-5D-5L (utility)', '', '', '', '□ Y / □ N'],
        ['Handgrip (best, kg)', '', '', '', '□ Y / □ N'],
        ['SPPB (total 0–12)', '', '', '', '□ Y / □ N'],
        ['TUG (s)', '', '', '', '□ Y / □ N'],
        ['2MST (steps)', '', '', '', '□ Y / □ N'],
        ['BBS (total 0–56)', '', '', '', '□ Y / □ N'],
        ['Regional test: __________', '', '', '', '□ Y / □ N'],
        ['Regional test: __________', '', '', '', '□ Y / □ N'],
    ]
    story.append(make_table(summary, col_widths=cols(5, 4, 4, 2.5, 3)))
    story.append(SP(10))

    # fall risk stratification box
    story.extend(sub_header('Fall Risk Stratification'))
    story.append(P('Tick any positive item; grade by the number of positives.', s_note))
    story.append(SP(2))
    risk_crit = [
        [P('□ SPPB ≤ 8', s_field), P('□ TUG ≥ 13.5 s', s_field)],
        [P('□ Gait speed < 1.0 m/s', s_field), P('□ ABC < 67%', s_field)],
        [P('□ BBS < 45', s_field), P('□ ≥ 2 falls in past 12 months', s_field)],
    ]
    rc_tbl = Table(risk_crit, colWidths=cols(1, 1))
    rc_tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),ACCENT_LIGHT),('BOX',(0,0),(-1,-1),0.8,ACCENT),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    story.append(rc_tbl)
    story.append(SP(4))
    story.append(P('<b>Overall fall-risk level:</b>　□ Low (0)　　□ Moderate (1–2)　　□ High (≥ 3)', s_large))
    story.append(SP(2))
    story.append(P('<b>Suggested interventions:</b> □ balance training　□ lower-limb strengthening　□ assistive-device review　□ home-modification referral　□ medication review (to MD)　□ fall-prevention education', s_field))
    story.append(SP(10))

    story.extend(sub_header('Clinical Impression'))
    for _ in range(3):
        story.append(HR())
        story.append(SP(2))
    story.append(SP(4))
    story.extend(sub_header('Treatment Goals'))
    for i in range(1, 4):
        story.append(P(f'{i}. ________________________________________________________________'))
    story.append(SP(8))
    story.extend(sub_header('Plan'))
    story.append(P('□ Outpatient PT　Frequency: ______ ×/week　Expected duration: ______ weeks'))
    story.append(P('□ Home exercise programme　□ Group class　□ Community rehab referral　□ Other: __________'))
    story.append(SP(4))
    for _ in range(2):
        story.append(HR())
        story.append(SP(2))
    story.append(SP(8))
    story.append(P('Therapist signature: ________________　　　　Date: ________________'))
    story.append(PageBreak())

    # ── APPENDIX ─────────────────────────────────────────────────────────────
    story.extend(section_banner('', 'Appendix 1 — MCID & Cutoff Reference'))
    mcid = [
        [P('<b>Measure</b>', s_th), P('<b>Range</b>', s_th), P('<b>MCID</b>', s_th), P('<b>Cutoff / high-risk threshold</b>', s_th)],
        ['NPRS (pain)', '0–10', '↓ ≥ 2 points', '—'],
        ['EQ-5D-5L (utility)', '0–1', '↑ 0.05–0.08', '—'],
        ['Handgrip (male)', 'kg', '↑ 5–6 kg', '< 26 kg sarcopenia risk'],
        ['Handgrip (female)', 'kg', '↑ 5–6 kg', '< 18 kg sarcopenia risk'],
        ['SPPB', '0–12', '↑ ≥ 1.0 point', '≤ 8 frailty / high fall risk'],
        ['TUG', 'seconds', '↓ 2–3 s', '≥ 13.5 s increased fall risk'],
        ['2MST (2-min step)', 'steps', '↑ ≥ 10 steps', 'well below age norm → reduced capacity'],
        ['BBS (Berg balance)', '0–56', '↑ ≥ 4 points', '< 45 increased fall risk'],
        ['ODI (low back)', '0–100%', '↓ ≥ 10%', '> 40% severe disability'],
        ['QuickDASH (upper limb)', '0–100', '↓ 10–15 points', '—'],
        ['ABC Scale (balance confidence)', '0–100%', '↑ 10%', '< 67% fall risk'],
    ]
    story.append(make_table(mcid, col_widths=cols(5, 2, 3, 6)))
    story.append(SP(6))
    story.extend(sub_header('Appendix 2 — Borg Rating of Perceived Exertion (RPE 6–20)'))
    borg = [
        [P('<b>Score</b>', s_th), P('<b>Description</b>', s_th)],
        ['6', 'No exertion at all (resting)'],
        ['8', 'Extremely light'],
        ['9', 'Very light (easy conversation, e.g. slow walk)'],
        ['11', 'Light'],
        ['13', 'Somewhat hard (talking takes effort)'],
        ['15', 'Hard'],
        ['17', 'Very hard (breathless; only brief phrases)'],
        ['19', 'Extremely hard (near maximum)'],
        ['20', 'Maximal exertion (exhaustion)'],
    ]
    story.append(make_table(borg, col_widths=cols(1, 6)))
    story.append(SP(6))
    story.extend(sub_header('Appendix 3 — Exercise Prescription (FITT-VP)'))
    ex = [
        [P('<b>Type</b>', s_th), P('<b>Intensity\n(RPE)</b>', s_th), P('<b>Frequency\n(×/wk)</b>', s_th),
         P('<b>Time\n(min)</b>', s_th), P('<b>Sets × reps</b>', s_th), P('<b>Notes</b>', s_th)],
        ['Aerobic\n(e.g. walking, cycle)', '', '', '', '', ''],
        ['Resistance (lower limb)', '', '', '', '', ''],
        ['Resistance (upper limb)', '', '', '', '', ''],
        ['Balance', '', '', '', '', ''],
        ['Flexibility (stretching)', '', '', '', '', ''],
    ]
    story.append(make_table(ex, col_widths=cols(3, 2, 2, 2, 2.5, 3)))
    story.append(SP(6))
    story.extend(sub_header('Appendix 4 — Suggested Assessment Flow (initial ~40–60 min)'))
    flow = [
        [P('<b>#</b>', s_th), P('<b>Step</b>', s_th), P('<b>~Time</b>', s_th)],
        ['1', 'Informed consent & history (patient may complete questionnaires in waiting room)', '5 min'],
        ['2', 'Subjective: NPRS + EQ-5D-5L', '5 min'],
        ['3', 'SPPB (balance + 4 m gait + 5 chair stands)', '8 min'],
        ['4', 'Rest 2–3 min', '3 min'],
        ['5', 'TUG', '3 min'],
        ['6', 'Handgrip', '3 min'],
        [P('7', s_td), P('2MST (home-friendly; with pre/post HR, BP, SpO<sub>2</sub>, RPE)', s_td), '5 min'],
        ['8', 'Berg Balance Scale (if detailed balance assessment needed)', '15 min'],
        ['9', 'Optional regional tests (ODI / QuickDASH / ABC)', '5–10 min'],
        ['10', 'Summary & goal-setting', '5 min'],
        [P('<b>Total</b>', s_td), P('', s_td), P('<b>~40–60 min</b>', s_td)],
    ]
    story.append(make_table(flow, col_widths=cols(1, 8, 2.5)))

    return story


def main():
    parser = argparse.ArgumentParser(
        description='Generate Geriatric PT Assessment Booklet PDF — English (v3.1)')
    parser.add_argument('-o', '--output',
                        default=default_output('Geriatric_PT_Assessment_Booklet_EN.pdf'),
                        help='Output PDF path')
    args = parser.parse_args()

    out = args.output
    doc = TocDocTemplate(out, pagesize=A4,
                         leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=20 * mm, bottomMargin=25 * mm,
                         title='Geriatric Physical Therapy Assessment Booklet',
                         author='Physical Therapy Assessment',
                         subject='Geriatric PT Outcome Measures (EN)')
    NumberedCanvas = make_numbered_canvas(
        'Geriatric PT Assessment Booklet', 'Version 3.1 EN  |  2026')
    doc.multiBuild(build_story(), canvasmaker=NumberedCanvas)
    print(f'PDF generated: {out}')
    print(f'Size: {os.path.getsize(out) / 1024:.1f} KB')


if __name__ == '__main__':
    main()
