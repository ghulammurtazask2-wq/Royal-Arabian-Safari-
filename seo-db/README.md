# SEO Database

Persistent data layer for the Royal Arabian Safari / arabiansafariroyal.com SEO system, per the environment-discovery and master-URL-database phases of the operating brief.

**Status: full-site audit complete.** All 244 pages/posts have been sampled and checked against actual stored WordPress content. See `seo-reports/2026-09-28-audit-complete-summary.md` for the consolidated findings list. This remains a living database, not a one-time snapshot — future sessions should extend and re-verify it (especially once GSC/GA4/backlink access exists), not treat it as finished forever.

## Files

- `pages.json` — Full inventory of all **244 published WordPress pages/posts**, pulled directly from the public WP REST API (`wp-json/wp/v2/pages`, `/posts`) and cross-referenced against the XML sitemap. Each entry records `in_sitemap: true/false` — 38 are currently `false` (see `technical_issues.json`). **All 244 pages now have `crawl_status: sampled_*` with a per-page `notes` field.**
- `keyword_url_map.json` — Keyword → preferred-URL hypotheses for the primary topic and related terms from the brief. Marked as **structural hypotheses**, not confirmed — this site has no GSC/GA4 access wired into this session, so nothing here should be treated as verified until checked against real query data.
- `cannibalization.json` — Candidate URL clusters that may compete for the same search intent, with a risk level and recommended next step per cluster. Every cluster (core-pillar, booking-policy, safety, seasonal-month x12, nationality x9) has now been fully sampled, not just spot-checked. No MERGE/REDIRECT has been recommended or performed anywhere — see each cluster's `requires_approval_for`.
- `technical_issues.json` — **13 tracked findings**, most-severe first: 2 P0 (a live 403 outage on a real page, and the 37-page sitemap gap), 4 P1 (price mismatches confirmed on 2 pages, a thin stub page, mismatched utility-page meta descriptions, no SERP visibility for the head term), 4 P2 (missing commercial schema, an unverified rating claim, a duplicated content module between 2 nationality pages, a media alt-text gap), 2 low-priority cosmetic items, and 1 explicitly retracted false-positive kept in the record as a correction.

## What's missing (and why nothing has been written back to the live site)

This repository (`ghulammurtazask2-wq/royal-arabian-safari-`) contains only a GitHub Action (`daily-seo-report.yml`) and one script (`daily_report.py`) that pulls 7-day GSC data through a service account and posts a Gemini-written summary to Google Sheets. It does **not** contain:

- The website's source/theme code (site is WordPress, hosted elsewhere)
- Working GSC/GA4/PageSpeed credentials accessible to this session (the pipeline's secrets live in GitHub Actions, not exposed here)
- WordPress **write** credentials — the WP REST API's public **read** endpoints (`wp/v2/pages`, `/posts`, `/media`, plus discovery of the full route list at `/wp-json/`) turned out to be openly accessible with no login, which is how all the data in this directory was gathered. Writes require authentication the site does support (see below) but that hasn't been provided to this session.
- Backlink or competitor-rank tooling

Everything in this directory was built read-only: sitemap discovery, WP REST API reads, and now a full 244/244-page on-page sample. No page content was changed and no write requests were sent to the CMS. An attempt to authenticate for writes (an Application Password was generated and shared) was blocked by a security check when the only reachable path routed credentials through a third-party web-fetch tool — direct network egress to the site is not available from this session, and that block was not worked around, per this system's own risk-handling rules.

## Next steps to unlock the rest of the system

1. **Widen this session's (or a future session's) network egress** to `arabiansafariroyal.com`, so WordPress REST API writes can be made directly (credentials never leaving the session) rather than routed through a third-party tool. This is the blocker on actually fixing any of the 13 tracked issues from here.
2. Provide GSC/GA4 API access (or point this session at the existing service-account credentials) so query-level ranking/CTR data can replace the structural guesses in `keyword_url_map.json` and `cannibalization.json`. Note: RankMath's Analytics module (`/rankmath/v1/an/*`) may already have GSC/GA4 connected inside WordPress itself — worth checking before setting up a separate credential.
3. Once either of the above exists, work the priority queue in `seo-reports/2026-09-28-audit-complete-summary.md` top to bottom, starting with the two P0s (both are config/cache fixes, not content rewrites).
