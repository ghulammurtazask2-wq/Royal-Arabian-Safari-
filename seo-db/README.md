# SEO Database (seed)

Persistent data layer for the Royal Arabian Safari / arabiansafariroyal.com SEO system, per the environment-discovery and master-URL-database phases of the operating brief. This is a **seed** — the first crawl only, not a complete system. Future sessions should extend it rather than replace it.

## Files

- `pages.json` — Full inventory of all **244 published WordPress pages/posts**, pulled directly from the public WP REST API (`wp-json/wp/v2/pages`, `/posts`) and cross-referenced against the XML sitemap. Each entry records `in_sitemap: true/false` — 38 are currently `false` (see `technical_issues.json`). 16 pages have full on-page sampling; the rest are `crawl_status: "not_yet_sampled"`.
- `keyword_url_map.json` — Keyword → preferred-URL hypotheses for the primary topic and related terms from the brief. Marked as **structural hypotheses**, not confirmed — this site has no GSC/GA4 access wired into this session, so nothing here should be treated as verified until checked against real query data.
- `cannibalization.json` — Candidate URL clusters that may compete for the same search intent, with a risk level and recommended next step per cluster. No MERGE/REDIRECT has been recommended or performed anywhere in this seed — see each cluster's `requires_approval_for`.
- `technical_issues.json` — Concrete, evidence-verified technical/content bugs found via the WP REST API: a 37-page sitemap gap (P0), a price mismatch on one page (P1), a media alt-text gap (P2), and one earlier finding (duplicate content blocks) that was checked against raw stored content and retracted as a false positive. See `seo-reports/2026-09-28-round2-wordpress-rest-api.md` for full detail.

## What's missing (and why nothing has been written back to the live site)

This repository (`ghulammurtazask2-wq/royal-arabian-safari-`) contains only a GitHub Action (`daily-seo-report.yml`) and one script (`daily_report.py`) that pulls 7-day GSC data through a service account and posts a Gemini-written summary to Google Sheets. It does **not** contain:

- The website's source/theme code (site is WordPress, hosted elsewhere)
- Working GSC/GA4/PageSpeed credentials accessible to this session (the pipeline's secrets live in GitHub Actions, not exposed here)
- WordPress **write** credentials — the WP REST API's public **read** endpoints (`wp/v2/pages`, `/posts`, `/media`, plus discovery of the full route list at `/wp-json/`) turned out to be openly accessible with no login, which is how all the data in this directory was gathered. Writes require authentication the site does support (see below) but that hasn't been provided to this session.
- Backlink or competitor-rank tooling

Everything in this directory was built read-only: sitemap discovery, WP REST API reads, and a 16-page on-page sample. No page content was changed and no write requests were sent to the CMS.

## Next steps to unlock the rest of the system

1. **Grant WordPress write access.** This install has Application Passwords authentication enabled (`wp-json` → `authentication.application-passwords`, authorization URL `https://www.arabiansafariroyal.com/wp-admin/authorize-application.php`). A user with edit rights generates one under **Users → Profile → Application Passwords** in wp-admin and shares the resulting username + generated password. That unlocks direct fixes via `wp/v2/pages/{id}` (title/content/meta) without sharing the main admin login. Note: the sitemap-cache fix (top P0 item) likely still needs a wp-admin UI click (RankMath settings / LiteSpeed Cache purge) rather than a REST write.
2. Provide GSC/GA4 API access (or point this session at the existing service-account credentials) so query-level ranking/CTR data can replace the structural guesses in `keyword_url_map.json` and `cannibalization.json`. Note: RankMath's Analytics module (`/rankmath/v1/an/*`) may already have GSC/GA4 connected inside WordPress itself — worth checking before setting up a separate credential.
3. Expand `pages.json` sampling from 16/244 to the full set — this is naturally a multi-session job; each cycle should sample another batch rather than re-fetching everything at once.
