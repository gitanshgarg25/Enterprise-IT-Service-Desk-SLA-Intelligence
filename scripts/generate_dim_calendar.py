"""
Calendar Dimension Generator
Creates data/cleaned/dim_calendar.csv covering 2025-10-01 to 2026-09-30 (365 days)
"""

import os
import csv
from datetime import datetime, timedelta

def generate_dim_calendar():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cal_path = os.path.join(base_dir, "data", "cleaned", "dim_calendar.csv")

    start_date = datetime(2025, 10, 1)
    end_date = datetime(2026, 9, 30)

    rows = []
    curr = start_date
    while curr <= end_date:
        d_str = curr.strftime("%Y-%m-%d")
        year = curr.year
        month = curr.month
        month_name = curr.strftime("%B")
        year_month = curr.strftime("%Y-%m")
        quarter = f"Q{(month - 1) // 3 + 1}"
        day_of_week = curr.strftime("%A")
        is_weekend = 1 if curr.weekday() >= 5 else 0
        is_weekday = 0 if is_weekend else 1

        rows.append([
            d_str, year, month, month_name, year_month, quarter, day_of_week, is_weekend, is_weekday
        ])
        curr += timedelta(days=1)

    with open(cal_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Year", "Month_Number", "Month_Name", "Year_Month", "Quarter", "Day_Of_Week", "Is_Weekend", "Is_Weekday"])
        writer.writerows(rows)

    print(f"Calendar dimension successfully written to {cal_path} ({len(rows)} days)")

if __name__ == "__main__":
    generate_dim_calendar()
