import requests
from bs4 import BeautifulSoup
import csv

cookie_input = input("Paste your full 'Cookie:' header from your browser:\n").strip()

cookies = {}
for part in cookie_input.split(";"):
    if "=" in part:
        k, v = part.strip().split("=", 1)
        cookies[k] = v

MAX_PAGE = int(input("Enter max page number to scrape: "))
CSV_FILE = "orac_submissions.csv"

session = requests.Session()
session.cookies.update(cookies)

results = []
for page in range(1, MAX_PAGE + 1):
    url = f"https://orac2.info/hub/allsubs/{page}"
    print(f"Scraping page {page}...")

    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 4:
            continue  # malformed

        time_tag = tds[0].find("time")
        datetime_str = time_tag["datetime"] if time_tag else "N/A"

        problem_tag = tds[1].find("a")
        problem_name = problem_tag.text.strip() if problem_tag else "N/A"

        score = tds[3].find("span")
        score = score.text.strip() if score else "N/A"

        results.append([datetime_str, problem_name, score])

# Write to CSV, I'd use sys.stdin/out here but its a bit freaky deaky with csvs for some reason??
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["datetime", "problem_name", "score"])
    writer.writerows(results)

print(f"Scraped {len(results)} submissions. Data written to '{CSV_FILE}'.")
