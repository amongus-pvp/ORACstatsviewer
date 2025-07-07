import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from zoneinfo import ZoneInfo
import numpy as np

df = pd.read_csv("orac_submissions.csv")

df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
df["datetime"] = df["datetime"].dt.tz_convert(ZoneInfo("Australia/Brisbane")) # replace this with your country/city

df["score"] = pd.to_numeric(df["score"], errors="coerce")

df_sorted = df.sort_values("datetime").reset_index(drop=True)

df_sorted["cumulative"] = range(1, len(df_sorted) + 1)

solved_set = set()
solved_times = []
solved_counts = []

for i, row in df_sorted.iterrows():
    pname = row["problem_name"]
    score = row["score"]
    if score == 100 and pname not in solved_set:
        solved_set.add(pname)
        solved_times.append(row["datetime"])
        solved_counts.append(row["cumulative"])

plt.figure(figsize=(10, 5))
plt.plot(df_sorted["datetime"], df_sorted["cumulative"], linestyle='-', marker='o', markersize=3, color='gray', label='All Submissions')
plt.scatter(solved_times, solved_counts, color='green', label='Problem Solved (100)', zorder=5)

plt.title("Cumulative Submissions Over Time")
plt.xlabel("Datetime")
plt.ylabel("Total Submissions")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

df_sorted["hour"] = df_sorted["datetime"].dt.hour
min_hour = max(0, df_sorted["hour"].min() - 1)
max_hour = min(23, df_sorted["hour"].max() + 1)

plt.figure(figsize=(10, 5))
plt.hist(df_sorted["hour"], bins=range(min_hour, max_hour + 2), edgecolor='black', align='left')
plt.title("Histogram of Submissions by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Submissions")
plt.xticks(range(min_hour, max_hour + 1))
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
plt.tight_layout()

plt.show()

problem_counts = Counter(df_sorted["problem_name"])
sorted_problems = sorted(problem_counts.items(), key=lambda x: -x[1])

print("\nSubmission counts per problem:")
for name, count in sorted_problems:
    print(f"{name}: {count}")
