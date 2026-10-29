"""
High-Resolution Dashboard & Excel Visual Renderer
Generates high-fidelity visual representations of the 4 Tableau Dashboards
and the Excel Executive Workbook for the GitHub README portfolio.

Outputs:
1. documentation/screenshots/tableau_dashboard_1_overview.png
2. documentation/screenshots/tableau_dashboard_2_sla.png
3. documentation/screenshots/tableau_dashboard_3_workload.png
4. documentation/screenshots/tableau_dashboard_4_root_causes.png
5. documentation/screenshots/excel_kpi_summary.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Color Palette
NAVY = "#1B365D"
DARK_BLUE = "#0F2537"
SLATE_BG = "#F4F7FA"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#222222"
TEXT_MUTED = "#666666"
GREEN_MET = "#2E7D32"
RED_BREACH = "#C62828"
ACCENT_BLUE = "#1976D2"
AMBER_WARN = "#EF6C00"
BORDER_COLOR = "#E0E0E0"

def set_card(ax, title):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, fontsize=12, fontweight='bold', color=NAVY, pad=12, loc='left')
    ax.grid(axis='y', linestyle='--', alpha=0.3, color="#CCCCCC")
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)
        spine.set_linewidth(1)

def render_dashboard_1(out_dir):
    fig = plt.figure(figsize=(15, 9.5), facecolor=SLATE_BG)
    fig.suptitle("ITSM Executive Service Desk & SLA Intelligence Platform | Executive Overview", 
                 fontsize=16, fontweight='bold', color=NAVY, y=0.96)
    
    # 6 KPI Top Cards
    kpis = [
        ("Total Intake", "10,000", "Gross tickets", NAVY),
        ("Resolved Tickets", "9,514", "95.14% resolution", NAVY),
        ("Active Backlog", "486", "4.86% in progress", AMBER_WARN),
        ("SLA Compliance", "82.31%", "Target: ≥ 85.0%", GREEN_MET),
        ("SLA Breaches", "1,683", "17.69% breach rate", RED_BREACH),
        ("Avg Resolution", "24.77h", "Target: 30.33h", ACCENT_BLUE)
    ]
    for i, (title, val, sub, col) in enumerate(kpis):
        ax_kpi = fig.add_axes([0.05 + i * 0.155, 0.83, 0.135, 0.08])
        ax_kpi.set_facecolor(CARD_BG)
        ax_kpi.set_xticks([])
        ax_kpi.set_yticks([])
        for spine in ax_kpi.spines.values():
            spine.set_color(BORDER_COLOR)
        ax_kpi.text(0.5, 0.72, title, fontsize=9, fontweight='bold', color=TEXT_MUTED, ha='center', va='center')
        ax_kpi.text(0.5, 0.42, val, fontsize=15, fontweight='bold', color=col, ha='center', va='center')
        ax_kpi.text(0.5, 0.16, sub, fontsize=7.5, color=TEXT_MUTED, ha='center', va='center')

    # Chart 1: Monthly Trend
    ax1 = fig.add_axes([0.05, 0.10, 0.58, 0.67])
    set_card(ax1, "Monthly Ticket Intake & Trend (Oct 2025 – Sep 2026)")
    months = ["Oct '25", "Nov", "Dec", "Jan '26", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep '26"]
    vol = [967, 782, 824, 817, 758, 841, 815, 887, 819, 826, 869, 795]
    ax1.plot(months, vol, marker='o', color=NAVY, linewidth=2.5, markersize=6, label="Intake Volume")
    ax1.fill_between(months, vol, alpha=0.1, color=ACCENT_BLUE)
    ax1.axhline(sum(vol)/12, color=AMBER_WARN, linestyle=':', linewidth=1.5, label=f"Monthly Mean ({int(sum(vol)/12):,})")
    for m, v in zip(months, vol):
        ax1.text(m, v + 12, str(v), ha='center', fontsize=8, color=TEXT_DARK)
    ax1.set_ylim(650, 1050)
    ax1.legend(loc='lower left', frameon=False, fontsize=9)

    # Chart 2: Priority Share
    ax2 = fig.add_axes([0.67, 0.10, 0.28, 0.67])
    set_card(ax2, "Ticket Distribution by Priority")
    prios = ["Medium (P3)", "Low (P4)", "High (P2)", "Critical (P1)"]
    p_vol = [4792, 2339, 2042, 827]
    p_pct = [47.92, 23.39, 20.42, 8.27]
    colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444"]
    bars = ax2.barh(prios, p_vol, color=colors, height=0.55)
    for bar, pct, v in zip(bars, p_pct, p_vol):
        ax2.text(bar.get_width() + 70, bar.get_y() + bar.get_height()/2, f"{v:,} ({pct:.1f}%)", 
                 va='center', fontsize=8.5, color=TEXT_DARK, fontweight='bold')
    ax2.set_xlim(0, 5600)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)

    path = os.path.join(out_dir, "tableau_dashboard_1_overview.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

def render_dashboard_2(out_dir):
    fig = plt.figure(figsize=(15, 9.5), facecolor=SLATE_BG)
    fig.suptitle("ITSM SLA & Priority Analysis | Compliance, Breach Rates & Operational Buffers", 
                 fontsize=16, fontweight='bold', color=NAVY, y=0.96)

    # Chart 1: SLA Compliance by Priority
    ax1 = fig.add_axes([0.05, 0.54, 0.42, 0.35])
    set_card(ax1, "SLA Compliance Rate by Urgency Level")
    prios = ["Critical (4h)", "High (8h)", "Medium (24h)", "Low (72h)"]
    comp = [81.04, 82.76, 82.74, 81.47]
    bars = ax1.bar(prios, comp, color=ACCENT_BLUE, width=0.5)
    ax1.axhline(85.0, color=RED_BREACH, linestyle='--', linewidth=1.5, label="Target: 85.0%")
    for b, c in zip(bars, comp):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 1.2, f"{c:.2f}%", ha='center', fontsize=8.5, fontweight='bold')
    ax1.set_ylim(60, 95)
    ax1.legend(loc='lower right', frameon=False, fontsize=8.5)

    # Chart 2: SLA Breaches by Category
    ax2 = fig.add_axes([0.53, 0.54, 0.42, 0.35])
    set_card(ax2, "Total SLA Breaches by Category")
    cats = ["Network & Connectivity", "Cloud & Infrastructure", "Access & Identity", "Software & Applications", "Hardware & Workstation"]
    breaches = [437, 367, 323, 298, 258]
    bars2 = ax2.barh(cats, breaches, color=RED_BREACH, height=0.5)
    for b, v in zip(bars2, breaches):
        ax2.text(b.get_width() + 8, b.get_y() + b.get_height()/2, f"{v:,} breaches ({v/1683*100:.1f}%)", 
                 va='center', fontsize=8.5, color=TEXT_DARK)
    ax2.set_xlim(0, 520)

    # Chart 3: SLA Breach Rate by Support Team
    ax3 = fig.add_axes([0.05, 0.08, 0.42, 0.36])
    set_card(ax3, "SLA Breach Rate % by Support Group")
    teams = ["Network Ops", "Cloud Infra", "End User Supp", "IAM", "Tier 1 Desk"]
    rates = [27.75, 19.14, 15.86, 15.90, 13.95]
    colors = [RED_BREACH if r > 20 else AMBER_WARN if r > 15 else GREEN_MET for r in rates]
    bars3 = ax3.bar(teams, rates, color=colors, width=0.5)
    for b, r in zip(bars3, rates):
        ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 0.6, f"{r:.1f}%", ha='center', fontsize=8.5, fontweight='bold')
    ax3.set_ylim(0, 35)

    # Chart 4: Actual vs Target Duration
    ax4 = fig.add_axes([0.53, 0.08, 0.42, 0.36])
    set_card(ax4, "Turnaround Hours: Actual vs Committed SLA")
    t_teams = ["Network Ops", "Cloud Infra", "IAM", "End User", "Tier 1 Desk"]
    act_hrs = [28.61, 25.41, 24.14, 23.92, 23.34]
    tgt_hrs = [30.16, 30.58, 29.74, 30.55, 30.36]
    x = range(len(t_teams))
    w = 0.32
    ax4.bar([i - w/2 for i in x], act_hrs, width=w, label="Actual Avg (hrs)", color=NAVY)
    ax4.bar([i + w/2 for i in x], tgt_hrs, width=w, label="SLA Target (hrs)", color="#94A3B8")
    ax4.set_xticks(x)
    ax4.set_xticklabels(t_teams, fontsize=8.5)
    ax4.legend(loc='lower left', frameon=False, fontsize=8.5)
    ax4.set_ylim(0, 36)

    path = os.path.join(out_dir, "tableau_dashboard_2_sla.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

def render_dashboard_3(out_dir):
    fig = plt.figure(figsize=(15, 9.5), facecolor=SLATE_BG)
    fig.suptitle("ITSM Workload & Team Performance | Capacity, Backlog & Service Quality", 
                 fontsize=16, fontweight='bold', color=NAVY, y=0.96)

    # Chart 1: Ticket Volume Distribution
    ax1 = fig.add_axes([0.05, 0.54, 0.42, 0.35])
    set_card(ax1, "Gross Ticket Intake by Support Team")
    teams = ["Tier 1 Desk", "Cloud Infra", "Network Ops", "End User Supp", "IAM"]
    vols = [3920, 1828, 1645, 1543, 1064]
    b1 = ax1.bar(teams, vols, color=NAVY, width=0.5)
    for b, v in zip(b1, vols):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 50, f"{v:,} ({v/100:.1f}%)", ha='center', fontsize=8.5, fontweight='bold')
    ax1.set_ylim(0, 4400)

    # Chart 2: Open Backlog by Priority
    ax2 = fig.add_axes([0.53, 0.54, 0.42, 0.35])
    set_card(ax2, "Active Open Backlog Queue by Support Team (486 Total)")
    backlog_teams = ["Tier 1 Desk", "Cloud Infra", "Network Ops", "End User Supp", "IAM"]
    backlogs = [220, 83, 70, 68, 45]
    b2 = ax2.bar(backlog_teams, backlogs, color=AMBER_WARN, width=0.5)
    for b, v in zip(b2, backlogs):
        ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 3, f"{v} ({v/486*100:.1f}%)", ha='center', fontsize=8.5, fontweight='bold')
    ax2.set_ylim(0, 260)

    # Chart 3: Turnaround Buffer Hours
    ax3 = fig.add_axes([0.05, 0.08, 0.42, 0.36])
    set_card(ax3, "Operational Turnaround Buffer Hours (Target - Actual)")
    t_teams = ["Tier 1 Desk", "End User Supp", "IAM", "Cloud Infra", "Network Ops"]
    buffers = [7.01, 6.63, 5.59, 5.17, 1.55]
    colors = [GREEN_MET if b > 5 else AMBER_WARN if b > 3 else RED_BREACH for b in buffers]
    b3 = ax3.bar(t_teams, buffers, color=colors, width=0.5)
    for b, v in zip(b3, buffers):
        ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 0.15, f"+{v:.2f}h", ha='center', fontsize=8.5, fontweight='bold')
    ax3.set_ylim(0, 8.5)

    # Chart 4: Reopens & Escalations
    ax4 = fig.add_axes([0.53, 0.08, 0.42, 0.36])
    set_card(ax4, "Service Friction: Reopened Rate % vs Escalation Rate %")
    teams_f = ["Tier 1 Desk", "Cloud Infra", "End User", "Network Ops", "IAM"]
    reopen = [6.00, 5.39, 5.02, 4.76, 4.51]
    escalate = [9.49, 15.37, 8.68, 14.71, 8.83]
    x = range(len(teams_f))
    w = 0.32
    ax4.bar([i - w/2 for i in x], reopen, width=w, label="Reopened Rate %", color="#E11D48")
    ax4.bar([i + w/2 for i in x], escalate, width=w, label="Escalation Rate %", color="#4F46E5")
    ax4.set_xticks(x)
    ax4.set_xticklabels(teams_f, fontsize=8.5)
    ax4.legend(loc='upper right', frameon=False, fontsize=8.5)
    ax4.set_ylim(0, 18)

    path = os.path.join(out_dir, "tableau_dashboard_3_workload.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

def render_dashboard_4(out_dir):
    fig = plt.figure(figsize=(15, 9.5), facecolor=SLATE_BG)
    fig.suptitle("ITSM Root Causes & Strategic Recommendations | Bottlenecks, CSAT & Action Plan", 
                 fontsize=16, fontweight='bold', color=NAVY, y=0.96)

    # Chart 1: Top 10 Root Cause Breaches
    ax1 = fig.add_axes([0.05, 0.48, 0.58, 0.41])
    set_card(ax1, "Top 10 Subcategories Driving SLA Breaches")
    subs = [
        "Office Wi-Fi Access (Net)",
        "DNS & Gateway Routing (Net)",
        "Bandwidth & Latency (Net)",
        "LAN Cable & Port (Net)",
        "Cloud Storage Perms (Cloud)",
        "Virtual Machine Crash (Cloud)",
        "Server Provisioning (Cloud)",
        "Database Connectivity (Cloud)",
        "Laptop Freeze & OS (HW)",
        "Peripheral Malfunction (HW)"
    ]
    sub_brk = [132, 126, 106, 105, 97, 97, 90, 83, 80, 80]
    sub_colors = [RED_BREACH if i < 4 else "#EA580C" if i < 8 else "#0284C7" for i in range(10)]
    bars = ax1.barh(subs[::-1], sub_brk[::-1], color=sub_colors[::-1], height=0.55)
    for b, v in zip(bars, sub_brk[::-1]):
        ax1.text(b.get_width() + 2, b.get_y() + b.get_height()/2, f"{v} ({v/1683*100:.1f}%)", 
                 va='center', fontsize=8, color=TEXT_DARK)
    ax1.set_xlim(0, 155)

    # Chart 2: CSAT Drop
    ax2 = fig.add_axes([0.68, 0.48, 0.27, 0.41])
    set_card(ax2, "The Customer Satisfaction Penalty")
    outcomes = ["SLA Met", "SLA Breached"]
    csats = [4.25, 2.65]
    b2 = ax2.bar(outcomes, csats, color=[GREEN_MET, RED_BREACH], width=0.45)
    for b, v in zip(b2, csats):
        ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 0.1, f"{v:.2f} / 5.0", ha='center', fontsize=10, fontweight='bold')
    ax2.text(0.5, 3.5, "Δ -1.60 pts\n(-37.6% drop)", ha='center', fontsize=11, fontweight='bold', color=RED_BREACH,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEE2E2', edgecolor=RED_BREACH, alpha=0.8))
    ax2.set_ylim(0, 5.0)

    # Lower Panel: Strategic Action Plan Matrix (Table)
    ax_rec = fig.add_axes([0.05, 0.06, 0.90, 0.34])
    ax_rec.set_facecolor(CARD_BG)
    ax_rec.set_xticks([])
    ax_rec.set_yticks([])
    for spine in ax_rec.spines.values():
        spine.set_color(BORDER_COLOR)
    ax_rec.set_title("Strategic Zero-Cost Management Recommendations & Future Targets", fontsize=11, fontweight='bold', color=NAVY, loc='left', pad=8)

    rec_headers = ["Strategic Focus", "Operational Finding", "Actionable Zero-Cost Solution", "Future Target Metric"]
    rec_rows = [
        ("1. Network Diagnostics", "4 Net subcategories cause 27.9% of breaches", "Deploy automated Wi-Fi client refresh & DNS failover scripts", "Reduce Network breach rate to < 15%"),
        ("2. SLA Proactive Alerts", "Breaching SLA triggers immediate -1.60 CSAT drop", "Automate 75% SLA consumption alerts to queue managers", "Improve corporate CSAT to > 4.25 / 5.0"),
        ("3. Frontline Deflection", "Tier 1 holds 45.3% of backlog; 208 aged >48 hrs", "Implement self-service password & role-permission portal", "Clear 60% of >48h Tier 1 backlog"),
        ("4. Triage Runbooks", "Cloud has 15.4% and Network has 14.7% escalation", "Publish Tier 1 standardized SOPs for VM restarts and permissions", "Lower escalation rate to < 10%"),
        ("5. Closure Validation", "511 tickets reopened; Tier 1 churn is 6.00%", "Enforce mandatory 48-hr user validation before hard closure", "Reduce company reopen rate to < 3.5%")
    ]

    col_x = [0.02, 0.22, 0.48, 0.80]
    # Header
    for idx, h in enumerate(rec_headers):
        ax_rec.text(col_x[idx], 0.88, h, fontsize=9.5, fontweight='bold', color=NAVY)
    ax_rec.axhline(0.82, color=BORDER_COLOR, linewidth=1)

    y_pos = 0.68
    for row in rec_rows:
        for idx, text in enumerate(row):
            weight = 'bold' if idx == 0 else 'normal'
            color = NAVY if idx == 0 else GREEN_MET if idx == 3 else TEXT_DARK
            ax_rec.text(col_x[idx], y_pos, text, fontsize=8, color=color, fontweight=weight)
        y_pos -= 0.14

    path = os.path.join(out_dir, "tableau_dashboard_4_root_causes.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

def render_excel_summary(out_dir):
    fig = plt.figure(figsize=(15, 9.5), facecolor="#F8FAFC")
    fig.suptitle("Microsoft Excel Analytics Workbook | Sheet: KPI_Summary (Live Dynamic Formulas)", 
                 fontsize=15, fontweight='bold', color=NAVY, y=0.96)

    # Draw Excel sheet grid aesthetics
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.86])
    ax.set_facecolor("#FFFFFF")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#CBD5E1")

    # Sheet Title Banner
    ax.text(0.03, 0.94, "ITSM Executive Service Desk KPI Dashboard", fontsize=15, fontweight='bold', color=NAVY)
    ax.text(0.03, 0.90, "Dynamic Excel workbook referencing Cleaned_Data using COUNTA, COUNTIFS, AVERAGE, SUMIF", fontsize=8.5, color=TEXT_MUTED, style='italic')

    # KPI Blocks
    kpis = [
        ("Total Intake", "=COUNTA(Cleaned_Data!A2:A10001)", "10,000", 0.03, 0.74),
        ("Resolved Tickets", "=COUNTIF(...)+COUNTIF(...)", "9,514", 0.27, 0.74),
        ("Active Backlog", "=COUNTIFS(...,'<>Resolved',...)", "486", 0.51, 0.74),
        ("Resolution Rate", "=D6/B6", "95.14%", 0.75, 0.74),
        
        ("SLA Met Tickets", "=COUNTIF(Cleaned_Data!M2:M10001,'Met')", "7,831", 0.03, 0.54),
        ("SLA Breached", "=COUNTIF(Cleaned_Data!M2:M10001,'Breached')", "1,683", 0.27, 0.54),
        ("SLA Compliance %", "=B10/D6 [Resolved Denominator]", "82.31%", 0.51, 0.54),
        ("SLA Breach Rate %", "=D10/D6", "17.69%", 0.75, 0.54),

        ("Avg Resolution", "=AVERAGE(Cleaned_Data!L2:L10001)", "24.77 hrs", 0.03, 0.34),
        ("Avg SLA Target", "=(SUMIF(...)+SUMIF(...))/D6", "30.33 hrs", 0.27, 0.34),
        ("Turnaround Buffer", "=D14-B14 [Safety Margin]", "+5.56 hrs", 0.51, 0.34),
        ("Customer CSAT", "=AVERAGE(Cleaned_Data!N2:N10001)", "3.97 / 5.0", 0.75, 0.34)
    ]

    for title, formula, val, x, y in kpis:
        rect = patches.FancyBboxPatch((x, y), 0.22, 0.16, boxstyle="round,pad=0.01", 
                                      facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1)
        ax.add_patch(rect)
        ax.text(x + 0.11, y + 0.12, title, fontsize=9, fontweight='bold', color=NAVY, ha='center')
        ax.text(x + 0.11, y + 0.065, val, fontsize=14, fontweight='bold', color=DARK_BLUE, ha='center')
        ax.text(x + 0.11, y + 0.02, formula, fontsize=6.5, color=TEXT_MUTED, ha='center', style='italic')

    # Lower Table Summary Preview
    rect_tbl = patches.Rectangle((0.03, 0.04), 0.94, 0.25, facecolor="#F1F5F9", edgecolor="#CBD5E1")
    ax.add_patch(rect_tbl)
    ax.text(0.05, 0.25, "Worksheet Tab Navigation:", fontsize=9.5, fontweight='bold', color=NAVY)
    tabs = [
        "1. Raw_Data (10,008 rows)", 
        "2. Cleaned_Data (10,000 rows)", 
        "3. Data_Quality (Audit & Rules)", 
        "4. KPI_Summary (Dynamic Formulas)", 
        "5. Pivot_Analysis (Monthly & Team)", 
        "6. Business_Insights (5 Action Plans)"
    ]
    for idx, t in enumerate(tabs):
        ax.text(0.05 + (idx % 3) * 0.31, 0.18 - (idx // 3) * 0.08, f"▸ {t}", fontsize=8.5, color=TEXT_DARK, fontweight='bold')

    path = os.path.join(out_dir, "excel_kpi_summary.png")
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "documentation", "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    
    render_dashboard_1(out_dir)
    render_dashboard_2(out_dir)
    render_dashboard_3(out_dir)
    render_dashboard_4(out_dir)
    render_excel_summary(out_dir)
    print("All 5 high-resolution portfolio screenshots rendered successfully!")

if __name__ == "__main__":
    main()
