# ITSM Data Quality & Validation Audit Report

## 1. Executive Summary
- **Raw Ingested Records:** 10,008
- **Duplicate Rows Removed:** 5 (exact duplicate records from simulated webhook retries)
- **Non-Production Test Records Removed:** 3 (`TEST-9901`, `TEST-9902`, `DEV-SMOKE-01`)
- **Total Excluded Anomaly Records:** 8
- **Validated Production Records:** 10,000
- **Data Completeness & Integrity Score:** 100.0%

## 2. Data Cleaning Rules & Actions Log

| Rule Category | Verification Check | Anomalies Detected | Remediation Action |
| :--- | :--- | :--- | :--- |
| **1. Uniqueness** | Duplicate `Ticket_ID` | 5 duplicate IDs | Deduplicated exact row copies, keeping primary occurrence. |
| **2. Test Data Filter** | Non-production tickets (`TEST-`, `DEV-`) | 3 test rows | Removed QA smoke-test rows from production analysis. |
| **3. String Hygiene** | Leading/trailing whitespace | 5 records | Trimmed whitespace across all categorical and text fields. |
| **4. Casing Standardization** | Inconsistent casing in Priority/Team/Category | 9 records | Normalized to standardized Title Case. |
| **5. SLA Target Integrity** | `SLA_Target_Hours` vs Priority mapping | 1 record | Aligned target hours to strict SLA matrix (4h, 8h, 24h, 72h). |
| **6. Date Logic** | Non-positive resolution duration (`diff <= 0`) | 0 records | Verified resolution date is strictly after creation date. |
| **7. Status Consistency (Resolved)** | Resolved tickets missing resolution date | 0 records | Verified all resolved/closed tickets have valid dates and actual hours. |
| **8. Status Consistency (Open)** | Open tickets with premature resolution values | 1 record | Enforced NULL for dates/actual hours on active open tickets. |

## 3. Production Dataset Schema

| Column Name | Data Type | Description | Constraint / Allowed Values |
| :--- | :--- | :--- | :--- |
| `Ticket_ID` | VARCHAR(16) | Unique ticket identifier | Primary Key (`TCK-10001` - `TCK-20000`) |
| `Created_Date` | DATETIME | Ticket creation timestamp | YYYY-MM-DD HH:MM:SS (2025-10-01 to 2026-09-30) |
| `Resolved_Date` | DATETIME | Ticket resolution timestamp | NULL for open tickets; >= Created_Date for resolved |
| `Status` | VARCHAR(20) | Operational lifecycle state | `Resolved`, `Closed`, `In Progress`, `Pending Customer`, `New` |
| `Priority` | VARCHAR(10) | Incident business urgency | `Critical`, `High`, `Medium`, `Low` |
| `Category` | VARCHAR(35) | Functional issue category | 5 standard IT domains |
| `Subcategory` | VARCHAR(35) | Detailed issue classification | 20 distinct subcategories |
| `Support_Team` | VARCHAR(40) | Resolving assignment group | 5 IT support teams |
| `Assigned_Agent` | VARCHAR(30) | Assigned IT support specialist | 20 named agents across teams |
| `Department` | VARCHAR(30) | Requester department | 6 business units |
| `SLA_Target_Hours` | DECIMAL(4,1) | SLA threshold in calendar hours | 4.0, 8.0, 24.0, 72.0 |
| `Actual_Resolution_Hours` | DECIMAL(6,2) | Actual turnaround in calendar hours | NULL for open; > 0 for resolved |
| `SLA_Status` | VARCHAR(25) | Compliance outcome | `Met`, `Breached`, `Open - In Evaluation` |
| `Customer_Satisfaction_Score` | INTEGER | Post-resolution survey (1 to 5) | NULL if unresponded or open |
| `Reopened_Flag` | INTEGER | Indicator if ticket was reopened | 0 = No, 1 = Yes (Resolved only) |
| `Escalated_Flag` | INTEGER | Indicator if ticket was escalated | 0 = No, 1 = Yes |

## 4. Reconciled Baseline Metrics & Denominators

| Metric | Count / Value | Calculation Denominator | Notes |
| :--- | :--- | :--- | :--- |
| **Total Ingested Tickets** | 10,000 | 10,000 (Total Volume) | Cleaned production intake |
| **Resolved / Closed Tickets** | 9,514 (95.14%) | 10,000 (Total Volume) | Operationally completed tickets |
| **Active Open Tickets** | 486 (4.86%) | 10,000 (Total Volume) | In Progress, Pending Customer, New |
| **SLA Eligible Tickets** | 9,514 | 9,514 (Resolved Tickets) | Only completed tickets evaluated for final SLA |
| **SLA Met Tickets** | 7,831 (82.31%) | 9,514 (Resolved Tickets) | `Actual_Resolution_Hours <= SLA_Target_Hours` |
| **SLA Breached Tickets** | 1,683 (17.69%) | 9,514 (Resolved Tickets) | `Actual_Resolution_Hours > SLA_Target_Hours` |
| **Average Actual Resolution Time**| 24.77 hours | 9,514 (Resolved Tickets) | Turnaround duration |
| **Average SLA Target Time** | 30.33 hours | 9,514 (Resolved Tickets) | Committed baseline SLA |
| **Average CSAT Score** | 3.97 / 5.0 | 6,053 (Survey Respondents) | 63.62% response rate among resolved tickets |
| **Reopened Tickets** | 511 (5.37%) | 9,514 (Resolved Tickets) | 5.11% if evaluated over total 10,000 intake |
| **Escalated Tickets** | 1,123 (11.23%) | 10,000 (Total Volume) | Incidents escalated across operational lifecycle |
