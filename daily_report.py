import os
import json
import datetime
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
import google.generativeai as genai
import requests

# ========== CONFIG ==========
SITE_URL = os.environ["SITE_URL"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
GA4_PROPERTY_ID = os.environ["GA4_PROPERTY_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Anomaly threshold: flag a period-over-period drop of this fraction or more
ANOMALY_DROP_THRESHOLD = 0.20

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
def get_search_console_data(days_back, row_limit=50):
    """Pull page-level GSC data for the trailing `days_back` days, ending yesterday."""
    service = build("searchconsole", "v1", credentials=credentials)
    end_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    start_date = (datetime.date.today() - datetime.timedelta(days=days_back)).isoformat()

    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": row_limit,
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "contains",
                "expression": SITE_URL
            }]
        }]
    }

    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    return response.get("rows", [])


def summarize_gsc_rows(rows, limit=30):
    summary = []
    for row in rows[:limit]:
        summary.append({
            "page": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1)
        })
    return summary


def totals(rows):
    clicks = sum(r.get("clicks", 0) for r in rows)
    impressions = sum(r.get("impressions", 0) for r in rows)
    ctr = round((clicks / impressions * 100), 2) if impressions else 0
    avg_position = round(sum(r.get("position", 0) * r.get("impressions", 0) for r in rows) / impressions, 1) if impressions else 0
    return {"clicks": clicks, "impressions": impressions, "ctr": ctr, "avg_position": avg_position}


# ========== 2. GOOGLE ANALYTICS 4 ==========
def get_ga4_summary(days_back):
    """Pull sessions, engaged sessions and key events for the trailing `days_back` days."""
    try:
        client = BetaAnalyticsDataClient(credentials=credentials)
        request = RunReportRequest(
            property=f"properties/{GA4_PROPERTY_ID}",
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="engagedSessions"),
                Metric(name="keyEvents"),
            ],
            date_ranges=[DateRange(start_date=f"{days_back}daysAgo", end_date="yesterday")],
        )
        response = client.run_report(request)
        rows = []
        for row in response.rows:
            rows.append({
                "channel": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "engaged_sessions": int(row.metric_values[1].value),
                "key_events": int(row.metric_values[2].value),
            })
        organic = next((r for r in rows if r["channel"] == "Organic Search"), None)
        return {"by_channel": rows, "organic_search": organic}
    except Exception as exc:
        print(f"WARNING: GA4 fetch failed ({exc}); continuing without GA4 data")
        return {"error": str(exc)}


# ========== 3. PAGE SPEED (top pages) ==========
def get_pagespeed(url):
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": "mobile",
        "category": ["performance", "seo"]
    }
    try:
        r = requests.get(endpoint, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        perf = categories.get("performance", {}).get("score", 0) * 100
        seo = categories.get("seo", {}).get("score", 0) * 100
        return {"performance": round(perf), "seo": round(seo)}
    except requests.RequestException as exc:
        print(f"WARNING: PageSpeed check failed for {url} ({exc})")
        return {"performance": None, "seo": None}


def get_pagespeed_for_top_pages(gsc_summary, top_n=5):
    top_pages = sorted(gsc_summary, key=lambda r: r["clicks"], reverse=True)[:top_n]
    results = []
    for row in top_pages:
        score = get_pagespeed(row["page"])
        results.append({"page": row["page"], **score})
    return results


# ========== 4. ANOMALY DETECTION ==========
def detect_anomalies(totals_7d, totals_28d):
    """Compare the trailing 7-day totals against the trailing-28-day daily average."""
    anomalies = []
    daily_avg_28d_clicks = totals_28d["clicks"] / 28 if totals_28d["clicks"] else 0
    daily_avg_7d_clicks = totals_7d["clicks"] / 7 if totals_7d["clicks"] else 0
    if daily_avg_28d_clicks > 0:
        drop = 1 - (daily_avg_7d_clicks / daily_avg_28d_clicks)
        if drop >= ANOMALY_DROP_THRESHOLD:
            anomalies.append(
                f"Clicks/day over the last 7 days ({daily_avg_7d_clicks:.1f}) are down "
                f"{drop*100:.0f}% vs the 28-day daily average ({daily_avg_28d_clicks:.1f})."
            )
    if totals_7d["avg_position"] and totals_28d["avg_position"]:
        if totals_7d["avg_position"] - totals_28d["avg_position"] >= 3:
            anomalies.append(
                f"Average position over 7 days ({totals_7d['avg_position']}) is "
                f"{totals_7d['avg_position'] - totals_28d['avg_position']:.1f} places worse than the 28-day average "
                f"({totals_28d['avg_position']})."
            )
    return anomalies


# ========== 5. GEMINI ANALYSIS ==========
def analyze_with_gemini(gsc_data_7d, totals_7d, totals_28d, anomalies, ga4_summary):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an expert SEO and website growth analyst.

Analyze the following Google Search Console data for the website {SITE_URL}.

7-day page-level data:
{json.dumps(gsc_data_7d, indent=2)}

7-day totals: {json.dumps(totals_7d)}
28-day totals: {json.dumps(totals_28d)}
Anomalies detected (period-over-period): {json.dumps(anomalies) if anomalies else "none"}
GA4 summary (sessions/engaged sessions/key events by channel, trailing 7 days): {json.dumps(ga4_summary)}

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
   - Give honest reasons based on the data, referencing the 7-day vs 28-day comparison and any anomalies above

5. Quick Wins (things that can be fixed fast on WordPress)

Write in simple English. Be direct and practical.
"""

    response = model.generate_content(prompt)
    return response.text


# ========== 6. WRITE TO GOOGLE SHEETS ==========
def write_to_sheets(report_text, gsc_summary, totals_7d, totals_28d, anomalies, ga4_summary, pagespeed_results):
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)

    try:
        worksheet = sh.worksheet("Daily Reports")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title="Daily Reports", rows=1000, cols=12)
        worksheet.append_row([
            "Date", "Clicks (7d)", "Impressions (7d)", "CTR % (7d)", "Avg Position (7d)",
            "Clicks (28d)", "Impressions (28d)", "Avg Position (28d)",
            "Anomalies", "GA4 Organic Sessions (7d)", "AI Report", "Top Pages JSON"
        ])

    today = datetime.date.today().isoformat()
    organic = (ga4_summary or {}).get("organic_search") or {}

    worksheet.append_row([
        today,
        totals_7d["clicks"], totals_7d["impressions"], totals_7d["ctr"], totals_7d["avg_position"],
        totals_28d["clicks"], totals_28d["impressions"], totals_28d["avg_position"],
        " | ".join(anomalies) if anomalies else "none",
        organic.get("sessions", "n/a"),
        report_text[:50000],
        json.dumps({"pages": gsc_summary, "pagespeed": pagespeed_results})[:30000],
    ])


# ========== MAIN ==========
def main():
    print("Starting daily report...")

    rows_7d = get_search_console_data(days_back=7)
    rows_28d = get_search_console_data(days_back=28, row_limit=200)
    print(f"Fetched {len(rows_7d)} pages (7d) and {len(rows_28d)} pages (28d) from Search Console")

    gsc_summary_7d = summarize_gsc_rows(rows_7d)
    totals_7d = totals(rows_7d)
    totals_28d = totals(rows_28d)

    anomalies = detect_anomalies(totals_7d, totals_28d)
    if anomalies:
        print("ANOMALIES DETECTED:")
        for a in anomalies:
            print(" -", a)

    ga4_summary = get_ga4_summary(days_back=7)

    pagespeed_results = get_pagespeed_for_top_pages(gsc_summary_7d, top_n=5)
    print(f"Checked PageSpeed for {len(pagespeed_results)} top pages")

    report = analyze_with_gemini(gsc_summary_7d, totals_7d, totals_28d, anomalies, ga4_summary)
    print("AI analysis completed")

    write_to_sheets(report, gsc_summary_7d, totals_7d, totals_28d, anomalies, ga4_summary, pagespeed_results)
    print("Report written to Google Sheets")
    print("Done.")


if __name__ == "__main__":
    main()
