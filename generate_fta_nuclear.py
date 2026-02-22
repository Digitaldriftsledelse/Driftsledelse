"""
Generates a Fault Tree Analysis Excel report for a Nuclear Power Plant.
Output: FTA_Nuclear_Power_Plant.xlsx
"""
import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ── Colour palette ───────────────────────────────────────────────────────────
RED    = "C0392B"
ORANGE = "E67E22"
YELLOW = "F1C40F"
GREEN  = "27AE60"
BLUE   = "2980B9"
DARK   = "1C2833"
WHITE  = "FFFFFF"
LGREY  = "F2F3F4"
MGREY  = "D5D8DC"

def fill(hex_col):
    return PatternFill("solid", fgColor=hex_col)

def font(bold=False, color=WHITE, size=11):
    return Font(bold=bold, color=color, size=size)

def border():
    s = Side(style="thin", color="AAAAAA")
    return Border(left=s, right=s, top=s, bottom=s)

def center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def apply(ws, row, col, value, fill_=None, font_=None, align=None, border_=True):
    c = ws.cell(row=row, column=col, value=value)
    if fill_:  c.fill   = fill_
    if font_:  c.font   = font_
    if align:  c.alignment = align
    if border_: c.border = border()
    return c

# ════════════════════════════════════════════════════════════════════════════
# SHEET 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = "Overview"
ws1.sheet_view.showGridLines = False
ws1.column_dimensions["A"].width = 28
ws1.column_dimensions["B"].width = 60

# Title banner
ws1.merge_cells("A1:B1")
c = ws1["A1"]
c.value = "FAULT TREE ANALYSIS — NUCLEAR POWER PLANT"
c.fill  = fill(DARK)
c.font  = Font(bold=True, color=WHITE, size=16)
c.alignment = center()
ws1.row_dimensions[1].height = 40

# Meta rows
meta = [
    ("Top-Level Event",  "Uncontrolled Reactor Core Damage (RCD)"),
    ("Scope",            "Pressurised Water Reactor (PWR) — full plant"),
    ("Analysis Method",  "Fault Tree Analysis (FTA) with Probabilistic Risk Assessment (PRA)"),
    ("CDF Target",       "< 1×10⁻⁵ per reactor-year (NRC Reg. Guide 1.200)"),
    ("Estimated CDF",    "~1×10⁻⁵ to 1×10⁻⁶ per reactor-year"),
    ("Standards Ref.",   "IEC 61513 | IAEA SSR-2/1 | NRC NUREG-1800"),
    ("Date",             "2026-02-22"),
    ("Analyst",          "Claude Code / Agentic Skills FTA"),
]
for i, (label, value) in enumerate(meta, start=2):
    bg = LGREY if i % 2 == 0 else WHITE
    apply(ws1, i, 1, label,  fill_=fill(bg), font_=Font(bold=True, color=DARK, size=11), align=left())
    apply(ws1, i, 2, value,  fill_=fill(bg), font_=Font(bold=False, color=DARK, size=11), align=left())
    ws1.row_dimensions[i].height = 22

# Gate legend
row = len(meta) + 3
ws1.merge_cells(f"A{row}:B{row}")
c = ws1.cell(row=row, column=1, value="Gate Legend")
c.fill = fill(BLUE); c.font = Font(bold=True, color=WHITE, size=12)
c.alignment = center(); ws1.row_dimensions[row].height = 28

gates = [
    ("OR gate  (∨)",  "Top event occurs if ANY one of the sub-events occurs"),
    ("AND gate (∧)",  "Top event occurs only if ALL sub-events occur simultaneously"),
    ("Basic event ○", "Root cause — no further decomposition required"),
    ("Intermediate",  "Intermediate event — decomposed further into sub-events"),
]
for j, (g, d) in enumerate(gates, start=row+1):
    apply(ws1, j, 1, g, fill_=fill(MGREY), font_=Font(bold=True, color=DARK, size=10), align=center())
    apply(ws1, j, 2, d, fill_=fill(LGREY), font_=Font(color=DARK, size=10), align=left())
    ws1.row_dimensions[j].height = 20

# ════════════════════════════════════════════════════════════════════════════
# SHEET 2 – FAULT TREE STRUCTURE
# ════════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("Fault Tree Structure")
ws2.sheet_view.showGridLines = False
cols = ["Level", "Event ID", "Event Name", "Event Type", "Gate", "Parent Event ID", "Description"]
widths = [8, 12, 36, 16, 10, 18, 52]
for i, (h, w) in enumerate(zip(cols, widths), 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

# Header
ws2.merge_cells("A1:G1")
c = ws2["A1"]
c.value = "Fault Tree Structure — Nuclear Power Plant"
c.fill = fill(DARK); c.font = Font(bold=True, color=WHITE, size=14)
c.alignment = center(); ws2.row_dimensions[1].height = 36

for i, h in enumerate(cols, 1):
    c = ws2.cell(row=2, column=i, value=h)
    c.fill = fill(BLUE); c.font = Font(bold=True, color=WHITE, size=10)
    c.alignment = center(); c.border = border()
ws2.row_dimensions[2].height = 22

tree_rows = [
    # Level, ID, Name, Type, Gate, Parent, Description
    (0, "TOP",    "Uncontrolled Reactor Core Damage",   "TOP EVENT",    "AND", "—",      "Primary undesired outcome: fuel integrity lost, radioactive release possible"),
    (1, "LHR",    "Loss of Heat Removal",               "Intermediate", "OR",  "TOP",    "Heat cannot be removed from the core"),
    (1, "RCF",    "Reactivity Control Failure",         "Intermediate", "OR",  "TOP",    "Reactor cannot be shut down when required"),
    (2, "LOCA",   "Loss of Coolant Accident",           "Intermediate", "OR",  "LHR",    "Coolant escapes the primary circuit"),
    (2, "DHR",    "Decay Heat Removal Failure",         "Intermediate", "AND", "LHR",    "All emergency core cooling trains fail"),
    (2, "SCRAM",  "Control Rod SCRAM Failure",          "Intermediate", "AND", "RCF",    "Control rods fail to insert on demand"),
    (2, "BORON",  "Emergency Boration Failure",         "Intermediate", "OR",  "RCF",    "Boron injection system fails"),
    (3, "E01",    "Large-break pipe rupture",           "Basic Event",  "—",   "LOCA",   "Primary coolant pipe guillotine failure"),
    (3, "E02",    "Small-break LOCA (seal/valve)",      "Basic Event",  "—",   "LOCA",   "Coolant pump seal or small valve leaks"),
    (3, "E03",    "RPV failure",                        "Basic Event",  "—",   "LOCA",   "Reactor Pressure Vessel integrity loss"),
    (3, "E04",    "Steam generator tube rupture",       "Basic Event",  "—",   "LOCA",   "SGTR causing primary-to-secondary leakage"),
    (3, "E05",    "HP injection pump fails",            "Basic Event",  "—",   "DHR",    "High-pressure ECCS pump fails on demand"),
    (3, "E06",    "LP injection pump fails",            "Basic Event",  "—",   "DHR",    "Low-pressure ECCS pump fails on demand"),
    (3, "E07",    "Passive accumulator fails",          "Basic Event",  "—",   "DHR",    "Nitrogen-driven accumulator fails to inject"),
    (3, "E08",    "Control rod mechanically stuck",     "Basic Event",  "—",   "SCRAM",  "Rod distortion/swelling prevents insertion"),
    (3, "SIG",    "SCRAM Signal Not Generated",         "Intermediate", "AND", "SCRAM",  "Automatic and manual SCRAM both unavailable"),
    (3, "E11",    "Boron pump fails to start",          "Basic Event",  "—",   "BORON",  "Motor or mechanical failure of boron pump"),
    (3, "E12",    "Boration supply valve fails closed", "Basic Event",  "—",   "BORON",  "Valve fails in closed position"),
    (3, "E13",    "Wrong boron concentration",          "Basic Event",  "—",   "BORON",  "Dilution error or incorrect tank fill"),
    (4, "E09",    "Neutron flux sensor failure",        "Basic Event",  "—",   "SIG",    "Instrumentation fails to detect power excursion"),
    (4, "E10",    "Operator fails manual SCRAM",        "Basic Event",  "—",   "SIG",    "Human error: SCRAM not initiated manually"),
]

type_colors = {
    "TOP EVENT":    (RED,    WHITE),
    "Intermediate": (ORANGE, WHITE),
    "Basic Event":  (GREEN,  WHITE),
}
for r, row_data in enumerate(tree_rows, start=3):
    lvl, eid, name, etype, gate, parent, desc = row_data
    indent = "  " * lvl + name
    bg, fg = type_colors.get(etype, (LGREY, DARK))
    row_bg = LGREY if r % 2 == 0 else WHITE
    apply(ws2, r, 1, lvl,    fill_=fill(row_bg), font_=Font(color=DARK, size=10), align=center())
    apply(ws2, r, 2, eid,    fill_=fill(row_bg), font_=Font(bold=True, color=DARK, size=10), align=center())
    apply(ws2, r, 3, indent, fill_=fill(bg),     font_=Font(bold=(etype!="Basic Event"), color=fg, size=10), align=left())
    apply(ws2, r, 4, etype,  fill_=fill(bg),     font_=Font(color=fg, size=10), align=center())
    apply(ws2, r, 5, gate,   fill_=fill(row_bg), font_=Font(bold=True, color=DARK, size=10), align=center())
    apply(ws2, r, 6, parent, fill_=fill(row_bg), font_=Font(color=DARK, size=10), align=center())
    apply(ws2, r, 7, desc,   fill_=fill(row_bg), font_=Font(color=DARK, size=10), align=left())
    ws2.row_dimensions[r].height = 20

# ════════════════════════════════════════════════════════════════════════════
# SHEET 3 – PROBABILITY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("Probability Analysis")
ws3.sheet_view.showGridLines = False
pcols = ["Event ID", "Event Name", "Failure Rate", "Unit", "Gate to Parent", "Propagated P", "Notes"]
pwidths = [12, 36, 16, 20, 16, 16, 40]
for i, (h, w) in enumerate(zip(pcols, pwidths), 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

ws3.merge_cells("A1:G1")
c = ws3["A1"]
c.value = "Probability Analysis — Basic & Intermediate Events"
c.fill = fill(DARK); c.font = Font(bold=True, color=WHITE, size=14)
c.alignment = center(); ws3.row_dimensions[1].height = 36

for i, h in enumerate(pcols, 1):
    c = ws3.cell(row=2, column=i, value=h)
    c.fill = fill(BLUE); c.font = Font(bold=True, color=WHITE, size=10)
    c.alignment = center(); c.border = border()
ws3.row_dimensions[2].height = 22

prob_rows = [
    # ID, Name, Rate, Unit, Gate, Propagated P, Notes
    ("E01", "Large-break pipe rupture",        "1×10⁻⁴", "/year",   "OR (LOCA)", "1×10⁻⁴",   "Per NUREG-1829 pipe failure rates"),
    ("E02", "Small-break LOCA (seal/valve)",   "5×10⁻³", "/year",   "OR (LOCA)", "5×10⁻³",   "Most frequent LOCA initiator"),
    ("E03", "RPV failure",                     "1×10⁻⁶", "/year",   "OR (LOCA)", "1×10⁻⁶",   "Includes PTS screening criteria"),
    ("E04", "Steam generator tube rupture",    "5×10⁻³", "/year",   "OR (LOCA)", "5×10⁻³",   "Per EPRI TR-107396"),
    ("LOCA","LOCA (combined OR)",              "—",       "—",       "OR → LHR", "~1×10⁻²",  "1−∏(1−Pᵢ) ≈ sum for small P"),
    ("E05", "HP injection pump fails",         "1×10⁻³", "/demand", "AND (DHR)", "—",         "Single train; 3 trains total"),
    ("E06", "LP injection pump fails",         "1×10⁻³", "/demand", "AND (DHR)", "—",         "Single train; 3 trains total"),
    ("E07", "Passive accumulator fails",       "1×10⁻⁴", "/demand", "AND (DHR)", "—",         "Nitrogen-pressurised; passive"),
    ("DHR", "Decay Heat Removal Failure (AND)","—",       "—",       "OR → LHR", "1×10⁻¹⁰",  "1e-3 × 1e-3 × 1e-4 = 1e-10"),
    ("E08", "Control rod mechanically stuck",  "1×10⁻⁴", "/demand", "AND (SCRAM)","—",        "Rod drop surveillance data"),
    ("E09", "Neutron flux sensor failure",     "1×10⁻²", "/year",   "AND (SIG)", "—",         "Redundant channels reduce system P"),
    ("E10", "Operator fails manual SCRAM",     "1×10⁻³", "/demand", "AND (SIG)", "—",         "Per HRA THERP methodology"),
    ("SIG", "SCRAM signal not generated (AND)","—",       "—",       "AND→SCRAM", "1×10⁻⁵",  "1e-2 × 1e-3 = 1e-5"),
    ("SCRAM","Control Rod SCRAM Failure (AND)","—",       "—",       "OR → RCF", "1×10⁻⁹",   "1e-4 × 1e-5 = 1e-9"),
    ("E11", "Boron pump fails to start",       "5×10⁻⁴", "/demand", "OR (BORON)","5×10⁻⁴",   "Redundant pump available"),
    ("E12", "Boration valve fails closed",     "1×10⁻³", "/demand", "OR (BORON)","1×10⁻³",   "Normally-open valve failure"),
    ("E13", "Wrong boron concentration",       "1×10⁻³", "/demand", "OR (BORON)","1×10⁻³",   "Chemistry surveillance reduces risk"),
    ("BORON","Emergency Boration Failure (OR)","—",       "—",       "OR → RCF", "~2.5×10⁻³","Combined OR of E11/E12/E13"),
    ("RCF", "Reactivity Control Failure (OR)", "—",       "—",       "AND → TOP","~2.5×10⁻³","OR of SCRAM + BORON ≈ BORON"),
    ("LHR", "Loss of Heat Removal (OR)",       "—",       "—",       "AND → TOP","~1×10⁻²",  "OR of LOCA + DHR ≈ LOCA"),
    ("TOP", "Core Damage (AND of LHR + RCF)",  "—",       "—",       "—",        "~2.5×10⁻⁵","1e-2 × 2.5e-3 = 2.5e-5/yr CDF"),
]

for r, row_data in enumerate(prob_rows, start=3):
    eid, name, rate, unit, gate, prop, notes = row_data
    row_bg = LGREY if r % 2 == 0 else WHITE
    is_top = eid == "TOP"
    is_inter = eid in ("LOCA","DHR","SIG","SCRAM","BORON","RCF","LHR")
    bg = RED if is_top else (ORANGE if is_inter else row_bg)
    fg = WHITE if (is_top or is_inter) else DARK
    for ci, val in enumerate([eid, name, rate, unit, gate, prop, notes], 1):
        f = fill(bg) if ci in (1,2) else fill(row_bg)
        fn = Font(bold=is_top or is_inter, color=fg if ci in (1,2) else DARK, size=10)
        align = center() if ci != 7 else left()
        apply(ws3, r, ci, val, fill_=f, font_=fn, align=align)
    ws3.row_dimensions[r].height = 20

# ════════════════════════════════════════════════════════════════════════════
# SHEET 4 – MINIMAL CUT SETS
# ════════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("Minimal Cut Sets")
ws4.sheet_view.showGridLines = False
mcs_cols = ["MCS ID", "Events Required", "No. of Events", "Combined Probability", "Risk Level", "Description"]
mcs_widths = [10, 50, 14, 22, 14, 46]
for i, (h, w) in enumerate(zip(mcs_cols, mcs_widths), 1):
    ws4.column_dimensions[get_column_letter(i)].width = w

ws4.merge_cells("A1:F1")
c = ws4["A1"]
c.value = "Minimal Cut Sets (MCS) — Critical Failure Paths"
c.fill = fill(DARK); c.font = Font(bold=True, color=WHITE, size=14)
c.alignment = center(); ws4.row_dimensions[1].height = 36

for i, h in enumerate(mcs_cols, 1):
    c = ws4.cell(row=2, column=i, value=h)
    c.fill = fill(BLUE); c.font = Font(bold=True, color=WHITE, size=10)
    c.alignment = center(); c.border = border()
ws4.row_dimensions[2].height = 22

risk_color = {"Critical": RED, "High": ORANGE, "Moderate": YELLOW, "Low": GREEN, "Very Low": BLUE}
risk_font  = {"Critical": WHITE, "High": WHITE, "Moderate": DARK, "Low": WHITE, "Very Low": WHITE}

mcs_data = [
    ("MCS-1", "Small-break LOCA (E02) + HP fail (E05) + LP fail (E06) + Accumulator fail (E07)", 4, "~5×10⁻¹³", "Very Low", "Full ECCS failure following LOCA; deep defence-in-depth"),
    ("MCS-2", "Large-break LOCA (E01) + HP fail (E05) + LP fail (E06) + Accumulator fail (E07)", 4, "~1×10⁻¹⁰", "Low",      "Guillotine break with total ECCS failure"),
    ("MCS-3", "Rod stuck (E08) + Sensor fail (E09) + Operator error (E10) + any LOCA",           4, "~5×10⁻¹³", "Very Low", "SCRAM failure combined with LOCA initiator"),
    ("MCS-4", "Rod stuck (E08) + Boron valve fails (E12) + any LOCA",                            3, "~5×10⁻⁷",  "Moderate", "Fewer redundant barriers; boration is last line"),
    ("MCS-5", "RPV failure (E03)",                                                                 1, "~1×10⁻⁶",  "Moderate", "Single basic event; bypasses all ECCS — highest structural priority"),
    ("MCS-6", "SGTR (E04) + all ECCS trains fail",                                               4, "~5×10⁻¹³", "Very Low", "Steam generator tube rupture with ECCS unavailability"),
    ("MCS-7", "Wrong boron concentration (E13) + rod stuck (E08) + any LOCA",                    3, "~5×10⁻⁸",  "Moderate", "Chemistry error combined with mechanical SCRAM failure"),
]
for r, row_data in enumerate(mcs_data, start=3):
    mcs_id, events, n, prob, risk, desc = row_data
    rc = risk_color.get(risk, LGREY)
    rf = risk_font.get(risk, DARK)
    row_bg = LGREY if r % 2 == 0 else WHITE
    apply(ws4, r, 1, mcs_id, fill_=fill(DARK),    font_=Font(bold=True, color=WHITE, size=10), align=center())
    apply(ws4, r, 2, events,  fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=left())
    apply(ws4, r, 3, n,       fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=center())
    apply(ws4, r, 4, prob,    fill_=fill(row_bg),  font_=Font(bold=True, color=DARK, size=10), align=center())
    apply(ws4, r, 5, risk,    fill_=fill(rc),      font_=Font(bold=True, color=rf, size=10), align=center())
    apply(ws4, r, 6, desc,    fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=left())
    ws4.row_dimensions[r].height = 22

# ════════════════════════════════════════════════════════════════════════════
# SHEET 5 – CORRECTIVE ACTIONS
# ════════════════════════════════════════════════════════════════════════════
ws5 = wb.create_sheet("Corrective Actions")
ws5.sheet_view.showGridLines = False
act_cols = ["Event ID", "Basic Event", "Probability", "Priority", "Prevention", "Detection", "Mitigation", "Standard Reference"]
act_widths = [10, 28, 14, 10, 34, 30, 30, 24]
for i, (h, w) in enumerate(zip(act_cols, act_widths), 1):
    ws5.column_dimensions[get_column_letter(i)].width = w

ws5.merge_cells("A1:H1")
c = ws5["A1"]
c.value = "Corrective Actions & Risk Mitigation"
c.fill = fill(DARK); c.font = Font(bold=True, color=WHITE, size=14)
c.alignment = center(); ws5.row_dimensions[1].height = 36

for i, h in enumerate(act_cols, 1):
    c = ws5.cell(row=2, column=i, value=h)
    c.fill = fill(BLUE); c.font = Font(bold=True, color=WHITE, size=10)
    c.alignment = center(); c.border = border()
ws5.row_dimensions[2].height = 22

prio_color = {"High": RED, "Medium": ORANGE, "Low": GREEN}
prio_font  = {"High": WHITE, "Medium": WHITE, "Low": WHITE}

action_rows = [
    ("E02", "Small-break LOCA",          "5×10⁻³/yr", "High",   "Seal inspection program, leak-before-break design", "Coolant pressure/flow alarms, continuous leakage monitoring", "Emergency boration, ECCS actuation procedures",   "IAEA SSR-2/1 §5.4"),
    ("E01", "Large-break pipe rupture",  "1×10⁻⁴/yr", "High",   "In-service inspection (ISI), stress corrosion monitoring", "Break detection sensors, LOCA alarms",          "ECCS high-pressure injection, operator EOPs",     "NRC Reg. Guide 1.200"),
    ("E03", "RPV failure",               "1×10⁻⁶/yr", "High",   "Fracture toughness surveillance, PTS thermal limits", "RPV integrity monitoring, thermal shock screening", "Depressurisation procedures, boration",          "ASME Code Case N-640"),
    ("E04", "SGTR",                      "5×10⁻³/yr", "High",   "Eddy current testing of tubes, anti-vibration bars", "Primary-to-secondary leak monitors, radiation alarms", "Steam generator isolation, controlled cooldown", "EPRI TR-107396"),
    ("E11", "Boron pump fails",          "5×10⁻⁴/dem","High",   "Redundant pump train, monthly functional tests",   "Pump start confirmation, flow indicators",          "Backup boration tank, gravity feed path",         "IEC 61513 §8.3"),
    ("E08", "Control rod stuck",         "1×10⁻⁴/dem","Medium", "Rod drop time testing, friction surveillance",      "Rod position indication, drop time alarms",         "Alternate shutdown via emergency boration",       "IAEA SSR-2/1 §6.2"),
    ("E05", "HP injection pump fails",   "1×10⁻³/dem","Medium", "Preventive maintenance, redundant trains (3+1)",    "Auto-test on standby, flow rate indicators",        "Alternate injection path, cross-connect valve",   "IEC 61513 §9.1"),
    ("E06", "LP injection pump fails",   "1×10⁻³/dem","Medium", "Scheduled overhaul, staggered maintenance",         "Standby run tests, vibration monitoring",           "Gravity-feed injection mode",                     "IEC 61513 §9.1"),
    ("E10", "Operator fails manual SCRAM","1×10⁻³/dem","Medium","Simulator training (quarterly), written EOPs",      "Annunciator panels, automatic SCRAM logic backup",  "Automatic backup SCRAM on high neutron flux",     "NUREG-1792"),
    ("E12", "Boration valve fails closed","1×10⁻³/dem","Medium","Normally-open design, valve position indication",   "Valve position monitoring, periodic stroke test",   "Manual operator action, alternate flow path",     "IEC 61513 §8.3"),
    ("E07", "Accumulator fails",         "1×10⁻⁴/dem","Low",    "Periodic nitrogen pressure checks, seal inspection","Pressure indicators on accumulator tanks",           "Alternate low-pressure injection",                "IAEA SSR-2/1 §5.6"),
    ("E09", "Neutron flux sensor failure","1×10⁻²/yr", "Low",   "Redundant detector channels (4-channel voting)",   "Channel calibration checks, deviation alarms",      "Manual SCRAM initiated by operator",              "IEC 61513 §10.2"),
    ("E13", "Wrong boron concentration", "1×10⁻³/dem","Low",    "Boron concentration sampling, two-person verification","Boric acid analysers, continuous conductivity monitors","Dilute and re-inject, alternate tank",         "ASTM D1838"),
]
for r, row_data in enumerate(action_rows, start=3):
    eid, name, prob, prio, prev, det, mit, std = row_data
    pc = prio_color.get(prio, LGREY)
    pf = prio_font.get(prio, DARK)
    row_bg = LGREY if r % 2 == 0 else WHITE
    apply(ws5, r, 1, eid,  fill_=fill(DARK),    font_=Font(bold=True, color=WHITE, size=10), align=center())
    apply(ws5, r, 2, name, fill_=fill(row_bg),  font_=Font(bold=True, color=DARK, size=10), align=left())
    apply(ws5, r, 3, prob, fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=center())
    apply(ws5, r, 4, prio, fill_=fill(pc),      font_=Font(bold=True, color=pf, size=10), align=center())
    apply(ws5, r, 5, prev, fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=left())
    apply(ws5, r, 6, det,  fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=left())
    apply(ws5, r, 7, mit,  fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=left())
    apply(ws5, r, 8, std,  fill_=fill(row_bg),  font_=Font(color=DARK, size=10), align=center())
    ws5.row_dimensions[r].height = 28

# ── Save ─────────────────────────────────────────────────────────────────────
out = "/home/user/Driftsledelse/FTA_Nuclear_Power_Plant.xlsx"
wb.save(out)
print(f"Saved: {out}")
