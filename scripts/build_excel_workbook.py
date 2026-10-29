"""
Excel Workbook Builder
Creates a comprehensive, macro-free, multi-sheet Excel analytics workbook:
excel/Enterprise_IT_Service_Desk_Analytics.xlsx

Sheets:
1. Raw_Data (10,008 rows)
2. Cleaned_Data (10,000 rows formatted as Excel Table)
3. Data_Quality (Audit log, remediation matrix, excluded records)
4. KPI_Summary (Executive KPI cards with live Excel formulas)
5. Pivot_Analysis (Structured multi-dimensional pivot summary tables)
6. Business_Insights (Executive findings, root causes, management recommendations)
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_workbook():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "itsm_tickets_raw.csv")
    cleaned_path = os.path.join(base_dir, "data", "cleaned", "itsm_tickets_cleaned.csv")
    excel_dir = os.path.join(base_dir, "excel")
    os.makedirs(excel_dir, exist_ok=True)
    excel_output = os.path.join(excel_dir, "Enterprise_IT_Service_Desk_Analytics.xlsx")

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    navy_header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    navy_header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    title_font = Font(name="Calibri", size=16, bold=True, color="1B365D")
    subtitle_font = Font(name="Calibri", size=11, italic=True, color="555555")
    section_font = Font(name="Calibri", size=13, bold=True, color="1B365D")
    bold_font = Font(name="Calibri", size=11, bold=True)
    regular_font = Font(name="Calibri", size=11)
    
    kpi_num_font = Font(name="Calibri", size=18, bold=True, color="1B365D")
    kpi_sub_font = Font(name="Calibri", size=9, italic=True, color="666666")

    card_fill = PatternFill(start_color="F4F7FA", end_color="F4F7FA", fill_type="solid")
    green_fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    red_fill = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")
    accent_fill = PatternFill(start_color="EAEFF5", end_color="EAEFF5", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    card_border = Border(
        left=Side(style='medium', color='1B365D'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # =========================================================================
    # SHEET 1: Raw_Data
    # =========================================================================
    print("Building Sheet 1: Raw_Data...")
    ws_raw = wb.create_sheet(title="Raw_Data")
    ws_raw.views.sheetView[0].showGridLines = True

    with open(raw_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r_idx, row in enumerate(reader, start=1):
            ws_raw.append(row)
            if r_idx == 1:
                for col_idx in range(1, len(row) + 1):
                    cell = ws_raw.cell(row=1, column=col_idx)
                    cell.fill = navy_header_fill
                    cell.font = navy_header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")

    # =========================================================================
    # SHEET 2: Cleaned_Data
    # =========================================================================
    print("Building Sheet 2: Cleaned_Data...")
    ws_clean = wb.create_sheet(title="Cleaned_Data")
    ws_clean.views.sheetView[0].showGridLines = True

    with open(cleaned_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        ws_clean.append(headers)

        for col_idx in range(1, len(headers) + 1):
            cell = ws_clean.cell(row=1, column=col_idx)
            cell.fill = navy_header_fill
            cell.font = navy_header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        for r_idx, row in enumerate(reader, start=2):
            parsed_row = []
            for c_idx, val in enumerate(row):
                if val == "":
                    parsed_row.append(None)
                elif c_idx in [10, 11]: # SLA_Target_Hours, Actual_Resolution_Hours
                    try:
                        parsed_row.append(float(val))
                    except ValueError:
                        parsed_row.append(val)
                elif c_idx in [13, 14, 15]: # CSAT, Reopened, Escalated
                    try:
                        parsed_row.append(int(val))
                    except ValueError:
                        parsed_row.append(val)
                else:
                    parsed_row.append(val)
            ws_clean.append(parsed_row)

    # Format numbers in Cleaned_Data
    for row_idx in range(2, 10002):
        # Target Hours (col K = 11)
        ws_clean.cell(row=row_idx, column=11).number_format = "0.0"
        # Actual Hours (col L = 12)
        if ws_clean.cell(row=row_idx, column=12).value is not None:
            ws_clean.cell(row=row_idx, column=12).number_format = "0.00"

    # =========================================================================
    # SHEET 3: Data_Quality
    # =========================================================================
    print("Building Sheet 3: Data_Quality...")
    ws_dq = wb.create_sheet(title="Data_Quality")
    ws_dq.views.sheetView[0].showGridLines = True

    ws_dq["B2"] = "ITSM Data Quality & Validation Audit Report"
    ws_dq["B2"].font = title_font
    ws_dq["B3"] = "Audit reconciliation of 10,008 raw records to 10,000 validated production records."
    ws_dq["B3"].font = subtitle_font

    # Summary Cards
    cards = [
        ("Raw Records Ingested", "10,008", "Full uncleaned extraction extract", "B5", "C6"),
        ("Anomalies Excluded", "8", "5 duplicates + 3 test records", "D5", "E6"),
        ("Production Records", "10,000", "Clean fact dataset (100% integrity)", "F5", "G6"),
        ("Data Quality Score", "100.0%", "Verified across 8 business rules", "H5", "I6")
    ]
    for title, val, sub, top_left, bot_right in cards:
        ws_dq[top_left] = title
        ws_dq[top_left].font = bold_font
        ws_dq[top_left].alignment = Alignment(horizontal="center")
        
        # Merge cells for card value
        c_col = top_left[0]
        c_row = int(top_left[1])
        ws_dq[f"{c_col}{c_row+1}"] = val
        ws_dq[f"{c_col}{c_row+1}"].font = kpi_num_font
        ws_dq[f"{c_col}{c_row+1}"].alignment = Alignment(horizontal="center")
        
        ws_dq[f"{c_col}{c_row+2}"] = sub
        ws_dq[f"{c_col}{c_row+2}"].font = kpi_sub_font
        ws_dq[f"{c_col}{c_row+2}"].alignment = Alignment(horizontal="center")
        
        for r in range(c_row, c_row + 3):
            for c in [ord(c_col) - ord('A') + 1, ord(c_col) - ord('A') + 2]:
                cell = ws_dq.cell(row=r, column=c)
                cell.fill = card_fill
                cell.border = thin_border

    # Rules Table
    ws_dq["B9"] = "Data Quality Verification Rules & Remediation Matrix"
    ws_dq["B9"].font = section_font

    dq_headers = ["Rule #", "Verification Check", "Target Field", "Anomalies Found", "Remediation Action Taken", "Status"]
    for c_idx, h in enumerate(dq_headers, start=2):
        cell = ws_dq.cell(row=11, column=c_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = navy_header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    rules_data = [
        (1, "Deduplication", "Ticket_ID", "5 duplicate rows", "Removed exact duplicate records from simulated webhook retries", "PASS"),
        (2, "Test Record Filter", "Ticket_ID", "3 QA test records", "Filtered out non-production test entries (TEST-9901, TEST-9902, DEV-SMOKE-01)", "PASS"),
        (3, "String Hygiene", "Category, Priority, Dept", "5 records with spaces", "Applied automated TRIM() across all categorical columns", "PASS"),
        (4, "Casing Normalization", "Priority, Status, Team", "9 casing variants", "Standardized all categorical text to proper Title Case", "PASS"),
        (5, "SLA Target Mapping", "SLA_Target_Hours", "1 mismatch", "Enforced contractual hours matrix (Critical=4h, High=8h, Medium=24h, Low=72h)", "PASS"),
        (6, "Date Duration Logic", "Created & Resolved Date", "0 violations", "Verified Resolved_Date strictly >= Created_Date (0 negative durations)", "PASS"),
        (7, "Resolved Completeness", "Resolved_Date & Actual_Hours", "0 violations", "Ensured 100% of resolved tickets have valid resolution dates and positive hours", "PASS"),
        (8, "Open Status Integrity", "Resolved_Date & Actual_Hours", "1 spurious date", "Enforced strict NULLs for resolution dates/actual hours on active open tickets", "PASS"),
    ]

    for r_idx, r_data in enumerate(rules_data, start=12):
        for c_idx, val in enumerate(r_data, start=2):
            cell = ws_dq.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 2:
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 7:
                cell.alignment = Alignment(horizontal="center")
                cell.fill = green_fill
                cell.font = bold_font

    # Excluded Records Table
    ws_dq["B22"] = "Log of Excluded Non-Production Records"
    ws_dq["B22"].font = section_font

    exc_headers = ["Ticket_ID", "Original Source", "Priority", "Category", "Reason for Exclusion"]
    for c_idx, h in enumerate(exc_headers, start=2):
        cell = ws_dq.cell(row=24, column=c_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = navy_header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    exc_data = [
        ("TCK-10151", "Raw Extract (Row 10009)", "High", "Hardware & Workstation", "Exact duplicate copy of ticket TCK-10151"),
        ("TCK-11201", "Raw Extract (Row 10010)", "Medium", "Access & Identity", "Exact duplicate copy of ticket TCK-11201"),
        ("TCK-13401", "Raw Extract (Row 10011)", "Medium", "Cloud & Infrastructure", "Exact duplicate copy of ticket TCK-13401"),
        ("TCK-16801", "Raw Extract (Row 10012)", "Low", "Software & Applications", "Exact duplicate copy of ticket TCK-16801"),
        ("TCK-19101", "Raw Extract (Row 10013)", "Critical", "Network & Connectivity", "Exact duplicate copy of ticket TCK-19101"),
        ("TEST-9901", "QA Testing Environment", "Medium", "TEST_CATEGORY", "QA synthetic smoke test ticket"),
        ("TEST-9902", "QA Automation Suite", "Medium", "QA_AUTOMATION", "Automated regression test entry"),
        ("DEV-SMOKE-01", "Developer Sandbox", "P1_URGENT_TEST", "Hardware & Workstation", "Developer deployment validation entry")
    ]
    for r_idx, e_data in enumerate(exc_data, start=25):
        for c_idx, val in enumerate(e_data, start=2):
            cell = ws_dq.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 2:
                cell.font = bold_font

    # =========================================================================
    # SHEET 4: KPI_Summary (Live Native Excel Formulas)
    # =========================================================================
    print("Building Sheet 4: KPI_Summary with live formulas...")
    ws_kpi = wb.create_sheet(title="KPI_Summary")
    ws_kpi.views.sheetView[0].showGridLines = True

    ws_kpi["B2"] = "ITSM Executive Service Desk KPI Dashboard"
    ws_kpi["B2"].font = title_font
    ws_kpi["B3"] = "Performance scorecard calculated using dynamic Excel formulas referencing Cleaned_Data."
    ws_kpi["B3"].font = subtitle_font

    # Top KPI Cards using Excel Formulas
    kpis = [
        ("Total Intake Tickets", "=COUNTA(Cleaned_Data!A2:A10001)", "Total volume (100% fact)", "B5", "C7", "#,##0"),
        ("Resolved Tickets", '=COUNTIF(Cleaned_Data!D2:D10001, "Resolved") + COUNTIF(Cleaned_Data!D2:D10001, "Closed")', "Completed incidents", "D5", "E7", "#,##0"),
        ("Active Open Backlog", '=COUNTIFS(Cleaned_Data!D2:D10001, "<>Resolved", Cleaned_Data!D2:D10001, "<>Closed")', "In Progress, Pending, New", "F5", "G7", "#,##0"),
        ("Resolution Rate", "=D6/B6", "Resolved / Total Intake", "H5", "I7", "0.00%"),
        
        ("SLA Met Tickets", '=COUNTIF(Cleaned_Data!M2:M10001, "Met")', "Resolved within SLA window", "B9", "C11", "#,##0"),
        ("SLA Breached Tickets", '=COUNTIF(Cleaned_Data!M2:M10001, "Breached")', "Resolution exceeded SLA", "D9", "E11", "#,##0"),
        ("SLA Compliance Rate", "=B10/D6", "SLA Met / Resolved (ITIL)", "F9", "G11", "0.00%"),
        ("SLA Breach Rate", "=D10/D6", "SLA Breached / Resolved", "H9", "I11", "0.00%"),

        ("Avg Resolution Hours", "=AVERAGE(Cleaned_Data!L2:L10001)", "Mean turnaround (hrs)", "B13", "C15", "0.00"),
        ("Avg SLA Target Hours", '=(SUMIF(Cleaned_Data!D2:D10001, "Resolved", Cleaned_Data!K2:K10001) + SUMIF(Cleaned_Data!D2:D10001, "Closed", Cleaned_Data!K2:K10001)) / D6', "Committed benchmark (hrs)", "D13", "E15", "0.00"),
        ("Turnaround Buffer", "=D14-B14", "Margin before breach (hrs)", "F13", "G15", "0.00"),
        ("Avg Customer CSAT", "=AVERAGE(Cleaned_Data!N2:N10001)", "Out of 5.0 (6,053 surveys)", "H13", "I15", "0.00"),

        ("Reopened Tickets", "=SUM(Cleaned_Data!O2:O10001)", "Reopened after resolution", "B17", "C19", "#,##0"),
        ("Reopened Rate (Resolved)", "=B18/D6", "Reopened / Resolved tickets", "D17", "E19", "0.00%"),
        ("Escalated Tickets", "=SUM(Cleaned_Data!P2:P10001)", "Lifecycle escalations", "F17", "G19", "#,##0"),
        ("Escalation Rate (Total)", "=F18/B6", "Escalated / Total Intake", "H17", "I19", "0.00%")
    ]

    for title, formula, sub, c_left, c_right, num_fmt in kpis:
        col = c_left[0]
        row = int(c_left[1:])
        
        ws_kpi[f"{col}{row}"] = title
        ws_kpi[f"{col}{row}"].font = bold_font
        ws_kpi[f"{col}{row}"].alignment = Alignment(horizontal="center")
        
        ws_kpi[f"{col}{row+1}"] = formula
        ws_kpi[f"{col}{row+1}"].font = kpi_num_font
        ws_kpi[f"{col}{row+1}"].alignment = Alignment(horizontal="center")
        ws_kpi[f"{col}{row+1}"].number_format = num_fmt
        
        ws_kpi[f"{col}{row+2}"] = sub
        ws_kpi[f"{col}{row+2}"].font = kpi_sub_font
        ws_kpi[f"{col}{row+2}"].alignment = Alignment(horizontal="center")

        # Styling Card Block
        c_num = ord(col) - ord('A') + 1
        for r in range(row, row + 3):
            for c in [c_num, c_num + 1]:
                cell = ws_kpi.cell(row=r, column=c)
                cell.fill = card_fill
                cell.border = thin_border

    # Section: Breakdown by Priority Table (Formula Driven)
    ws_kpi["B22"] = "SLA Performance by Priority Level"
    ws_kpi["B22"].font = section_font

    p_headers = ["Priority", "SLA Target", "Total Tickets", "Resolved", "SLA Met", "SLA Breached", "Compliance %", "Breach %", "Avg Res (hrs)"]
    for c_idx, h in enumerate(p_headers, start=2):
        cell = ws_kpi.cell(row=24, column=c_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = navy_header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    priorities = [
        ("Critical", "4.0 hrs", 25),
        ("High", "8.0 hrs", 26),
        ("Medium", "24.0 hrs", 27),
        ("Low", "72.0 hrs", 28)
    ]

    for p_name, p_target, r in priorities:
        ws_kpi.cell(row=r, column=2, value=p_name).font = bold_font
        ws_kpi.cell(row=r, column=3, value=p_target).alignment = Alignment(horizontal="center")
        
        # Total
        c_tot = ws_kpi.cell(row=r, column=4, value=f'=COUNTIF(Cleaned_Data!E2:E10001, "{p_name}")')
        c_tot.number_format = "#,##0"
        
        # Resolved
        c_res = ws_kpi.cell(row=r, column=5, value=f'=COUNTIFS(Cleaned_Data!E2:E10001, "{p_name}", Cleaned_Data!D2:D10001, "Resolved") + COUNTIFS(Cleaned_Data!E2:E10001, "{p_name}", Cleaned_Data!D2:D10001, "Closed")')
        c_res.number_format = "#,##0"
        
        # Met
        c_met = ws_kpi.cell(row=r, column=6, value=f'=COUNTIFS(Cleaned_Data!E2:E10001, "{p_name}", Cleaned_Data!M2:M10001, "Met")')
        c_met.number_format = "#,##0"
        
        # Breached
        c_brk = ws_kpi.cell(row=r, column=7, value=f'=COUNTIFS(Cleaned_Data!E2:E10001, "{p_name}", Cleaned_Data!M2:M10001, "Breached")')
        c_brk.number_format = "#,##0"
        
        # Compliance %
        c_cmp = ws_kpi.cell(row=r, column=8, value=f'=F{r}/E{r}')
        c_cmp.number_format = "0.00%"
        c_cmp.font = bold_font
        
        # Breach %
        c_brp = ws_kpi.cell(row=r, column=9, value=f'=G{r}/E{r}')
        c_brp.number_format = "0.00%"
        
        # Avg Res Hours
        c_avg = ws_kpi.cell(row=r, column=10, value=f'=AVERAGEIFS(Cleaned_Data!L2:L10001, Cleaned_Data!E2:E10001, "{p_name}")')
        c_avg.number_format = "0.00"

        for c in range(2, 11):
            ws_kpi.cell(row=r, column=c).border = thin_border

    # Priority Total Row
    ws_kpi.cell(row=29, column=2, value="Total / Average").font = bold_font
    ws_kpi.cell(row=29, column=3, value="—").alignment = Alignment(horizontal="center")
    ws_kpi.cell(row=29, column=4, value="=SUM(D25:D28)").number_format = "#,##0"
    ws_kpi.cell(row=29, column=5, value="=SUM(E25:E28)").number_format = "#,##0"
    ws_kpi.cell(row=29, column=6, value="=SUM(F25:F28)").number_format = "#,##0"
    ws_kpi.cell(row=29, column=7, value="=SUM(G25:G28)").number_format = "#,##0"
    ws_kpi.cell(row=29, column=8, value="=F29/E29").number_format = "0.00%"
    ws_kpi.cell(row=29, column=9, value="=G29/E29").number_format = "0.00%"
    ws_kpi.cell(row=29, column=10, value="=AVERAGE(Cleaned_Data!L2:L10001)").number_format = "0.00"
    for c in range(2, 11):
        cell = ws_kpi.cell(row=29, column=c)
        cell.font = bold_font
        cell.fill = accent_fill
        cell.border = thin_border

    # Section: Breakdown by Support Team Table
    ws_kpi["B32"] = "Operational Performance by Support Team"
    ws_kpi["B32"].font = section_font

    t_headers = ["Support Team", "Tier", "Total Tickets", "Resolved", "Open Backlog", "SLA Met", "SLA Breached", "Compliance %", "Avg Res (hrs)", "Avg CSAT"]
    for c_idx, h in enumerate(t_headers, start=2):
        cell = ws_kpi.cell(row=34, column=c_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = navy_header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    teams = [
        ("Service Desk - Tier 1", "Tier 1", 35),
        ("Cloud & Systems Infrastructure", "Tier 3", 36),
        ("End User Support - Tier 2", "Tier 2", 37),
        ("Network Operations", "Tier 3", 38),
        ("Identity & Access Management (IAM)", "Tier 2", 39)
    ]

    for t_name, t_tier, r in teams:
        ws_kpi.cell(row=r, column=2, value=t_name).font = bold_font
        ws_kpi.cell(row=r, column=3, value=t_tier).alignment = Alignment(horizontal="center")
        
        # Total
        ws_kpi.cell(row=r, column=4, value=f'=COUNTIF(Cleaned_Data!H2:H10001, "{t_name}")').number_format = "#,##0"
        # Resolved
        ws_kpi.cell(row=r, column=5, value=f'=COUNTIFS(Cleaned_Data!H2:H10001, "{t_name}", Cleaned_Data!D2:D10001, "Resolved") + COUNTIFS(Cleaned_Data!H2:H10001, "{t_name}", Cleaned_Data!D2:D10001, "Closed")').number_format = "#,##0"
        # Open
        ws_kpi.cell(row=r, column=6, value=f'=D{r}-E{r}').number_format = "#,##0"
        # Met
        ws_kpi.cell(row=r, column=7, value=f'=COUNTIFS(Cleaned_Data!H2:H10001, "{t_name}", Cleaned_Data!M2:M10001, "Met")').number_format = "#,##0"
        # Breached
        ws_kpi.cell(row=r, column=8, value=f'=COUNTIFS(Cleaned_Data!H2:H10001, "{t_name}", Cleaned_Data!M2:M10001, "Breached")').number_format = "#,##0"
        # Compliance %
        c_cmp = ws_kpi.cell(row=r, column=9, value=f'=G{r}/E{r}')
        c_cmp.number_format = "0.00%"
        c_cmp.font = bold_font
        # Avg Res
        ws_kpi.cell(row=r, column=10, value=f'=AVERAGEIFS(Cleaned_Data!L2:L10001, Cleaned_Data!H2:H10001, "{t_name}")').number_format = "0.00"
        # Avg CSAT
        ws_kpi.cell(row=r, column=11, value=f'=AVERAGEIFS(Cleaned_Data!N2:N10001, Cleaned_Data!H2:H10001, "{t_name}")').number_format = "0.00"

        for c in range(2, 12):
            ws_kpi.cell(row=r, column=c).border = thin_border

    # Team Total Row
    ws_kpi.cell(row=40, column=2, value="Total / Average").font = bold_font
    ws_kpi.cell(row=40, column=3, value="—").alignment = Alignment(horizontal="center")
    ws_kpi.cell(row=40, column=4, value="=SUM(D35:D39)").number_format = "#,##0"
    ws_kpi.cell(row=40, column=5, value="=SUM(E35:E39)").number_format = "#,##0"
    ws_kpi.cell(row=40, column=6, value="=SUM(F35:F39)").number_format = "#,##0"
    ws_kpi.cell(row=40, column=7, value="=SUM(G35:G39)").number_format = "#,##0"
    ws_kpi.cell(row=40, column=8, value="=SUM(H35:H39)").number_format = "#,##0"
    ws_kpi.cell(row=40, column=9, value="=G40/E40").number_format = "0.00%"
    ws_kpi.cell(row=40, column=10, value="=AVERAGE(Cleaned_Data!L2:L10001)").number_format = "0.00"
    ws_kpi.cell(row=40, column=11, value="=AVERAGE(Cleaned_Data!N2:N10001)").number_format = "0.00"
    for c in range(2, 12):
        cell = ws_kpi.cell(row=40, column=c)
        cell.font = bold_font
        cell.fill = accent_fill
        cell.border = thin_border

    # =========================================================================
    # SHEET 5: Pivot_Analysis
    # =========================================================================
    print("Building Sheet 5: Pivot_Analysis...")
    ws_pivot = wb.create_sheet(title="Pivot_Analysis")
    ws_pivot.views.sheetView[0].showGridLines = True

    ws_pivot["B2"] = "Multi-Dimensional Pivot Analysis Tables"
    ws_pivot["B2"].font = title_font
    ws_pivot["B3"] = "Cross-tabulated operational summaries. To build interactive drag-and-drop PivotTables, use Insert > PivotTable from Cleaned_Data."
    ws_pivot["B3"].font = subtitle_font

    # Pivot 1: Monthly Intake by Priority
    ws_pivot["B5"] = "Pivot Table 1: Monthly Ticket Intake Trend by Priority"
    ws_pivot["B5"].font = section_font

    p1_headers = ["Month", "Critical (P1)", "High (P2)", "Medium (P3)", "Low (P4)", "Total Tickets", "MoM Growth %"]
    for c_idx, h in enumerate(p1_headers, start=2):
        cell = ws_pivot.cell(row=7, column=c_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = navy_header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    months = [
        ("2025-10", 79, 203, 473, 212, 967, "—"),
        ("2025-11", 62, 153, 381, 186, 782, "-19.1%"),
        ("2025-12", 72, 172, 384, 196, 824, "+5.4%"),
        ("2026-01", 68, 174, 388, 187, 817, "-0.9%"),
        ("2026-02", 59, 151, 370, 178, 758, "-7.2%"),
        ("2026-03", 69, 169, 411, 192, 841, "+10.9%"),
        ("2026-04", 64, 165, 396, 190, 815, "-3.1%"),
        ("2026-05", 77, 187, 417, 206, 887, "+8.8%"),
        ("2026-06", 67, 167, 396, 189, 819, "-7.7%"),
        ("2026-07", 70, 168, 387, 201, 826, "+0.9%"),
        ("2026-08", 75, 172, 420, 202, 869, "+5.2%"),
        ("2026-09", 65, 161, 369, 200, 795, "-8.5%")
    ]

    for idx, (m_val, p1, p2, p3, p4, tot, mom) in enumerate(months, start=8):
        ws_pivot.cell(row=idx, column=2, value=m_val).alignment = Alignment(horizontal="center")
        ws_pivot.cell(row=idx, column=3, value=p1).number_format = "#,##0"
        ws_pivot.cell(row=idx, column=4, value=p2).number_format = "#,##0"
        ws_pivot.cell(row=idx, column=5, value=p3).number_format = "#,##0"
        ws_pivot.cell(row=idx, column=6, value=p4).number_format = "#,##0"
        c_t = ws_pivot.cell(row=idx, column=7, value=tot)
        c_t.number_format = "#,##0"
        c_t.font = bold_font
        ws_pivot.cell(row=idx, column=8, value=mom).alignment = Alignment(horizontal="center")

        for c in range(2, 9):
            ws_pivot.cell(row=idx, column=c).border = thin_border

    # Pivot 1 Total
    ws_pivot.cell(row=20, column=2, value="Full Year Total").font = bold_font
    ws_pivot.cell(row=20, column=3, value=827).number_format = "#,##0"
    ws_pivot.cell(row=20, column=4, value=2042).number_format = "#,##0"
    ws_pivot.cell(row=20, column=5, value=4792).number_format = "#,##0"
    ws_pivot.cell(row=20, column=6, value=2339).number_format = "#,##0"
    ws_pivot.cell(row=20, column=7, value=10000).number_format = "#,##0"
    ws_pivot.cell(row=20, column=8, value="—").alignment = Alignment(horizontal="center")
    for c in range(2, 9):
        cell = ws_pivot.cell(row=20, column=c)
        cell.font = bold_font
        cell.fill = accent_fill
        cell.border = thin_border

    # Pivot 2: Top 10 Root-Cause SLA Breaches by Subcategory
    ws_pivot["B23"] = "Pivot Table 2: Top 10 Root-Cause SLA Breach Drivers (Category & Subcategory)"
    ws_pivot["B23"].font = section_font

    p2_headers = ["Rank", "Category", "Subcategory", "Resolved", "SLA Breaches", "% of All Breaches", "Breach Rate %", "Avg Res (hrs)", "Avg CSAT"]
    for c_idx, h in enumerate(p2_headers, start=2):
        cell = ws_pivot.cell(row=25, column=c_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = navy_header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    top_breaches = [
        (1, "Network & Connectivity", "Office Wi-Fi Access", 470, 132, "7.84%", "28.09%", 26.63, 3.81),
        (2, "Network & Connectivity", "DNS & Gateway Routing", 465, 126, "7.49%", "27.10%", 30.20, 3.79),
        (3, "Network & Connectivity", "Bandwidth & Latency", 460, 106, "6.30%", "23.04%", 25.65, 3.86),
        (4, "Network & Connectivity", "LAN Cable & Port", 469, 105, "6.24%", "22.39%", 28.46, 3.94),
        (5, "Cloud & Infrastructure", "Cloud Storage Permissions", 503, 97, "5.76%", "19.28%", 26.06, 3.83),
        (6, "Cloud & Infrastructure", "Virtual Machine Crash", 480, 97, "5.76%", "20.21%", 24.78, 3.93),
        (7, "Cloud & Infrastructure", "Server Provisioning", 480, 90, "5.35%", "18.75%", 24.46, 3.76),
        (8, "Cloud & Infrastructure", "Database Connectivity", 475, 83, "4.93%", "17.47%", 26.78, 3.95),
        (9, "Hardware & Workstation", "Laptop Freeze & OS", 449, 80, "4.75%", "17.82%", 23.54, 4.12),
        (10, "Hardware & Workstation", "Peripheral Malfunction", 473, 80, "4.75%", "16.91%", 24.28, 3.96),
    ]

    for idx, row_data in enumerate(top_breaches, start=26):
        for c_idx, val in enumerate(row_data, start=2):
            cell = ws_pivot.cell(row=idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [2, 7, 8]:
                cell.alignment = Alignment(horizontal="center")
            if c_idx == 6: # Breaches count
                cell.font = bold_font
            if c_idx in [9, 10]:
                cell.number_format = "0.00"

    # =========================================================================
    # SHEET 6: Business_Insights
    # =========================================================================
    print("Building Sheet 6: Business_Insights...")
    ws_ins = wb.create_sheet(title="Business_Insights")
    ws_ins.views.sheetView[0].showGridLines = True

    ws_ins["B2"] = "Management Insights & Strategic Action Plan"
    ws_ins["B2"].font = title_font
    ws_ins["B3"] = "Evidence-based analytical findings and operational recommendations for service desk leadership."
    ws_ins["B3"].font = subtitle_font

    insights = [
        (
            "Finding 1: Network & Connectivity is the Primary Driver of Corporate SLA Breaches",
            "What the data shows: Network Operations exhibits the highest resolution duration (28.61 hrs vs 30.16h SLA) and narrowest buffer (1.55h). Four Network subcategories (Office Wi-Fi, DNS Routing, Bandwidth, and LAN Ports) occupy ranks 1 through 4 in total breaches, accounting for 469 breaches (27.87% of all corporate SLA failures).\n"
            "Why it matters to management: Network issues disrupt whole office floors, crippling business productivity and inflating user dissatisfaction.\n"
            "Action Plan: Deploy automated Wi-Fi access diagnostic scripts, upgrade gateway DNS routing redundancy, and conduct proactive port diagnostics.\n"
            "Future Metric: Track Network Operations breach rate (target reduction from 25.1% to <15%) and Wi-Fi turnaround time."
        ),
        (
            "Finding 2: SLA Breaches Cause an Immediate 1.6-Point Drop in Customer Satisfaction",
            "What the data shows: Customers whose tickets were resolved within SLA gave an average rating of 4.25 / 5.0 (82.7% gave 4 or 5 stars). In stark contrast, when an SLA was breached, average satisfaction plummeted to 2.65 / 5.0 (70.6% gave negative ratings of 1, 2, or 3 stars).\n"
            "Why it matters to management: Service level breaches directly destroy end-user trust and escalate friction between IT and business units.\n"
            "Action Plan: Establish an automated Early Warning Alert in the ITSM tool when a ticket reaches 75% of its SLA window without assignment.\n"
            "Future Metric: Correlation between SLA compliance improvement and company-wide CSAT score (target: >4.20 overall CSAT)."
        ),
        (
            "Finding 3: Heavy Backlog Concentration in Tier 1 Service Desk",
            "What the data shows: Service Desk - Tier 1 holds 220 active open tickets (45.27% of the total 486 open tickets company-wide), with 208 tickets having aged past 48 hours without closure.\n"
            "Why it matters to management: Tier 1 serves as the front door for all employee requests. A clogged Tier 1 queue delays ticket triage and artificially inflates end-to-end turnaround.\n"
            "Action Plan: Implement automated self-service password reset and basic ERP access provisioning workflows to deflect 25-30% of repetitive Tier 1 requests without adding headcount.\n"
            "Future Metric: First Contact Resolution (FCR) rate and Tier 1 queue aging percentage."
        ),
        (
            "Finding 4: Elevated Escalation Rates in Cloud and Network Infrastructure",
            "What the data shows: Cloud & Systems Infrastructure has an escalation rate of 15.37% (281 tickets) and Network Operations has 14.71% (242 tickets), compared to <9% for other support groups.\n"
            "Why it matters to management: High escalation rates signal ambiguous initial triage, inadequate documentation, or missing Tier 1 troubleshooting scripts.\n"
            "Action Plan: Develop Standard Operating Procedures (SOPs) and Tier 1 runbooks for common Cloud storage permission requests and VM restart protocols.\n"
            "Future Metric: Reduction in Cloud escalation rate from 15.37% to <10%."
        ),
        (
            "Finding 5: Reopened Ticket Churn Undermines Operational Efficiency",
            "What the data shows: 511 tickets were reopened post-resolution (5.37% reopen rate). Service Desk - Tier 1 had the highest churn with 222 reopened tickets (6.00% of resolved tickets).\n"
            "Why it matters to management: Every reopened ticket consumes double the support agent effort and signals premature ticket closure.\n"
            "Action Plan: Enforce mandatory customer confirmation or a 48-hour 'Pending Closure' validation window before a ticket is permanently marked as Closed.\n"
            "Future Metric: Track 30-day ticket reopening rate (target: <3.5%)."
        )
    ]

    curr_row = 5
    for title, desc in insights:
        ws_ins.cell(row=curr_row, column=2, value=title).font = section_font
        curr_row += 1
        
        # Merge cells for readable card
        ws_ins.merge_cells(start_row=curr_row, start_column=2, end_row=curr_row+4, end_column=10)
        cell = ws_ins.cell(row=curr_row, column=2, value=desc)
        cell.font = regular_font
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        
        for r in range(curr_row, curr_row + 5):
            for c in range(2, 11):
                c_node = ws_ins.cell(row=r, column=c)
                c_node.fill = card_fill
                c_node.border = thin_border

        curr_row += 6

    # =========================================================================
    # Auto-adjust column widths across all sheets
    # =========================================================================
    print("Adjusting column widths and polishing views...")
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            # Sample first 100 rows for speed on large sheets
            sample_rows = col[:100] if len(col) > 100 else col
            for cell in sample_rows:
                if cell.value:
                    lines = str(cell.value).split("\n")
                    for l in lines:
                        if len(l) > max_len and not str(cell.value).startswith("="):
                            max_len = len(l)
            adjusted_width = min(max(max_len + 3, 12), 45)
            sheet.column_dimensions[col_letter].width = adjusted_width

    # Save workbook
    wb.save(excel_output)
    print(f"Workbook successfully saved to: {excel_output}")

if __name__ == "__main__":
    build_excel_workbook()
