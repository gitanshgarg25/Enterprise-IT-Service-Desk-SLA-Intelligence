"""
IT Service Desk Dataset Generator
Generates realistic, industry-style IT support ticket data for analytics.
Deterministic seed: 42
Outputs: data/raw/itsm_tickets_raw.csv (approx 10,025 rows including realistic raw anomalies)
"""

import os
import random
import csv
from datetime import datetime, timedelta

def generate_raw_tickets():
    random.seed(42)

    # Output path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    raw_file = os.path.join(raw_dir, "itsm_tickets_raw.csv")

    # Timeframe: 1 Full Year (2025-10-01 to 2026-09-30)
    start_date = datetime(2025, 10, 1, 0, 0, 0)
    end_date = datetime(2026, 9, 30, 23, 59, 59)
    total_seconds = int((end_date - start_date).total_seconds())

    # Master metadata
    priorities = {
        "Critical": {"weight": 0.08, "sla_hours": 4.0},
        "High": {"weight": 0.22, "sla_hours": 8.0},
        "Medium": {"weight": 0.48, "sla_hours": 24.0},
        "Low": {"weight": 0.22, "sla_hours": 72.0}
    }

    categories = {
        "Access & Identity": {
            "subcategories": ["Password Reset", "MFA Authentication", "Role-Based Permissions", "Account Unlock"],
            "primary_team": "Identity & Access Management (IAM)",
            "tier1_share": 0.45
        },
        "Software & Applications": {
            "subcategories": ["Enterprise ERP", "Office 365 & Email", "VPN & Remote Access", "Specialized Dev Tools"],
            "primary_team": "Service Desk - Tier 1",
            "tier1_share": 0.70
        },
        "Hardware & Workstation": {
            "subcategories": ["Laptop Freeze & OS", "Peripheral Malfunction", "Monitor & Docking Station", "Asset Replacement"],
            "primary_team": "End User Support - Tier 2",
            "tier1_share": 0.20
        },
        "Network & Connectivity": {
            "subcategories": ["Office Wi-Fi Access", "LAN Cable & Port", "Bandwidth & Latency", "DNS & Gateway Routing"],
            "primary_team": "Network Operations",
            "tier1_share": 0.15
        },
        "Cloud & Infrastructure": {
            "subcategories": ["Server Provisioning", "Cloud Storage Permissions", "Database Connectivity", "Virtual Machine Crash"],
            "primary_team": "Cloud & Systems Infrastructure",
            "tier1_share": 0.10
        }
    }

    team_agents = {
        "Service Desk - Tier 1": ["Alex Chen", "Priya Sharma", "David Kim", "Emma Watson", "Carlos Mendez"],
        "End User Support - Tier 2": ["Frank Miller", "Grace Hopper", "Hannah Abbott", "Ian Wright"],
        "Identity & Access Management (IAM)": ["Maya Patel", "Noah Smith", "Olivia Brown"],
        "Network Operations": ["Jack Reynolds", "Karen Vance", "Leo Tanaka"],
        "Cloud & Systems Infrastructure": ["Paul Robinson", "Quinn Hughes", "Rachel Green"]
    }

    departments = [
        ("Software Engineering", 0.35),
        ("Sales & Marketing", 0.20),
        ("Finance & Accounting", 0.15),
        ("Customer Operations", 0.15),
        ("Human Resources", 0.10),
        ("Legal & Compliance", 0.05)
    ]
    dept_names = [d[0] for d in departments]
    dept_weights = [d[1] for d in departments]

    records = []
    num_tickets = 10000

    for i in range(1, num_tickets + 1):
        ticket_id = f"TCK-{10000 + i}"

        # Created timestamp with realistic time weighting
        random_offset = random.randint(0, total_seconds)
        created_dt = start_date + timedelta(seconds=random_offset)

        # Skew towards business hours (8am - 6pm) and weekdays (Mon-Fri)
        is_weekend = created_dt.weekday() >= 5
        if is_weekend and random.random() < 0.7:
            # Shift some weekend tickets to weekday
            created_dt -= timedelta(days=created_dt.weekday() - 4)

        hour = created_dt.hour
        if (hour < 8 or hour > 18) and random.random() < 0.65:
            # Shift towards business hours
            created_dt = created_dt.replace(hour=random.randint(8, 17), minute=random.randint(0, 59))

        # Select Priority
        p_rand = random.random()
        if p_rand < 0.08:
            priority = "Critical"
        elif p_rand < 0.30:
            priority = "High"
        elif p_rand < 0.78:
            priority = "Medium"
        else:
            priority = "Low"

        sla_target = priorities[priority]["sla_hours"]

        # Select Category & Subcategory
        cat_name = random.choice(list(categories.keys()))
        cat_info = categories[cat_name]
        subcat = random.choice(cat_info["subcategories"])

        # Determine Support Team
        if random.random() < cat_info["tier1_share"]:
            team = "Service Desk - Tier 1"
        else:
            team = cat_info["primary_team"]

        agent = random.choice(team_agents[team])
        department = random.choices(dept_names, weights=dept_weights, k=1)[0]

        # Escalation and Reopen chances
        # Critical and Cloud/Network issues have slightly higher escalation rates
        esc_prob = 0.07
        if priority in ["Critical", "High"]:
            esc_prob += 0.08
        if cat_name in ["Cloud & Infrastructure", "Network & Connectivity"]:
            esc_prob += 0.05
        is_escalated = 1 if random.random() < esc_prob else 0

        # Open vs Resolved Status determination
        # Tickets created in the last 14 days of the year (late Sep 2026) have higher chance of being open
        days_from_end = (end_date - created_dt).total_seconds() / 86400.0

        if days_from_end <= 3:
            status_weights = [0.15, 0.05, 0.50, 0.20, 0.10] # Resolved, Closed, In Progress, Pending Customer, New
        elif days_from_end <= 10:
            status_weights = [0.55, 0.15, 0.20, 0.07, 0.03]
        else:
            status_weights = [0.82, 0.14, 0.025, 0.01, 0.005]

        status = random.choices(
            ["Resolved", "Closed", "In Progress", "Pending Customer", "New"],
            weights=status_weights,
            k=1
        )[0]

        # Resolution calculations
        is_resolved = status in ["Resolved", "Closed"]

        if is_resolved:
            is_reopened = 1 if random.random() < 0.055 else 0

            # Resolution duration logic:
            # Base compliance rate ~ 78-85%, lower for escalated or complex categories
            breach_prob = 0.16
            if is_escalated:
                breach_prob += 0.18
            if team == "Network Operations":
                breach_prob += 0.08
            elif team == "Service Desk - Tier 1":
                breach_prob -= 0.04

            is_breached = random.random() < breach_prob

            if not is_breached:
                # Met SLA: duration is between 15% and 95% of SLA target
                duration_hours = round(random.uniform(0.2, 0.95) * sla_target, 2)
            else:
                # Breached SLA: duration exceeds SLA target (105% to 250%)
                duration_hours = round(random.uniform(1.05, 2.8) * sla_target, 2)

            # Ensure duration does not exceed snapshot date
            resolved_dt = created_dt + timedelta(hours=duration_hours)
            if resolved_dt > end_date:
                # Cap to end_date minus few minutes if needed
                resolved_dt = end_date - timedelta(minutes=random.randint(5, 120))
                duration_hours = round((resolved_dt - created_dt).total_seconds() / 3600.0, 2)

            resolved_date_str = resolved_dt.strftime("%Y-%m-%d %H:%M:%S")
            actual_res_hours_str = f"{duration_hours:.2f}"

            # Customer Satisfaction Score (CSAT: 1 to 5)
            # About 35% survey non-response rate
            if random.random() < 0.35:
                csat_score = ""
            else:
                if not is_breached and not is_escalated and not is_reopened:
                    csat = random.choices([5, 4, 3, 2, 1], weights=[0.60, 0.30, 0.07, 0.02, 0.01], k=1)[0]
                elif is_breached or is_escalated:
                    csat = random.choices([5, 4, 3, 2, 1], weights=[0.08, 0.18, 0.28, 0.28, 0.18], k=1)[0]
                else:
                    csat = random.choices([5, 4, 3, 2, 1], weights=[0.20, 0.35, 0.25, 0.12, 0.08], k=1)[0]
                csat_score = str(csat)

        else:
            # Open tickets
            resolved_date_str = ""
            actual_res_hours_str = ""
            csat_score = ""
            is_reopened = 0

        record = {
            "Ticket_ID": ticket_id,
            "Created_Date": created_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "Resolved_Date": resolved_date_str,
            "Status": status,
            "Priority": priority,
            "Category": cat_name,
            "Subcategory": subcat,
            "Support_Team": team,
            "Assigned_Agent": agent,
            "Department": department,
            "SLA_Target_Hours": f"{sla_target:.1f}",
            "Actual_Resolution_Hours": actual_res_hours_str,
            "Customer_Satisfaction_Score": csat_score,
            "Reopened_Flag": is_reopened,
            "Escalated_Flag": is_escalated
        }
        records.append(record)

    # Add 25 intentional raw anomalies to simulate authentic operational ITSM logging:
    # 1. 5 duplicate records
    for d_idx in [150, 1200, 3400, 6800, 9100]:
        dup = dict(records[d_idx])
        records.append(dup)

    # 2. 5 records with trailing/leading whitespace in text fields
    records[45]["Category"] = "Hardware & Workstation  "
    records[312]["Priority"] = " High"
    records[789]["Department"] = " Software Engineering "
    records[1540]["Support_Team"] = "Network Operations "
    records[2400]["Status"] = "Resolved "

    # 3. 3 test rows logged by QA engineers
    test_record_1 = dict(records[10])
    test_record_1["Ticket_ID"] = "TEST-9901"
    test_record_1["Category"] = "TEST_CATEGORY"
    test_record_1["Department"] = "QA_TEST"
    records.append(test_record_1)

    test_record_2 = dict(records[20])
    test_record_2["Ticket_ID"] = "TEST-9902"
    test_record_2["Category"] = "QA_AUTOMATION"
    records.append(test_record_2)

    test_record_3 = dict(records[30])
    test_record_3["Ticket_ID"] = "DEV-SMOKE-01"
    test_record_3["Priority"] = "P1_URGENT_TEST"
    records.append(test_record_3)

    # 4. 4 records with inconsistent lowercase casing
    records[520]["Category"] = "software & applications"
    records[1150]["Priority"] = "low"
    records[2340]["Priority"] = "medium"
    records[3800]["Category"] = "cloud & infrastructure"

    # 5. 3 records with uppercase status
    records[4500]["Status"] = "RESOLVED"
    records[6200]["Status"] = "CLOSED"
    records[7800]["Status"] = "IN PROGRESS"

    # 6. 5 records with minor casing differences in Support Team
    records[8200]["Support_Team"] = "service desk - tier 1"
    records[8500]["Support_Team"] = "network operations"

    # Write raw CSV
    fieldnames = [
        "Ticket_ID", "Created_Date", "Resolved_Date", "Status", "Priority",
        "Category", "Subcategory", "Support_Team", "Assigned_Agent", "Department",
        "SLA_Target_Hours", "Actual_Resolution_Hours", "Customer_Satisfaction_Score",
        "Reopened_Flag", "Escalated_Flag"
    ]

    with open(raw_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Successfully generated {len(records)} raw ticket records at {raw_file}")

if __name__ == "__main__":
    generate_raw_tickets()
