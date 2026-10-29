# Excel Analysis & Workbook Architecture Guide

**Workbook File:** [`excel/Enterprise_IT_Service_Desk_Analytics.xlsx`](file:///Users/gitanshgarg/Documents/infosys/Enterprise-IT-Service-Desk-SLA-Intelligence/excel/Enterprise_IT_Service_Desk_Analytics.xlsx) (~1.7 MB)  
**Compatibility:** Microsoft Excel 2016+, Microsoft Excel for the Web (free via OneDrive / Office.com), and Apple Numbers.  
**Architecture:** 100% macro-free (`.xlsx`), standard ANSI formulas, dynamic cell references.

---

## 1. Workbook Structure & Sheet Directory

| Sheet Tab Name | Purpose & Contents | Technical Implementation |
| :--- | :--- | :--- |
| **`Raw_Data`** | Baseline uncleaned extract (10,008 rows) preserving raw logging anomalies | Raw data ingest with stylized navy header |
| **`Cleaned_Data`** | 10,000 clean production records across 16 fields | Typed data rows, formatted numbers, dates, and SLA status flags |
| **`Data_Quality`** | Data governance audit log and remediation matrix | Summary cards, 8-rule audit table, log of 8 excluded records |
| **`KPI_Summary`** | Executive service desk dashboard with dynamic KPI cards | Dynamic Excel formulas (`COUNTA`, `COUNTIF`, `COUNTIFS`, `AVERAGEIFS`) |
| **`Pivot_Analysis`** | Cross-tabulated pivot summary tables | Monthly trend matrix, team scorecard, top 10 bottleneck rank |
| **`Business_Insights`** | Management takeaways, root cause drivers, and action plan | 5 formatted insight callouts with target KPIs and future metrics |

---

## 2. Key Formulas Used in `KPI_Summary`

Every KPI is calculated dynamically from `Cleaned_Data` using standard formulas without hardcoded numbers:

```excel
-- 1. Total Intake Tickets (10,000)
=COUNTA(Cleaned_Data!A2:A10001)

-- 2. Resolved Tickets (9,514)
=COUNTIF(Cleaned_Data!D2:D10001, "Resolved") + COUNTIF(Cleaned_Data!D2:D10001, "Closed")

-- 3. Active Open Backlog (486)
=COUNTIFS(Cleaned_Data!D2:D10001, "<>Resolved", Cleaned_Data!D2:D10001, "<>Closed")

-- 4. Resolution Rate % (95.14%)
=D6 / B6

-- 5. SLA Met Tickets (7,831)
=COUNTIF(Cleaned_Data!M2:M10001, "Met")

-- 6. SLA Breached Tickets (1,683)
=COUNTIF(Cleaned_Data!M2:M10001, "Breached")

-- 7. SLA Compliance Rate % (82.31%)
=B10 / D6   [Denominator: Resolved Tickets]

-- 8. SLA Breach Rate % (17.69%)
=D10 / D6   [Denominator: Resolved Tickets]

-- 9. Average Actual Resolution Hours (24.77 hrs)
=AVERAGE(Cleaned_Data!L2:L10001)

-- 10. Average SLA Target Hours (30.33 hrs)
=(SUMIF(Cleaned_Data!D2:D10001, "Resolved", Cleaned_Data!K2:K10001) + SUMIF(Cleaned_Data!D2:D10001, "Closed", Cleaned_Data!K2:K10001)) / D6

-- 11. Turnaround Buffer Hours (+5.56 hrs)
=D14 - B14

-- 12. Average Customer Satisfaction (3.97 / 5.0)
=AVERAGE(Cleaned_Data!N2:N10001)

-- 13. Reopened Tickets & Rate (511 / 5.37%)
=SUM(Cleaned_Data!O2:O10001)  |  =B18 / D6 [Denominator: Resolved Tickets]

-- 14. Escalated Tickets & Rate (1,123 / 11.23%)
=SUM(Cleaned_Data!P2:P10001)  |  =F18 / B6 [Denominator: Total Intake]
```

---

## 3. How to Build Native Dynamic PivotTables in Excel

If you wish to explore interactive slicing inside Microsoft Excel or Excel on the Web:

1. Click on the **`Cleaned_Data`** sheet.
2. Select any cell within the data range (e.g., `A1`).
3. Press `Ctrl + A` (or `Cmd + A` on Mac) to select all 10,000 rows.
4. Go to the top ribbon and select **Insert > PivotTable**.
5. Choose **New Worksheet** and click **OK**.
6. In the **PivotTable Fields** panel on the right:
   - **For Monthly Trend:** Drag `Created_Date` into **Rows**, and `Ticket_ID` into **Values** (summarized by `Count`).
   - **For SLA Performance by Team:** Drag `Support_Team` into **Rows**, `SLA_Status` into **Columns**, and `Ticket_ID` into **Values** (`Count`). Right-click the values and select **Show Values As > % of Row Total** to see compliance rates dynamically.
   - **For Backlog by Priority:** Drag `Status` to **Filters** (filter to `In Progress`, `Pending Customer`, `New`), drag `Support_Team` to **Rows**, and `Priority` to **Columns**.

---

## 4. Reconciled Metrics Summary

| Dimension | Total Tickets | Resolved | SLA Met | SLA Breached | Compliance % | Avg Res (hrs) | Avg CSAT |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Service Desk - Tier 1** | 3,920 | 3,700 | 3,184 | 516 | **86.05%** | 23.34 | 4.05 |
| **End User Support - Tier 2** | 1,543 | 1,475 | 1,241 | 234 | **84.14%** | 23.92 | 4.04 |
| **IAM** | 1,064 | 1,019 | 857 | 162 | **84.10%** | 24.14 | 4.07 |
| **Cloud & Systems Infra** | 1,828 | 1,745 | 1,411 | 334 | **80.86%** | 25.41 | 3.84 |
| **Network Operations** | 1,645 | 1,575 | 1,138 | 437 | **72.25%** | 28.61 | 3.82 |
| **Company Total** | **10,000** | **9,514** | **7,831** | **1,683** | **82.31%** | **24.77** | **3.97** |
