import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from zoneinfo import ZoneInfo
import numpy as np
import matplotlib.dates as mdates

df = pd.read_csv("orac_submissions.csv")

df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
df["datetime"] = df["datetime"].dt.tz_convert(ZoneInfo("Australia/Brisbane")) # replace this with your country/city

df["score"] = pd.to_numeric(df["score"], errors="coerce")

df_sorted = df.sort_values("datetime").reset_index(drop=True)

df_sorted["cumulative"] = range(1, len(df_sorted) + 1)

colors = []
solved_set = set()

for i, row in df_sorted.iterrows():
    pname = row["problem_name"]
    score = row["score"]

    if pd.isna(score):
        colors.append("gray")
    elif score == 0:
        colors.append("red")
    elif 0 < score < 100:
        colors.append("yellow")
    elif score == 100:
        if pname not in solved_set:
            colors.append("green")
            solved_set.add(pname)
        else:
            colors.append("gray")
    else:
        colors.append("gray")

plt.figure(figsize=(10, 5))

# --- Black line connecting all points ---
plt.plot(df_sorted["datetime"], df_sorted["cumulative"], color='black', linewidth=1, zorder=1)

# --- Colored dots ---
plt.scatter(df_sorted["datetime"], df_sorted["cumulative"], c=colors, s=15, zorder=2)

# --- Title and labels ---
plt.title("Cumulative Submissions Over Time (Brisbane Time)")
plt.xlabel("Datetime")
plt.ylabel("Total Submissions")

# --- Custom legend ---
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='First Solve (100)', markerfacecolor='green', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Score = 0', markerfacecolor='red', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='0 < Score < 100', markerfacecolor='yellow', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Other', markerfacecolor='gray', markersize=8),
]
plt.legend(handles=legend_elements)

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()



start_time = df_sorted["datetime"].min()
end_time = df_sorted["datetime"].max()

sample_times = pd.date_range(start=start_time, end=end_time, freq="6h")

window_counts = []

for t in sample_times:
    t_start = t - pd.Timedelta(days=7)
    count = ((df_sorted["datetime"] >= t_start) & (df_sorted["datetime"] <= t)).sum()
    window_counts.append(count)

plt.figure(figsize=(10, 5))
plt.plot(sample_times, window_counts, color='blue', linewidth=2)
plt.title("Submission Activity (Rolling 7-Day Window)")
plt.xlabel("Datetime")
plt.ylabel("Submissions in Past 7 Days")
plt.grid(True, linestyle='--', alpha=0.5)

# Set date ticks every 3 months
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3)) # change this number for ticker
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

plt.tight_layout()

plt.show()

problem_counts = Counter(df_sorted["problem_name"])
sorted_problems = sorted(problem_counts.items(), key=lambda x: -x[1])

print("\nSubmission counts per problem:")
for name, count in sorted_problems:
    print(f"{name}: {count}")
