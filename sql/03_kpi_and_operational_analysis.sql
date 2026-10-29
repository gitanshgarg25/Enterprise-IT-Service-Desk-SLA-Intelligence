-- ============================================================================
-- Script 03: Core KPI and Operational Analysis Queries
-- Project: Enterprise IT Service Desk & SLA Intelligence Platform
-- Description: Core queries covering ticket volume, SLA compliance, team workload,
--              open backlog, escalation/reopens, and CSAT performance.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 3: Monthly Ticket Ingestion Trend & Month-over-Month (MoM) Growth
-- Purpose: Analyzes ticket intake seasonality across the 12-month period.
-- Uses: strftime for date truncation, LAG() window function for MoM variance.
-- ----------------------------------------------------------------------------
WITH Monthly_Intake AS (
    SELECT 
        strftime('%Y-%m', Created_Date) AS Year_Month,
        COUNT(*) AS Total_Tickets
    FROM fact_tickets
    GROUP BY strftime('%Y-%m', Created_Date)
)
SELECT 
    Year_Month,
    Total_Tickets,
    LAG(Total_Tickets, 1) OVER (ORDER BY Year_Month) AS Previous_Month_Tickets,
    ROUND(
        (CAST(Total_Tickets AS REAL) - LAG(Total_Tickets, 1) OVER (ORDER BY Year_Month)) 
        / LAG(Total_Tickets, 1) OVER (ORDER BY Year_Month) * 100.0, 
        2
    ) AS MoM_Growth_Pct
FROM Monthly_Intake
ORDER BY Year_Month;

-- ----------------------------------------------------------------------------
-- Query 4: Ticket Volume Distribution by Priority and Category
-- Purpose: Evaluates incident distribution across functional domains and urgency.
-- Uses: GROUP BY, CASE statements, and percentage of total intake.
-- ----------------------------------------------------------------------------
SELECT 
    Category,
    COUNT(*) AS Total_Tickets,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_tickets), 2) AS Pct_Of_Total_Volume,
    SUM(CASE WHEN Priority = 'Critical' THEN 1 ELSE 0 END) AS Critical_P1_Count,
    SUM(CASE WHEN Priority = 'High' THEN 1 ELSE 0 END) AS High_P2_Count,
    SUM(CASE WHEN Priority = 'Medium' THEN 1 ELSE 0 END) AS Medium_P3_Count,
    SUM(CASE WHEN Priority = 'Low' THEN 1 ELSE 0 END) AS Low_P4_Count
FROM fact_tickets
GROUP BY Category
ORDER BY Total_Tickets DESC;

-- ----------------------------------------------------------------------------
-- Query 5: SLA Compliance and Breach Rates by Priority
-- Purpose: Measures contractual SLA compliance strictly on resolved tickets.
-- Denominator: Resolved & Closed tickets (9,514 eligible tickets).
-- ----------------------------------------------------------------------------
SELECT 
    Priority,
    SLA_Target_Hours,
    COUNT(*) AS Resolved_Tickets,
    SUM(CASE WHEN SLA_Status = 'Met' THEN 1 ELSE 0 END) AS SLA_Met_Count,
    SUM(CASE WHEN SLA_Status = 'Breached' THEN 1 ELSE 0 END) AS SLA_Breached_Count,
    ROUND(SUM(CASE WHEN SLA_Status = 'Met' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 2) AS Compliance_Rate_Pct,
    ROUND(SUM(CASE WHEN SLA_Status = 'Breached' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 2) AS Breach_Rate_Pct
FROM fact_tickets
WHERE Status IN ('Resolved', 'Closed')
GROUP BY Priority, SLA_Target_Hours
ORDER BY SLA_Target_Hours ASC;

-- ----------------------------------------------------------------------------
-- Query 6: Average Resolution Time and SLA Variance by Support Team
-- Purpose: Evaluates operational turnaround speed against SLA commitments.
-- Uses: JOIN with dim_support_team, AVG aggregation.
-- ----------------------------------------------------------------------------
SELECT 
    t.Support_Team,
    t.Support_Tier,
    COUNT(f.Ticket_ID) AS Resolved_Tickets,
    ROUND(AVG(f.Actual_Resolution_Hours), 2) AS Avg_Actual_Resolution_Hours,
    ROUND(AVG(f.SLA_Target_Hours), 2) AS Avg_SLA_Target_Hours,
    ROUND(AVG(f.SLA_Target_Hours) - AVG(f.Actual_Resolution_Hours), 2) AS Avg_Turnaround_Buffer_Hours
FROM fact_tickets f
JOIN dim_support_team t ON f.Support_Team = t.Support_Team
WHERE f.Status IN ('Resolved', 'Closed')
GROUP BY t.Support_Team, t.Support_Tier
ORDER BY Avg_Actual_Resolution_Hours DESC;

-- ----------------------------------------------------------------------------
-- Query 7: Active Open Backlog by Support Team and Urgency
-- Purpose: Highlights operational bottlenecks and active queue distribution.
-- Denominator: 486 Active Open Tickets (In Progress, Pending Customer, New).
-- ----------------------------------------------------------------------------
SELECT 
    Support_Team,
    COUNT(*) AS Total_Open_Backlog,
    SUM(CASE WHEN Priority = 'Critical' THEN 1 ELSE 0 END) AS Open_Critical_P1,
    SUM(CASE WHEN Priority = 'High' THEN 1 ELSE 0 END) AS Open_High_P2,
    SUM(CASE WHEN Priority = 'Medium' THEN 1 ELSE 0 END) AS Open_Medium_P3,
    SUM(CASE WHEN Priority = 'Low' THEN 1 ELSE 0 END) AS Open_Low_P4,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_tickets WHERE Status NOT IN ('Resolved', 'Closed')), 2) AS Pct_Of_Total_Backlog
FROM fact_tickets
WHERE Status NOT IN ('Resolved', 'Closed')
GROUP BY Support_Team
ORDER BY Total_Open_Backlog DESC;

-- ----------------------------------------------------------------------------
-- Query 8: Reopened and Escalated Ticket Analysis by Support Team
-- Purpose: Evaluates service quality friction (first-contact resolution vs churn).
-- Explicit Denominators:
--   - Reopened Rate %: Reopened / Resolved Tickets (ITIL standard)
--   - Escalation Rate %: Escalated / Total Intake Tickets
-- ----------------------------------------------------------------------------
SELECT 
    Support_Team,
    COUNT(*) AS Total_Tickets,
    SUM(CASE WHEN Status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS Resolved_Tickets,
    SUM(Reopened_Flag) AS Reopened_Count,
    ROUND(
        SUM(Reopened_Flag) * 100.0 / 
        NULLIF(SUM(CASE WHEN Status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END), 0), 
        2
    ) AS Reopened_Rate_Pct,
    SUM(Escalated_Flag) AS Escalated_Count,
    ROUND(SUM(Escalated_Flag) * 100.0 / COUNT(*), 2) AS Escalation_Rate_Pct
FROM fact_tickets
GROUP BY Support_Team
ORDER BY Reopened_Rate_Pct DESC;

-- ----------------------------------------------------------------------------
-- Query 9: Customer Satisfaction (CSAT) vs SLA Outcome Correlation
-- Purpose: Empirically proves that SLA breaches degrade customer experience.
-- Shows response count and average CSAT by SLA Status.
-- ----------------------------------------------------------------------------
SELECT 
    SLA_Status,
    COUNT(*) AS Total_Resolved_Tickets,
    COUNT(Customer_Satisfaction_Score) AS Survey_Responses,
    ROUND(COUNT(Customer_Satisfaction_Score) * 100.0 / COUNT(*), 2) AS Response_Rate_Pct,
    ROUND(AVG(Customer_Satisfaction_Score), 2) AS Avg_CSAT_Score,
    SUM(CASE WHEN Customer_Satisfaction_Score = 5 THEN 1 ELSE 0 END) AS Rating_5_Count,
    SUM(CASE WHEN Customer_Satisfaction_Score = 4 THEN 1 ELSE 0 END) AS Rating_4_Count,
    SUM(CASE WHEN Customer_Satisfaction_Score = 3 THEN 1 ELSE 0 END) AS Rating_3_Count,
    SUM(CASE WHEN Customer_Satisfaction_Score = 2 THEN 1 ELSE 0 END) AS Rating_2_Count,
    SUM(CASE WHEN Customer_Satisfaction_Score = 1 THEN 1 ELSE 0 END) AS Rating_1_Count
FROM fact_tickets
WHERE Status IN ('Resolved', 'Closed')
GROUP BY SLA_Status
ORDER BY Avg_CSAT_Score DESC;
