# Geriatric PT Assessment Booklet

A printable, clinically-validated assessment booklet for geriatric physical therapy. Generates an A4 PDF covering the full initial-evaluation workflow, from patient history through outcome measures to summary and exercise prescription.

## Contents

The booklet includes these standardised instruments:

- **Patient History** — chief complaint, PMH, fall history, medications, ADL, red flags, home environment
- **NPRS** — Numeric Pain Rating Scale
- **EQ-5D-5L** — EuroQol quality-of-life measure
- **Handgrip Strength** — with AWGS 2019 sarcopenia cutoffs
- **SPPB** — Short Physical Performance Battery (balance, gait speed, chair stands)
- **TUG** — Timed Up and Go
- **2MST** — Two-Minute Step Test (home-friendly aerobic assessment)
- **ODI** — Oswestry Disability Index (low back pain)
- **QuickDASH** — upper-limb outcome measure
- **ABC Scale** — Activities-specific Balance Confidence
- **BBS** — Berg Balance Scale
- **Summary** — results tracking, fall-risk stratification, goals, treatment plan
- **Appendices** — MCID/cutoff reference, Borg RPE scale, FITT-VP exercise prescription, assessment flow

Available in both **English** and **Chinese** (中文).

## Quick start

```bash
pip install reportlab

# English booklet
python generate_pt_assessment_pdf_en.py

# Chinese booklet
python generate_pt_assessment_pdf.py
```

Each script writes its PDF to the project directory by default. Use `-o` to specify a different path:

```bash
python generate_pt_assessment_pdf_en.py -o ~/Desktop/booklet.pdf
```

## Project structure

```
core.py                          Shared layout engine (fonts, styles, helpers)
generate_pt_assessment_pdf_en.py  English booklet generator
generate_pt_assessment_pdf.py      Chinese booklet generator
Geriatric_PT_Assessment_Booklet_EN.pdf  Pre-built English PDF
老年物理治疗评估工具手册.pdf            Pre-built Chinese PDF
backups/                         Historical versions
```

## Dependencies

- Python 3.8+
- [ReportLab](https://www.reportlab.org/) (`pip install reportlab`)

Fonts auto-detect from the system: macOS Songti SC (preferred), or Linux Noto CJK / WenQuanYi as fallback.

## License

MIT — see [LICENSE](LICENSE).
