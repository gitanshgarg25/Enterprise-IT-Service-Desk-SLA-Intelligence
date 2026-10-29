"""
Database Setup and SQL Analysis Runner
Creates the SQLite database, imports clean tables, runs all analytical queries,
and exports full query outputs to documentation/sql_analysis_results.md.
"""

import sqlite3
import csv
import os

def setup_and_run_sql():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "itsm_service_desk.db")
    sql_dir = os.path.join(base_dir, "sql")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    results_path = os.path.join(base_dir, "documentation", "sql_analysis_results.md")

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Execute Schema Script
    with open(os.path.join(sql_dir, "01_schema_and_import.sql"), "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    print("Schema created successfully in itsm_service_desk.db.")

    # 2. Insert Data from CSVs
    # Priority Dimension
    with open(os.path.join(cleaned_dir, "dim_priority_sla.csv"), "r", encoding="utf-8") as f:
        p_rows = list(csv.reader(f))[1:]
        cursor.executemany("INSERT INTO dim_priority_sla VALUES (?, ?, ?, ?)", p_rows)

    # Support Team Dimension
    with open(os.path.join(cleaned_dir, "dim_support_team.csv"), "r", encoding="utf-8") as f:
        t_rows = list(csv.reader(f))[1:]
        cursor.executemany("INSERT INTO dim_support_team VALUES (?, ?, ?)", t_rows)

    # Fact Tickets
    with open(os.path.join(cleaned_dir, "itsm_tickets_cleaned.csv"), "r", encoding="utf-8") as f:
        f_reader = csv.DictReader(f)
        f_data = []
        for r in f_reader:
            f_data.append((
                r["Ticket_ID"],
                r["Created_Date"],
                r["Resolved_Date"] if r["Resolved_Date"] else None,
                r["Status"],
                r["Priority"],
                r["Category"],
                r["Subcategory"],
                r["Support_Team"],
                r["Assigned_Agent"],
                r["Department"],
                float(r["SLA_Target_Hours"]),
                float(r["Actual_Resolution_Hours"]) if r["Actual_Resolution_Hours"] else None,
                r["SLA_Status"],
                int(r["Customer_Satisfaction_Score"]) if r["Customer_Satisfaction_Score"] else None,
                int(r["Reopened_Flag"]),
                int(r["Escalated_Flag"])
            ))
        cursor.executemany("""
            INSERT INTO fact_tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, f_data)

    conn.commit()
    print(f"Imported {len(f_data)} tickets, {len(p_rows)} priority rows, {len(t_rows)} team rows.")

    # 3. Helper to format queries as markdown tables
    def execute_and_format(query_name, query_text):
        cursor.execute(query_text)
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        md = f"### {query_name}\n\n"
        md += "| " + " | ".join(cols) + " |\n"
        md += "| " + " | ".join([":---" for _ in cols]) + " |\n"
        for r in rows:
            formatted_cells = []
            for cell in r:
                if cell is None:
                    formatted_cells.append("NULL")
                elif isinstance(cell, float):
                    formatted_cells.append(f"{cell:.2f}")
                else:
                    formatted_cells.append(str(cell))
            md += "| " + " | ".join(formatted_cells) + " |\n"
        md += f"\n*Total rows returned: {len(rows)}*\n\n"
        return md

    # Run and log all analytical queries
    with open(results_path, "w", encoding="utf-8") as out:
        out.write("# SQL Analytics & Query Results Documentation\n\n")
        out.write("This document contains the verified query results executed directly against `data/itsm_service_desk.db` in SQLite.\n\n")

        out.write("## Section 1: In-Engine Data Quality & Referential Integrity\n\n")
        
        q_count = """
        SELECT 'fact_tickets' AS Table_Name, COUNT(*) AS Total_Records FROM fact_tickets
        UNION ALL
        SELECT 'dim_priority_sla', COUNT(*) FROM dim_priority_sla
        UNION ALL
        SELECT 'dim_support_team', COUNT(*) FROM dim_support_team;
        """
        out.write(execute_and_format("Check 1: Row Counts Across Tables", q_count))

        q_integrity = """
        SELECT 
            'Resolved Missing Dates' AS Issue_Type,
            COUNT(*) AS Violation_Count
        FROM fact_tickets
        WHERE Status IN ('Resolved', 'Closed')
          AND (Resolved_Date IS NULL OR Actual_Resolution_Hours IS NULL OR Actual_Resolution_Hours <= 0)
        UNION ALL
        SELECT 
            'Open With Premature Dates' AS Issue_Type,
            COUNT(*) AS Violation_Count
        FROM fact_tickets
        WHERE Status NOT IN ('Resolved', 'Closed')
          AND (Resolved_Date IS NOT NULL AND Resolved_Date != '' OR Actual_Resolution_Hours IS NOT NULL);
        """
        out.write(execute_and_format("Check 2: Status & Date Integrity Check", q_integrity))

        out.write("## Section 2: Core Operational & KPI Queries\n\n")

        q3 = """
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
        """
        out.write(execute_and_format("Query 3: Monthly Ticket Volume & MoM Growth", q3))

        q4 = """
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
        """
        out.write(execute_and_format("Query 4: Ticket Volume by Category & Priority Breakdown", q4))

        q5 = """
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
        """
        out.write(execute_and_format("Query 5: SLA Compliance and Breach Rates by Priority", q5))

        q6 = """
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
        """
        out.write(execute_and_format("Query 6: Resolution Time & SLA Buffer by Support Team", q6))

        q7 = """
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
        """
        out.write(execute_and_format("Query 7: Active Open Backlog by Team and Priority", q7))

        q8 = """
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
        """
        out.write(execute_and_format("Query 8: Reopened & Escalated Incidents by Team", q8))

        q9 = """
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
        """
        out.write(execute_and_format("Query 9: CSAT vs SLA Outcome Correlation", q9))

        out.write("## Section 3: Advanced Business-Focused Queries\n\n")

        q10_1 = """
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
        """
        out.write(execute_and_format("Business Query 1: Top 10 Root-Cause SLA Breach Bottlenecks", q10_1))

        q10_2 = """
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
        """
        out.write(execute_and_format("Business Query 2: Agent Scorecard & Team-Relative Ranking", q10_2))

        q10_3 = """
        WITH Active_Queue AS (
            SELECT 
                Ticket_ID,
                Created_Date,
                Priority,
                Category,
                Support_Team,
                SLA_Target_Hours,
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
        """
        out.write(execute_and_format("Business Query 3: Active Backlog Aging & Critical Exposure Matrix", q10_3))

    conn.close()
    print(f"All queries executed successfully. Results written to {results_path}")

if __name__ == "__main__":
    setup_and_run_sql()
