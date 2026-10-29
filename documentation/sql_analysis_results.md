# SQL Analytics & Query Results Documentation

This document contains the verified query results executed directly against `data/itsm_service_desk.db` in SQLite.

## Section 1: In-Engine Data Quality & Referential Integrity

### Check 1: Row Counts Across Tables

| Table_Name | Total_Records |
| :--- | :--- |
| fact_tickets | 10000 |
| dim_priority_sla | 4 |
| dim_support_team | 5 |

*Total rows returned: 3*

### Check 2: Status & Date Integrity Check

| Issue_Type | Violation_Count |
| :--- | :--- |
| Resolved Missing Dates | 0 |
| Open With Premature Dates | 0 |

*Total rows returned: 2*

## Section 2: Core Operational & KPI Queries

### Query 3: Monthly Ticket Volume & MoM Growth

| Year_Month | Total_Tickets | Previous_Month_Tickets | MoM_Growth_Pct |
| :--- | :--- | :--- | :--- |
| 2025-10 | 967 | NULL | NULL |
| 2025-11 | 782 | 967 | -19.13 |
| 2025-12 | 824 | 782 | 5.37 |
| 2026-01 | 817 | 824 | -0.85 |
| 2026-02 | 758 | 817 | -7.22 |
| 2026-03 | 841 | 758 | 10.95 |
| 2026-04 | 815 | 841 | -3.09 |
| 2026-05 | 887 | 815 | 8.83 |
| 2026-06 | 819 | 887 | -7.67 |
| 2026-07 | 826 | 819 | 0.85 |
| 2026-08 | 869 | 826 | 5.21 |
| 2026-09 | 795 | 869 | -8.52 |

*Total rows returned: 12*

### Query 4: Ticket Volume by Category & Priority Breakdown

| Category | Total_Tickets | Pct_Of_Total_Volume | Critical_P1_Count | High_P2_Count | Medium_P3_Count | Low_P4_Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Software & Applications | 2068 | 20.68 | 171 | 403 | 983 | 511 |
| Cloud & Infrastructure | 2036 | 20.36 | 178 | 412 | 947 | 499 |
| Access & Identity | 2029 | 20.29 | 179 | 405 | 989 | 456 |
| Network & Connectivity | 1957 | 19.57 | 155 | 395 | 968 | 439 |
| Hardware & Workstation | 1910 | 19.10 | 144 | 427 | 905 | 434 |

*Total rows returned: 5*

### Query 5: SLA Compliance and Breach Rates by Priority

| Priority | SLA_Target_Hours | Resolved_Tickets | SLA_Met_Count | SLA_Breached_Count | Compliance_Rate_Pct | Breach_Rate_Pct |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Critical | 4 | 786 | 637 | 149 | 81.04 | 18.96 |
| High | 8 | 1926 | 1594 | 332 | 82.76 | 17.24 |
| Medium | 24 | 4578 | 3788 | 790 | 82.74 | 17.26 |
| Low | 72 | 2224 | 1812 | 412 | 81.47 | 18.53 |

*Total rows returned: 4*

### Query 6: Resolution Time & SLA Buffer by Support Team

| Support_Team | Support_Tier | Resolved_Tickets | Avg_Actual_Resolution_Hours | Avg_SLA_Target_Hours | Avg_Turnaround_Buffer_Hours |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Network Operations | Tier 3 | 1575 | 28.61 | 30.16 | 1.55 |
| Cloud & Systems Infrastructure | Tier 3 | 1745 | 25.41 | 30.58 | 5.17 |
| Identity & Access Management (IAM) | Tier 2 | 1019 | 24.14 | 29.74 | 5.59 |
| End User Support - Tier 2 | Tier 2 | 1475 | 23.92 | 30.55 | 6.63 |
| Service Desk - Tier 1 | Tier 1 | 3700 | 23.34 | 30.36 | 7.01 |

*Total rows returned: 5*

### Query 7: Active Open Backlog by Team and Priority

| Support_Team | Total_Open_Backlog | Open_Critical_P1 | Open_High_P2 | Open_Medium_P3 | Open_Low_P4 | Pct_Of_Total_Backlog |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Service Desk - Tier 1 | 220 | 15 | 51 | 100 | 54 | 45.27 |
| Cloud & Systems Infrastructure | 83 | 11 | 14 | 34 | 24 | 17.08 |
| Network Operations | 70 | 5 | 14 | 35 | 16 | 14.40 |
| End User Support - Tier 2 | 68 | 7 | 20 | 31 | 10 | 13.99 |
| Identity & Access Management (IAM) | 45 | 3 | 17 | 14 | 11 | 9.26 |

*Total rows returned: 5*

### Query 8: Reopened & Escalated Incidents by Team

| Support_Team | Total_Tickets | Resolved_Tickets | Reopened_Count | Reopened_Rate_Pct | Escalated_Count | Escalation_Rate_Pct |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Service Desk - Tier 1 | 3920 | 3700 | 222 | 6.00 | 372 | 9.49 |
| Cloud & Systems Infrastructure | 1828 | 1745 | 94 | 5.39 | 281 | 15.37 |
| End User Support - Tier 2 | 1543 | 1475 | 74 | 5.02 | 134 | 8.68 |
| Network Operations | 1645 | 1575 | 75 | 4.76 | 242 | 14.71 |
| Identity & Access Management (IAM) | 1064 | 1019 | 46 | 4.51 | 94 | 8.83 |

*Total rows returned: 5*

### Query 9: CSAT vs SLA Outcome Correlation

| SLA_Status | Total_Resolved_Tickets | Survey_Responses | Response_Rate_Pct | Avg_CSAT_Score | Rating_5_Count | Rating_4_Count | Rating_3_Count | Rating_2_Count | Rating_1_Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Met | 7831 | 4987 | 63.68 | 4.25 | 2640 | 1486 | 477 | 251 | 133 |
| Breached | 1683 | 1066 | 63.34 | 2.65 | 75 | 178 | 318 | 291 | 204 |

*Total rows returned: 2*

## Section 3: Advanced Business-Focused Queries

### Business Query 1: Top 10 Root-Cause SLA Breach Bottlenecks

| Breach_Impact_Rank | Category | Subcategory | Total_Resolved | Breached_Tickets | Pct_Of_All_Breaches | Subcategory_Breach_Rate_Pct | Avg_Actual_Hours | Avg_CSAT_Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Network & Connectivity | Office Wi-Fi Access | 470 | 132 | 7.84 | 28.09 | 26.63 | 3.81 |
| 2 | Network & Connectivity | DNS & Gateway Routing | 465 | 126 | 7.49 | 27.10 | 30.20 | 3.79 |
| 3 | Network & Connectivity | Bandwidth & Latency | 460 | 106 | 6.30 | 23.04 | 25.65 | 3.86 |
| 4 | Network & Connectivity | LAN Cable & Port | 469 | 105 | 6.24 | 22.39 | 28.46 | 3.94 |
| 5 | Cloud & Infrastructure | Cloud Storage Permissions | 503 | 97 | 5.76 | 19.28 | 26.06 | 3.83 |
| 5 | Cloud & Infrastructure | Virtual Machine Crash | 480 | 97 | 5.76 | 20.21 | 24.78 | 3.93 |
| 6 | Cloud & Infrastructure | Server Provisioning | 480 | 90 | 5.35 | 18.75 | 24.46 | 3.76 |
| 7 | Cloud & Infrastructure | Database Connectivity | 475 | 83 | 4.93 | 17.47 | 26.78 | 3.95 |
| 8 | Hardware & Workstation | Laptop Freeze & OS | 449 | 80 | 4.75 | 17.82 | 23.54 | 4.12 |
| 8 | Hardware & Workstation | Peripheral Malfunction | 473 | 80 | 4.75 | 16.91 | 24.28 | 3.96 |

*Total rows returned: 10*

### Business Query 2: Agent Scorecard & Team-Relative Ranking

| Support_Team | Support_Tier | Assigned_Agent | Total_Assigned | Resolved_Count | Agent_Compliance_Rate_Pct | Avg_Resolution_Hours | Avg_Agent_CSAT | Team_Internal_Rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Cloud & Systems Infrastructure | Tier 3 | Quinn Hughes | 604 | 574 | 83.45 | 23.11 | 3.92 | 1 |
| Cloud & Systems Infrastructure | Tier 3 | Rachel Green | 608 | 579 | 79.97 | 25.78 | 3.87 | 2 |
| Cloud & Systems Infrastructure | Tier 3 | Paul Robinson | 616 | 592 | 79.39 | 27.30 | 3.75 | 3 |
| End User Support - Tier 2 | Tier 2 | Grace Hopper | 389 | 374 | 85.29 | 24.08 | 4.06 | 1 |
| End User Support - Tier 2 | Tier 2 | Frank Miller | 367 | 352 | 84.66 | 24.52 | 3.98 | 2 |
| End User Support - Tier 2 | Tier 2 | Hannah Abbott | 394 | 373 | 84.45 | 23.13 | 4.14 | 3 |
| End User Support - Tier 2 | Tier 2 | Ian Wright | 393 | 376 | 82.45 | 23.97 | 3.99 | 4 |
| Identity & Access Management (IAM) | Tier 2 | Noah Smith | 330 | 320 | 85.63 | 23.88 | 4.07 | 1 |
| Identity & Access Management (IAM) | Tier 2 | Maya Patel | 380 | 365 | 84.38 | 22.95 | 4.10 | 2 |
| Identity & Access Management (IAM) | Tier 2 | Olivia Brown | 354 | 334 | 82.34 | 25.70 | 4.05 | 3 |
| Network Operations | Tier 3 | Emma Watson | 1 | 1 | 100.00 | 3.23 | 5.00 | 1 |
| Network Operations | Tier 3 | Priya Sharma | 1 | 1 | 100.00 | 68.32 | 4.00 | 1 |
| Network Operations | Tier 3 | Leo Tanaka | 549 | 525 | 73.71 | 26.63 | 3.90 | 3 |
| Network Operations | Tier 3 | Karen Vance | 556 | 532 | 72.56 | 31.51 | 3.74 | 4 |
| Network Operations | Tier 3 | Jack Reynolds | 538 | 516 | 71.51 | 27.61 | 3.83 | 5 |
| Service Desk - Tier 1 | Tier 1 | Quinn Hughes | 1 | 1 | 100.00 | 34.43 | 1.00 | 1 |
| Service Desk - Tier 1 | Tier 1 | Priya Sharma | 796 | 754 | 87.27 | 22.99 | 4.10 | 2 |
| Service Desk - Tier 1 | Tier 1 | Emma Watson | 803 | 757 | 86.00 | 23.07 | 4.11 | 3 |
| Service Desk - Tier 1 | Tier 1 | Carlos Mendez | 766 | 714 | 85.85 | 22.87 | 3.99 | 4 |
| Service Desk - Tier 1 | Tier 1 | David Kim | 801 | 755 | 85.83 | 23.30 | 3.99 | 5 |
| Service Desk - Tier 1 | Tier 1 | Alex Chen | 753 | 719 | 84.14 | 24.49 | 4.00 | 6 |

*Total rows returned: 21*

### Business Query 3: Active Backlog Aging & Critical Exposure Matrix

| Support_Team | Total_Open_Tickets | Currently_Overdue_Tickets | Overdue_Risk_Pct | Age_Under_12h | Age_12_to_24h | Age_24_to_48h | Age_Over_48h |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Service Desk - Tier 1 | 220 | 208 | 94.55 | 6 | 4 | 2 | 208 |
| Cloud & Systems Infrastructure | 83 | 79 | 95.18 | 2 | 4 | 4 | 73 |
| End User Support - Tier 2 | 68 | 64 | 94.12 | 1 | 1 | 2 | 64 |
| Network Operations | 70 | 63 | 90.00 | 4 | 3 | 5 | 58 |
| Identity & Access Management (IAM) | 45 | 41 | 91.11 | 1 | 3 | 4 | 37 |

*Total rows returned: 5*

