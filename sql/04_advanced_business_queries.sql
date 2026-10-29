-- ============================================================================
-- Script 04: Advanced Business-Focused Analytical Queries
-- Project: Enterprise IT Service Desk & SLA Intelligence Platform
-- Description: Advanced SQL employing CTEs, Window Functions, Multi-table Joins,
--              and Conditional Aggregations to solve core management questions.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Business Query 1: Root-Cause Bottleneck Ranking (Category & Subcategory)
-- Business Question: "Which specific technical domains and subcategories drive the
--                     highest volume of SLA breaches, and what is their CSAT impact?"
-- Techniques: CTE, Window Ranking (DENSE_RANK), Conditional Aggregation, Running Share
-- ----------------------------------------------------------------------------
WITH Subcategory_Performance AS (
    SELECT 
        Category,
        Subcategory,
        COUNT(*) AS Total_Resolved,
        SUM(CASE WHEN SLA_Status = 'Breached' THEN 1 ELSE 0 END) AS Breached_Tickets,
        ROUND(
            SUM(CASE WHEN SLA_Status = 'Breached' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 
            2
        ) AS Subcategory_Breach_Rate_Pct,
        ROUND(AVG(Actual_Resolution_Hours), 2) AS Avg_Actual_Hours,
        ROUND(AVG(Customer_Satisfaction_Score), 2) AS Avg_CSAT_Score
    FROM fact_tickets
    WHERE Status IN ('Resolved', 'Closed')
    GROUP BY Category, Subcategory
)
SELECT 
    DENSE_RANK() OVER (ORDER BY Breached_Tickets DESC) AS Breach_Impact_Rank,
    Category,
    Subcategory,
    Total_Resolved,
    Breached_Tickets,
    ROUND(Breached_Tickets * 100.0 / (SELECT COUNT(*) FROM fact_tickets WHERE SLA_Status = 'Breached'), 2) AS Pct_Of_All_Breaches,
    Subcategory_Breach_Rate_Pct,
    Avg_Actual_Hours,
    Avg_CSAT_Score
FROM Subcategory_Performance
ORDER BY Breached_Tickets DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Business Query 2: Support Agent Efficiency Scorecard & Tier Ranking
-- Business Question: "How do individual agents perform within their respective teams
--                     on resolution volume, SLA compliance %, and user satisfaction?"
-- Techniques: Multi-table JOIN, CTE, Window Partitioning (RANK() OVER PARTITION BY)
-- ----------------------------------------------------------------------------
WITH Agent_Metrics AS (
    SELECT 
        t.Support_Team,
        t.Support_Tier,
        f.Assigned_Agent,
        COUNT(f.Ticket_ID) AS Total_Assigned,
        SUM(CASE WHEN f.Status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS Resolved_Count,
        SUM(CASE WHEN f.SLA_Status = 'Met' THEN 1 ELSE 0 END) AS SLA_Met_Count,
        ROUND(
            SUM(CASE WHEN f.SLA_Status = 'Met' THEN 1.0 ELSE 0.0 END) / 
            NULLIF(SUM(CASE WHEN f.Status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END), 0) * 100.0, 
            2
        ) AS Agent_Compliance_Rate_Pct,
        ROUND(AVG(f.Actual_Resolution_Hours), 2) AS Avg_Resolution_Hours,
        ROUND(AVG(f.Customer_Satisfaction_Score), 2) AS Avg_Agent_CSAT
    FROM fact_tickets f
    JOIN dim_support_team t ON f.Support_Team = t.Support_Team
    GROUP BY t.Support_Team, t.Support_Tier, f.Assigned_Agent
)
SELECT 
    Support_Team,
    Support_Tier,
    Assigned_Agent,
    Total_Assigned,
    Resolved_Count,
    Agent_Compliance_Rate_Pct,
    Avg_Resolution_Hours,
    Avg_Agent_CSAT,
    RANK() OVER (
        PARTITION BY Support_Team 
        ORDER BY Agent_Compliance_Rate_Pct DESC, Resolved_Count DESC
    ) AS Team_Internal_Rank
FROM Agent_Metrics
ORDER BY Support_Team, Team_Internal_Rank;

-- ----------------------------------------------------------------------------
-- Business Query 3: Active Backlog Aging & SLA Exposure Matrix
-- Business Question: "As of the fiscal year-end snapshot (2026-10-01), which active
--                     tickets are already overdue, and where is the immediate risk?"
-- Techniques: Date Arithmetic (julianday), CASE Binning, Subqueries, Exposure Flagging
-- ----------------------------------------------------------------------------
WITH Active_Queue AS (
    SELECT 
        Ticket_ID,
        Created_Date,
        Priority,
        Category,
        Support_Team,
        SLA_Target_Hours,
        -- Calculate current age in calendar hours from snapshot point
        ROUND((julianday('2026-10-01 00:00:00') - julianday(Created_Date)) * 24.0, 2) AS Current_Age_Hours
    FROM fact_tickets
    WHERE Status NOT IN ('Resolved', 'Closed')
),
Categorized_Queue AS (
    SELECT 
        *,
        CASE 
            WHEN Current_Age_Hours > SLA_Target_Hours THEN 'Overdue (Breached)'
            ELSE 'Within Target'
        END AS SLA_Exposure_Status,
        CASE 
            WHEN Current_Age_Hours < 12.0 THEN '1. Under 12 Hours'
            WHEN Current_Age_Hours < 24.0 THEN '2. 12 to 24 Hours'
            WHEN Current_Age_Hours < 48.0 THEN '3. 24 to 48 Hours'
            ELSE '4. Over 48 Hours'
        END AS Aging_Bucket
    FROM Active_Queue
)
SELECT 
    Support_Team,
    COUNT(*) AS Total_Open_Tickets,
    SUM(CASE WHEN SLA_Exposure_Status = 'Overdue (Breached)' THEN 1 ELSE 0 END) AS Currently_Overdue_Tickets,
    ROUND(
        SUM(CASE WHEN SLA_Exposure_Status = 'Overdue (Breached)' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100.0, 
        2
    ) AS Overdue_Risk_Pct,
    SUM(CASE WHEN Aging_Bucket = '1. Under 12 Hours' THEN 1 ELSE 0 END) AS Age_Under_12h,
    SUM(CASE WHEN Aging_Bucket = '2. 12 to 24 Hours' THEN 1 ELSE 0 END) AS Age_12_to_24h,
    SUM(CASE WHEN Aging_Bucket = '3. 24 to 48 Hours' THEN 1 ELSE 0 END) AS Age_24_to_48h,
    SUM(CASE WHEN Aging_Bucket = '4. Over 48 Hours' THEN 1 ELSE 0 END) AS Age_Over_48h
FROM Categorized_Queue
GROUP BY Support_Team
ORDER BY Currently_Overdue_Tickets DESC;
