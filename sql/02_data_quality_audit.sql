-- ============================================================================
-- Script 02: Data Quality & Integrity Audit Queries
-- Project: Enterprise IT Service Desk & SLA Intelligence Platform
-- Description: Validates dataset integrity within SQL engine after import.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Check 1: Record Counts Across Fact and Dimension Tables
-- Expected: fact_tickets = 10,000; dim_priority_sla = 4; dim_support_team = 5
-- ----------------------------------------------------------------------------
SELECT 'fact_tickets' AS Table_Name, COUNT(*) AS Total_Records FROM fact_tickets
UNION ALL
SELECT 'dim_priority_sla', COUNT(*) FROM dim_priority_sla
UNION ALL
SELECT 'dim_support_team', COUNT(*) FROM dim_support_team;

-- ----------------------------------------------------------------------------
-- Check 2: Uniqueness of Primary Key (Ticket_ID)
-- Expected: 0 duplicate IDs
-- ----------------------------------------------------------------------------
SELECT 
    Ticket_ID, 
    COUNT(*) AS Occurrence_Count
FROM fact_tickets
GROUP BY Ticket_ID
HAVING COUNT(*) > 1;

-- ----------------------------------------------------------------------------
-- Check 3: Date and Status Integrity Verification
-- Rule A: Resolved/Closed tickets must have Resolved_Date and Actual_Resolution_Hours > 0
-- Rule B: Open tickets must have NULL Resolved_Date and NULL Actual_Resolution_Hours
-- Expected: 0 violating records for both checks
-- ----------------------------------------------------------------------------
SELECT 
    'Resolved Tickets Missing Dates' AS Issue_Type,
    COUNT(*) AS Violation_Count
FROM fact_tickets
WHERE Status IN ('Resolved', 'Closed')
  AND (Resolved_Date IS NULL OR Actual_Resolution_Hours IS NULL OR Actual_Resolution_Hours <= 0)

UNION ALL

SELECT 
    'Open Tickets With Premature Dates' AS Issue_Type,
    COUNT(*) AS Violation_Count
FROM fact_tickets
WHERE Status NOT IN ('Resolved', 'Closed')
  AND (Resolved_Date IS NOT NULL AND Resolved_Date != '' OR Actual_Resolution_Hours IS NOT NULL);

-- ----------------------------------------------------------------------------
-- Check 4: SLA Target Integrity vs Dimension
-- Expected: 0 discrepancies
-- ----------------------------------------------------------------------------
SELECT 
    f.Ticket_ID,
    f.Priority,
    f.SLA_Target_Hours AS Fact_SLA,
    d.SLA_Target_Hours AS Dim_SLA
FROM fact_tickets f
JOIN dim_priority_sla d ON f.Priority = d.Priority
WHERE ABS(f.SLA_Target_Hours - d.SLA_Target_Hours) > 0.01;

-- ----------------------------------------------------------------------------
-- Check 5: Orphan Records (Referential Integrity Check)
-- Expected: 0 unmapped priorities or unmapped support teams
-- ----------------------------------------------------------------------------
SELECT 
    'Unmapped Priority' AS Issue_Type,
    COUNT(*) AS Violation_Count
FROM fact_tickets f
LEFT JOIN dim_priority_sla d ON f.Priority = d.Priority
WHERE d.Priority IS NULL

UNION ALL

SELECT 
    'Unmapped Support Team' AS Issue_Type,
    COUNT(*) AS Violation_Count
FROM fact_tickets f
LEFT JOIN dim_support_team t ON f.Support_Team = t.Support_Team
WHERE t.Support_Team IS NULL;
