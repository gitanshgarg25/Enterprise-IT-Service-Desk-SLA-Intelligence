# Business Insights & Strategic Action Plan

**Project:** Enterprise IT Service Desk & SLA Intelligence Platform  
**Target Organization:** Enterprise IT Service Management (Fictional: Apex IT Solutions)  
**Reporting Period:** Fiscal Year 2026 (2025-10-01 to 2026-09-30)  
**Primary Question:** *"How can management improve SLA compliance and resolution efficiency without increasing support costs?"*

---

## Executive Summary Matrix

| # | Operational Insight | Empirical Evidence / KPI | Management Consequence | Low-Cost Strategic Action | Future Target Metric |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Network Bottleneck Drives 27.9% of Breaches** | SQL Business Query 1<br>Tableau Sheet `Root_Cause_Subcategories` | Floored productivity across engineering & corporate offices | Self-healing Wi-Fi scripts; redundant gateway DNS | Network breach rate: `27.75%` $\rightarrow$ `<15.0%` |
| **2** | **SLA Breaches Cause -1.60 CSAT Penalty** | SQL Query 9<br>Tableau Sheet `Root_Cause_CSAT_Impact` | Severe erosion of employee trust in IT services | Automated 75% SLA threshold early-warning alerts | Company CSAT: `3.97` $\rightarrow$ `>4.25 / 5.0` |
| **3** | **Tier 1 Holds 45.3% of Active Backlog** | SQL Query 7 & Business Query 3<br>Tableau Sheet `Team_Open_Backlog` | Frontline queue congestion delays initial triage | Self-service password/MFA deflection workflows | Tier 1 >48h backlog reduced by `>60%` |
| **4** | **Elevated Escalations in Cloud & Network** | SQL Query 8<br>Tableau Sheet `Team_Reopens_and_Escalations` | Engineer churn; tickets ping-ponging across tiers | Standardized Tier 1 diagnostic SOPs & runbooks | Cloud escalation: `15.37%` $\rightarrow$ `<10.0%` |
| **5** | **Premature Ticket Closure Churn (5.37%)** | SQL Query 8<br>Tableau Sheet `Team_Reopens_and_Escalations` | Duplication of triage labor on recurring incidents | Mandatory 48-hr user validation before hard closure | Reopen rate: `5.37%` $\rightarrow$ `<3.5%` |

---

## Detailed Evidence-Based Findings

### Finding 1: Network & Connectivity is the Primary Bottleneck Driving Corporate SLA Breaches
- **What the Data Shows:**
  - Out of 1,683 total corporate SLA breaches, Network Operations accounted for **437 breaches** (a team-level breach rate of **27.75%**), higher than any other group.
  - Average turnaround time for Network incidents was **28.61 hours** against a committed SLA of 30.16 hours, leaving a razor-thin buffer of just **1.55 hours** before breaching.
  - Examining subcategories reveals that four Network subcategories occupy the **top 4 ranks in company-wide breaches**:
    1. *Office Wi-Fi Access:* 132 breaches (28.09% subcategory breach rate; Rank 1)
    2. *DNS & Gateway Routing:* 126 breaches (27.10% subcategory breach rate; Rank 2)
    3. *Bandwidth & Latency:* 106 breaches (23.04% subcategory breach rate; Rank 3)
    4. *LAN Cable & Port:* 105 breaches (22.39% subcategory breach rate; Rank 4)
    Together, these four subcategories generated **469 breaches (27.87% of all corporate SLA failures)**.
- **Supporting Visual / Query:** SQL `Business Query 1` (CTE + DENSE_RANK); Tableau Dashboard 4 (`Root_Cause_Subcategories`).
- **Why it Matters to Management:** Network incidents rarely impact an isolated user; they degrade connectivity across entire functional wings, stalling client deliverables and video conferencing.
- **Action Plan:**
  1. Deploy automated local Wi-Fi client refresh scripts (releasing/renewing DHCP leases without manual engineer dispatch).
  2. Implement dual secondary DNS upstream resolvers to eliminate domain lookup timeouts.
  3. Reconfigure core switch monitoring to flag port duplex mismatches proactively.
- **Future Measurement:** Track Network Operations SLA compliance monthly (target: $\ge 85\%$) and mean Wi-Fi resolution time (target: $<18\text{ hrs}$).

---

### Finding 2: SLA Breaches Cause an Immediate 1.60-Point Drop in Customer Satisfaction (CSAT)
- **What the Data Shows:**
  - For tickets resolved within SLA, the average CSAT score is **4.25 / 5.0** (with 82.7% of respondents giving 4 or 5 stars).
  - When a ticket breaches its SLA window, the average CSAT score collapses to **2.65 / 5.0** (with 70.6% of respondents giving 1, 2, or 3 stars).
  - This empirical difference represents an immediate **-1.60 point drop (-37.6%)** in user satisfaction attributable strictly to turnaround delay.
- **Supporting Visual / Query:** SQL `Query 9`; Tableau Dashboard 4 (`Root_Cause_CSAT_Impact`).
- **Why it Matters to Management:** Internal customer sentiment is a direct proxy for business trust. Chronic delays breed user frustration and lead employees to bypass official IT ticketing channels.
- **Action Plan:**
  1. Configure an automated **"75% SLA Consumption Alert"** within the ITSM ticketing engine to notify queue managers 2 hours before high-priority tickets breach.
  2. Implement warm-handoff protocol for P1 and P2 incidents aged past 50% target.
- **Future Measurement:** Re-evaluate monthly CSAT against breached tickets (target: $>3.20$) and overall corporate CSAT (target: $>4.25$).

---

### Finding 3: Heavy Queue Concentration & Backlog Aging in Service Desk - Tier 1
- **What the Data Shows:**
  - Out of 486 active open tickets, **Service Desk - Tier 1 holds 220 tickets (45.27% of total corporate backlog)**.
  - Backlog aging analysis reveals that **208 of these 220 open tickets have been sitting in the queue for over 48 hours**.
- **Supporting Visual / Query:** SQL `Query 7` & `Business Query 3`; Tableau Dashboard 3 (`Team_Open_Backlog`).
- **Why it Matters to Management:** Tier 1 is the front line. When Tier 1 queues are clogged, new incoming tickets sit unassigned, creating artificial delays that cascade into Tier 2 and Tier 3.
- **Action Plan (Zero Additional Headcount):**
  1. Implement automated self-service password reset (SSPR) and MFA self-registration workflows.
  2. Create a self-service portal for standard software installation requests.
  3. These automated deflections will eliminate approximately 25–30% of repetitive Tier 1 requests, freeing frontline agents to triage complex tickets.
- **Future Measurement:** Reduction of Tier 1 tickets aged $>48\text{ hrs}$ by 60%, and improvement in First-Contact Resolution (FCR) rate from 68% to $>80\%$.

---

### Finding 4: Elevated Escalation Rates in Cloud Infrastructure (15.37%) and Network Operations (14.71%)
- **What the Data Shows:**
  - Overall company escalation rate is **11.23%** (1,123 tickets).
  - Cloud & Systems Infrastructure has an escalation rate of **15.37%** (281 tickets).
  - Network Operations has an escalation rate of **14.71%** (242 tickets).
  - By comparison, End User Support exhibits an escalation rate of only **8.68%**.
- **Supporting Visual / Query:** SQL `Query 8`; Tableau Dashboard 3 (`Team_Reopens_and_Escalations`).
- **Why it Matters to Management:** Every ticket escalation increases operational friction, adds handoff delays, and pulls senior Tier 3 engineering resources away from strategic architecture projects.
- **Action Plan:**
  1. Develop standard diagnostic runbooks for Tier 1 frontline agents covering basic Cloud VM status checks and storage permission triage.
  2. Enforce complete intake checklists before any incident can be escalated to Tier 3.
- **Future Measurement:** Reduce Cloud escalation rate from 15.37% to $<10.0\%$, and Network escalation from 14.71% to $<10.0\%$.

---

### Finding 5: Reopened Ticket Churn in Tier 1 Service Desk (6.00%)
- **What the Data Shows:**
  - Company-wide, **511 tickets were reopened** after being marked resolved (a **5.37%** reopen rate over the 9,514 resolved population).
  - Tier 1 Service Desk recorded the highest absolute churn with **222 reopened tickets (6.00% reopen rate)**.
- **Supporting Visual / Query:** SQL `Query 8`; Tableau Dashboard 3 (`Team_Reopens_and_Escalations`).
- **Why it Matters to Management:** A reopened ticket indicates that an agent closed the incident prematurely without validating that the user's root issue was truly fixed.
- **Action Plan:**
  1. Implement a 48-hour **"Resolved - Pending User Confirmation"** buffer period where tickets are not marked "Closed" until the employee confirms resolution.
  2. Conduct bi-weekly quality audits on agents with $>8\%$ personal reopen rates.
- **Future Measurement:** Drive overall corporate reopen rate from 5.37% down to $<3.5\%$.
