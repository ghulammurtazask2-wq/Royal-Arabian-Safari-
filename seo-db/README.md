# SEO Database (seed)

Persistent data layer for the Royal Arabian Safari / arabiansafariroyal.com SEO system, per the environment-discovery and master-URL-database phases of the operating brief. This is a **seed** — the first crawl only, not a complete system. Future sessions should extend it rather than replace it.

## Files

- `pages.json` — Full 206-URL inventory pulled from `page-sitemap.xml` + `post-sitemap.xml`, clustered by topic/pattern. 10 pages have full on-page sampling (title, meta description, canonical, robots meta, notes); the rest are `crawl_status: "not_yet_sampled"`.
- `keyword_url_map.json` — Keyword → preferred-URL hypotheses for the primary topic and related terms from the brief. Marked as **structural hypotheses**, not confirmed — this site has no GSC/GA4 access wired into this session, so nothing here should be treated as verified until checked against real query data.
- `cannibalization.json` — Candidate URL clusters that may compete for the same search intent, with a risk level and recommended next step per cluster. No MERGE/REDIRECT has been recommended or performed anywhere in this seed — see each cluster's `requires_approval_for`.

## What's missing (and why nothing beyond audit/reporting has been done)

This repository (`ghulammurtazask2-wq/royal-arabian-safari-`) contains only a GitHub Action (`daily-seo-report.yml`) and one script (`daily_report.py`) that pulls 7-day GSC data through a service account and posts a Gemini-written summary to Google Sheets. It does **not** contain:

- The website's source/theme code (site is WordPress, hosted elsewhere)
- Working GSC/GA4/PageSpeed credentials accessible to this session (the pipeline's secrets live in GitHub Actions, not exposed here)
- WordPress admin or REST API credentials (confirmed to exist, but not provided to this session)
- Backlink or competitor-rank tooling

Everything in this directory was built from a live, read-only crawl of `https://www.arabiansafariroyal.com/` (sitemaps + a 10-page on-page sample) via web fetch tools. No page content was changed and no requests were sent to the CMS.

## Next steps to unlock the rest of the system

1. Provide GSC/GA4 API access (or point this session at the existing service-account credentials) so query-level ranking/CTR data can replace the structural guesses in `keyword_url_map.json` and `cannibalization.json`.
2. Provide WordPress edit access (admin or REST API + app password, ideally as a scoped credential) if on-page fixes (titles, meta, schema, internal links) should be applied directly rather than only recommended.
3. Expand `pages.json` sampling from 10/206 to the full set — this is naturally a multi-session job; each cycle should sample another batch rather than re-fetching everything at once.
