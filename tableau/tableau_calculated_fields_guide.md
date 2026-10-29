# Tableau Calculated Fields & Data Modeling Guide

This guide maps each production metric to its exact Tableau calculation syntax for building visualizations in Tableau Desktop or Tableau Public.

---

## 1. Connecting Data in Tableau Desktop

1. Open **Tableau Desktop 2026.2** from `/Applications`.
2. Under **Connect > To a File**, select **Text file** (or **Microsoft Excel** if connecting to `excel/Enterprise_IT_Service_Desk_Analytics.xlsx`).
3. Select `data/cleaned/itsm_tickets_cleaned.csv`.
4. (Optional Star Schema Join / Relationship):
   - Drag `dim_priority_sla.csv` into the Canvas; establish relationship on `Priority = Priority`.
   - Drag `dim_support_team.csv` into the Canvas; establish relationship on `Support Team = Support Team`.
   - Drag `dim_calendar.csv` into the Canvas; establish relationship on `DATE(Created Date) = Date`.

---

## 2. Production Tableau Calculated Fields

Create each calculated field by navigating to **Analysis > Create Calculated Field...** in the top menu.

---

### Calculation 1: `Total Tickets`
- **Data Type:** Integer
- **Tableau Formula:**
```tableau
COUNT([Ticket ID])
```

---

### Calculation 2: `Resolved Tickets`
- **Data Type:** Integer
- **Tableau Formula:**
```tableau
COUNT(IF [Status] = 'Resolved' OR [Status] = 'Closed' THEN [Ticket ID] END)
```

---

### Calculation 3: `Open Tickets (Backlog)`
- **Data Type:** Integer
- **Tableau Formula:**
```tableau
COUNT(IF [Status] != 'Resolved' AND [Status] != 'Closed' THEN [Ticket ID] END)
```

---

### Calculation 4: `SLA Met Tickets`
- **Data Type:** Integer
- **Tableau Formula:**
```tableau
COUNT(IF [SLA Status] = 'Met' THEN [Ticket ID] END)
```

---

### Calculation 5: `SLA Breached Tickets`
- **Data Type:** Integer
- **Tableau Formula:**
```tableau
COUNT(IF [SLA Status] = 'Breached' THEN [Ticket ID] END)
```

---

### Calculation 6: `SLA Compliance %`
- **Data Type:** Percentage (Default Format: `0.0%`)
- **Tableau Formula:**
```tableau
[SLA Met Tickets] / [Resolved Tickets]
```
*(Denominator: Strictly Resolved & Closed Tickets = 9,514)*

---

### Calculation 7: `SLA Breach Rate %`
- **Data Type:** Percentage (Default Format: `0.0%`)
- **Tableau Formula:**
```tableau
[SLA Breached Tickets] / [Resolved Tickets]
```

---

### Calculation 8: `Avg Resolution Hours`
- **Data Type:** Number (Decimal, `0.00`)
- **Tableau Formula:**
```tableau
AVG([Actual Resolution Hours])
```
*(Open tickets carry NULL and are automatically excluded by Tableau's AVG aggregation)*

---

### Calculation 9: `Avg SLA Target Hours`
- **Data Type:** Number (Decimal, `0.00`)
- **Tableau Formula:**
```tableau
AVG(IF [Status] = 'Resolved' OR [Status] = 'Closed' THEN [SLA Target Hours] END)
```

---

### Calculation 10: `Turnaround Buffer Hours`
- **Data Type:** Number (Decimal, `0.00`)
- **Tableau Formula:**
```tableau
[Avg SLA Target Hours] - [Avg Resolution Hours]
```

---

### Calculation 11: `Avg CSAT Score`
- **Data Type:** Number (Decimal, `0.00`)
- **Tableau Formula:**
```tableau
AVG([Customer Satisfaction Score])
```

---

### Calculation 12: `Reopened Rate %`
- **Data Type:** Percentage (`0.0%`)
- **Tableau Formula:**
```tableau
SUM([Reopened Flag]) / [Resolved Tickets]
```

---

### Calculation 13: `Escalation Rate %`
- **Data Type:** Percentage (`0.0%`)
- **Tableau Formula:**
```tableau
SUM([Escalated Flag]) / [Total Tickets]
```

---

### Calculation 14: `Backlog Aging Bucket`
- **Data Type:** String
- **Tableau Formula:**
```tableau
IF ISNULL([Resolved Date]) THEN
    IF DATEDIFF('hour', [Created Date], #2026-10-01 00:00:00#) < 12 THEN "1. Under 12 Hours"
    ELSEIF DATEDIFF('hour', [Created Date], #2026-10-01 00:00:00#) < 24 THEN "2. 12 to 24 Hours"
    ELSEIF DATEDIFF('hour', [Created Date], #2026-10-01 00:00:00#) < 48 THEN "3. 24 to 48 Hours"
    ELSE "4. Over 48 Hours"
    END
END
```

---

## 3. Formatting Standards in Tableau
- **Color Palettes:**
  - Executive Navy: `#1B365D` (Primary bars, headers, lines)
  - SLA Met: Soft Sage Green `#2E7D32`
  - SLA Breached: Crimson Coral `#C62828`
  - Background: Crisp White `#FFFFFF` and Slate White `#F8FAFC`
- **Tooltips:** Clean formatting showing Category, Priority, Exact Count, and Percentage of Total.
