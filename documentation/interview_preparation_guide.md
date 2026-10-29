# Comprehensive Interview Preparation Guide

**Project:** Enterprise IT Service Desk & SLA Intelligence Platform  
**Target Roles:** Data Analyst, Business Analyst, Insights & BI Developer (Infosys, TCS, Wipro, Accenture)  
**Core Stack:** SQL (SQLite / ANSI SQL), Microsoft Excel, Tableau Desktop / Power BI (DAX)

---

## 1. Resume Entry (3 High-Impact Bullet Points)

Add this entry under **Projects** on your resume:

> **Enterprise IT Service Desk & SLA Intelligence Platform** | *SQL, Tableau, Excel, Data Modeling*
> - Engineered an end-to-end IT service desk analytics platform auditing **10,000 incident records** across 5 enterprise support tiers to uncover operational bottlenecks and drive SLA optimization.
> - Formulated an in-engine SQLite data pipeline utilizing **CTEs, Window Functions (`RANK`, `DENSE_RANK`, `LAG`), and Conditional Aggregations** to analyze ticket aging, support group backlogs, and multi-tier escalation churn.
> - Built a **4-page interactive executive dashboard** and macro-free dynamic Excel model demonstrating that **Network & Connectivity incidents drive 27.87% of corporate SLA breaches** and trigger a **-1.60 point drop in Customer Satisfaction (CSAT)**, delivering 5 zero-cost mitigation strategies.

---

## 2. 60-Second Project "Elevator Pitch"

> *"In this project, I developed an end-to-end IT Service Desk and SLA Intelligence Platform to solve a core business challenge: **how can IT leadership improve service level compliance and operational efficiency without increasing support costs?**"*
>
> *"I started with an extraction of over 10,000 raw ITSM incident records. I built an automated Python cleaning pipeline that resolved duplicate records, normalized text casing, and enforced ITIL date-logic rules with a 100% audit pass rate."*
>
> *"Next, I loaded the data into SQLite and modeled it into a Kimball Star Schema. Using CTEs, window ranking functions, and time-intelligence queries, I discovered that **Network & Connectivity incidents (specifically Wi-Fi and DNS routing) were responsible for 27.87% of all corporate SLA breaches**, and when an SLA breached, user satisfaction plunged by **1.60 points** on a 5-point scale."*
>
> *"Finally, I developed dynamic Excel models with native formulas and an interactive 4-page Tableau dashboard suite. I translated these empirical findings into five zero-cost operational recommendations—such as automated Wi-Fi client refresh scripts and early 75% SLA warning alerts—that directly address root bottlenecks without requiring new hires."*

---

## 3. Ten Likely Interview Questions & Model Answers

### Q1: Why did you choose an IT Service Desk project instead of a generic sales or e-commerce dataset?
**Answer:**  
*"IT Service Desk and operational ticket analytics are central to enterprise IT companies like Infosys, which manage global client infrastructure under strict contractual Service Level Agreements (SLAs). Analyzing ticket turnaround, breach liabilities, agent workloads, and CSAT scores demonstrates my ability to solve real operational business problems rather than just summarizing revenue numbers."*

---

### Q2: How did you define the denominator for SLA Compliance Rate, and why does it matter?
**Answer:**  
*"Under ITIL standards, SLA Compliance Rate must be evaluated **strictly over resolved and closed tickets** (7,831 Met / 9,514 Resolved = 82.31%). A common beginner mistake is dividing by total tickets (10,000), which artificially inflates compliance because active open tickets cannot be audited for historical compliance until their lifecycle concludes. In my data model, I kept open tickets clearly labeled as 'Open - In Evaluation' to prevent metric contamination."*

---

### Q3: What is the difference between calendar hours and business hours in SLA calculations, and which did you use?
**Answer:**  
*"Business hours only count working hours (e.g., 9 AM to 5 PM, Monday through Friday, excluding public holidays), whereas calendar hours calculate elapsed clock time continuously. For consistency and simplicity, I used calendar hours across all 10,000 tickets. In a live enterprise ITSM environment like ServiceNow, business hours are calculated using custom operational work schedules, but the underlying data modeling and KPI relationships remain identical."*

---

### Q4: Explain the Star Schema data model you designed. Why not keep everything in one flat table?
**Answer:**  
*"While a single flat table works for basic charts, enterprise dimensional modeling (Kimball methodology) uses a Star Schema to separate transactional facts from descriptive dimensions. I established a central `fact_tickets` table (10,000 records) connected via 1:Many relationships to `dim_priority_sla`, `dim_support_team`, and `dim_calendar`. This architecture eliminates redundant text storage, optimizes query performance, prevents filter context ambiguity in BI tools, and makes it easy to add new dimensions like geographical location or cost centers in the future."*

---

### Q5: Walk me through one of your advanced SQL queries. What technique did you use and why?
**Answer:**  
*"In Business Query 1, I performed a Root-Cause Bottleneck Analysis. I wrote a Common Table Expression (CTE) to aggregate resolved tickets, breach counts, and average CSAT grouped by `Category` and `Subcategory`. In the outer query, I used the window function `DENSE_RANK() OVER (ORDER BY Breached_Tickets DESC)` to rank each subcategory across the company. This immediately revealed that four Network & Connectivity subcategories held ranks 1 through 4, accounting for 27.87% of all corporate SLA failures. Using a CTE kept the logic modular and readable."*

---

### Q6: How did you ensure data quality and handle dirty data during the ingestion phase?
**Answer:**  
*"I implemented an automated data quality pipeline testing 8 rules:
1. **Uniqueness:** Identified and dropped 5 duplicate ticket rows resulting from simulated webhook retries.
2. **Test Filtering:** Excluded 3 QA testing records (`TEST-`, `DEV-`).
3. **String Hygiene & Casing:** Standardized whitespace and Title Case.
4. **Date Logic:** Enforced `Resolved_Date >= Created_Date` (zero negative durations).
5. **Status Consistency:** Ensured 100% of open tickets had NULL resolution dates and actual hours, and 100% of resolved tickets had positive resolution times.
Every check was logged in a formal Data Quality Report before running analytical queries."*

---

### Q7: If management has a fixed budget and cannot hire more support engineers, what is your top recommendation based on the data?
**Answer:**  
*"My primary recommendation is **frontline deflection and automated self-healing scripts**. The data shows that Service Desk - Tier 1 holds 45.27% of all open tickets, with 208 tickets aged over 48 hours. By implementing self-service password reset (SSPR) and automated access workflows, we can deflect an estimated 25–30% of repetitive Tier 1 requests without adding headcount. This allows Tier 1 agents to triage complex network and cloud tickets faster, resolving the backlog before tickets breach."*

---

### Q8: What did your analysis reveal about the relationship between SLA breaches and Customer Satisfaction (CSAT)?
**Answer:**  
*"There is an empirical, statistically significant penalty: tickets resolved within SLA averaged **4.25 / 5.0** CSAT, with 82.7% positive ratings. When an SLA was breached, CSAT dropped by **1.60 points down to 2.65 / 5.0**, with over 70% negative ratings. This proves to management that SLA targets are not just arbitrary operational deadlines; they directly safeguard employee sentiment and business trust."*

---

### Q9: How would you implement this same project in Power BI if a client environment required it?
**Answer:**  
*"The analytical framework translates directly. In Power BI, I would ingest the cleaned CSV using Power Query, establish 1:Many relationships to dimension tables in the Model View, and create DAX measures using `CALCULATE`, `COUNTROWS`, and `DIVIDE` (with `0` fallback) to prevent divide-by-zero errors. The report visuals would be organized into the same 4 pages (Executive Overview, SLA Analysis, Team Performance, and Root Causes) with slicers for Date, Priority, and Support Team."*

---

### Q10: What are the main limitations of your project that an interviewer should know?
**Answer:**  
*"Honesty about limitations is critical:
1. **Synthetic Data Disclosure:** The dataset simulates realistic operational patterns with a fixed random seed (`42`), but findings represent a simulated enterprise environment, not real corporate employee data.
2. **Calendar Hours vs. Business Hours:** SLA calculations use continuous clock hours rather than business shift hours.
3. **Survey Response Bias:** CSAT was collected on ~63.6% of resolved tickets; users with extreme experiences (very happy or very frustrated) may be slightly over-represented.
4. **Cross-Team Routing:** Re-assignments between teams were simplified to primary assigned groups."*

---

## 4. Key Metrics Cheat Sheet for Quick Reference

Keep these numbers memorized before any interview:

| Metric | Exact Number | Context / Denominator |
| :--- | :---: | :--- |
| **Total Ticket Volume** | `10,000` | Full 12-month fiscal intake |
| **Resolved Tickets** | `9,514` | 95.14% resolution throughput |
| **Active Open Backlog** | `486` | 4.86% active queue liabilities |
| **Contractual SLA Met** | `7,831` | **82.31%** compliance rate (denom: 9,514) |
| **SLA Breaches** | `1,683` | **17.69%** breach rate (denom: 9,514) |
| **Average Actual Turnaround** | `24.77 hrs` | vs `30.33 hrs` committed SLA benchmark |
| **Turnaround Buffer** | `+5.56 hrs` | Safety buffer before system-wide breach |
| **Average CSAT** | `3.97 / 5.0` | Out of 6,053 survey responses |
| **CSAT Delta (Met vs Breached)**| `4.25` vs `2.65` | **-1.60 point drop** (-37.6% satisfaction penalty) |
| **Top Root Cause Breach Share**| `27.87%` | 4 Network subcategories cause 469 breaches |
| **Tier 1 Backlog Share** | `45.27%` | 220 out of 486 active tickets sit in Tier 1 |
| **Escalation Rate (Total)** | `11.23%` | 1,123 tickets (Cloud leads at 15.37%) |
| **Reopened Rate (Resolved)** | `5.37%` | 511 tickets (Tier 1 leads at 6.00%) |
