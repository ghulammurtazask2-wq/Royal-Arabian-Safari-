import os
import json
import datetime
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
import google.generativeai as genai
import requests

# ========== CONFIG ==========
SITE_URL = os.environ["SITE_URL"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
GA4_PROPERTY_ID = os.environ["GA4_PROPERTY_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Load service account
sa_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
credentials = service_account.Credentials.from_service_account_info(
    sa_info,
    scopes=[
        "https://www.googleapis.com/auth/webmasters.readonly",
        "https://www.googleapis.com/auth/analytics.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

# ========== 1. GOOGLE SEARCH CONSOLE DATA ==========
def get_search_console_data():
    service = build("searchconsole", "v1", credentials=credentials)
    end_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    start_date = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()

    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": 50,
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "contains",
                "expression": SITE_URL
            }]
        }]
    }

    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    rows = response.get("rows", [])
    return rows

# ========== 2. PAGE SPEED (top pages) ==========
def get_pagespeed(url):
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": "mobile",
        "category": ["performance", "seo"]
    }
    try:
        r = requests.get(endpoint, params=params, timeout=30)
        data = r.json()
        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        perf = categories.get("performance", {}).get("score", 0) * 100
        seo = categories.get("seo", {}).get("score", 0) * 100
        return {"performance": round(perf), "seo": round(seo)}
    except:
        return {"performance": None, "seo": None}

# ========== 3. GEMINI ANALYSIS ==========
def analyze_with_gemini(gsc_data):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an expert SEO and website growth analyst.

Analyze the following Google Search Console data for the website {SITE_URL} (last 7 days).

Data:
{json.dumps(gsc_data, indent=2)}

Provide a clear daily report in this exact structure:

1. Top 5 Underperforming Pages
   - Page URL
   - Impressions / Clicks / CTR / Position
   - Main problem
   - Exact recommended action

2. Biggest Opportunities
   - Pages with high impressions but low CTR
   - Pages with good position but low clicks

3. Priority Action List for Today (maximum 7 items)
   - Be specific and actionable

4. Why the site may not be improving daily
   - Give honest reasons based on the data

5. Quick Wins (things that can be fixed fast on WordPress)

Write in simple English. Be direct and practical.
"""

    response = model.generate_content(prompt)
    return response.text

# ========== 4. WRITE TO GOOGLE SHEETS ==========
def write_to_sheets(report_text, gsc_summary):
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)

    # Create or get worksheet
    try:
        worksheet = sh.worksheet("Daily Reports")
    except:
        worksheet = sh.add_worksheet(title="Daily Reports", rows=1000, cols=10)

    today = datetime.date.today().isoformat()

    # Append new row
    worksheet.append_row([
        today,
        report_text[:50000],  # Sheets cell limit protection
        json.dumps(gsc_summary)[:30000]
    ])

# ========== MAIN ==========
def main():
    print("Starting daily report...")

    gsc_data = get_search_console_data()
    print(f"Fetched {len(gsc_data)} pages from Search Console")

    # Prepare clean summary for AI
    clean_data = []
    for row in gsc_data[:30]:
        clean_data.append({
            "page": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1)
        })

    report = analyze_with_gemini(clean_data)
    print("AI analysis completed")

    write_to_sheets(report, clean_data)
    print("Report written to Google Sheets")
    print("Done.")

if __name__ == "__main__":
    main()
