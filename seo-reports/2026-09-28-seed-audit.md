# Royal Arabian Safari — Seed SEO Audit
**Date:** 2026-09-28
**Site:** https://www.arabiansafariroyal.com/
**Scope:** Phase 0 (environment discovery) + Phase 1 (initial live-site crawl and structural audit)

---

## 1. Environment discovery — what actually exists

| Source | Status | Notes / required action |
|---|---|---|
| Repository (`royal-arabian-safari-`) | Available | Contains only `daily_report.py` + `.github/workflows/daily-seo-report.yml`. No website source, no CMS, no prior SEO database, no CLAUDE.md. |
| Google Search Console | **Not available in this session** | `daily_report.py` reads GSC via a service account stored in the `GOOGLE_SERVICE_ACCOUNT_JSON` GitHub secret, but that secret is not exposed to this session. **Required action:** either run future audits through the existing GitHub Action, or share equivalent read access with this session. |
| Google Analytics 4 | **Not available** | `GA4_PROPERTY_ID` secret exists but the script never actually calls the GA4 API yet (dead config — see §5). **Required action:** decide whether to wire in a real GA4 call, and share credentials if this session should pull it directly. |
| WordPress CMS | **Not available in this session** | Confirmed by the user to exist, credentials not provided here. All findings below are from a public, read-only crawl — nothing was written back to the site. |
| PageSpeed / Core Web Vitals | Not checked this pass | `daily_report.py` already calls the public PageSpeed API for a per-page score; this session did not independently verify CWV. |
| Backlink data | Not available | No tool/source connected. |
| Competitor SERP data | Not available | No rank-tracking tool connected; would need live SERP fetches per keyword, not done this pass to keep scope bounded. |
| Live site (read-only) | **Available** | Crawled directly via sitemap discovery + on-page fetch. This is the basis for everything below. |

**Bottom line:** this pass is a real, evidence-based *technical + on-page* audit built from the live site. It is not a performance audit (no ranking/traffic/conversion data was available), and no changes were made to the live site.

---

## 2. Site inventory

- `robots.txt` is clean: disallows only `/wp-admin/` (with `admin-ajax.php` allowed), and explicitly **allows** every major AI crawler (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) — a deliberate, sensible choice for AI-search visibility.
- Sitemap index (`sitemap_index.xml`) → `page-sitemap.xml` (202 URLs) + `post-sitemap.xml` (4 URLs) = **206 total indexable URLs**.
- Canonical host is `https://www.arabiansafariroyal.com/` (bare domain redirects to `www`).
- The blog/post sitemap is nearly empty (4 posts) against 202 pages — this is an almost entirely page-driven, programmatic-style commercial site, not a blog-led content strategy.

### URL clusters (by pattern)

| Cluster | Count |
|---|---|
| Abu Dhabi desert safari — commercial/topical | 79 |
| Dubai desert safari — commercial | 26 |
| Other informational | 24 |
| Layover / stopover / transit visa | 13 |
| Airport / taxi / lounge | 13 |
| Activity add-ons (quad biking, camel, falconry, etc.) | 13 |
| Seasonal month variants (`desert-safari-abu-dhabi-{month}`) | 12 |
| Non-safari Abu Dhabi attractions (Heritage Village, Saadiyat, etc.) | 11 |
| Audience/nationality variants (`...-for-{nationality}`) | 9 |
| Utility (contact, about, privacy, terms) | 4 |

---

## 3. On-page sample (10 of 206 URLs crawled in depth)

Sampled: homepage, `/abu-dhabi-desert-safari-tours/`, `/abu-dhabi-desert-safari-prices/`, 3 seasonal-month pages (Sep/Oct/Dec), 3 nationality pages (Saudis/Germans/Indians), `/morning-desert-safari-abu-dhabi/`. Full detail in `seo-db/pages.json`.

**Good news, evidence-based:** the initial hypothesis going in — that a 206-URL, heavily-patterned site (12 month pages, 9 nationality pages) would turn out to be thin/templated/spun content — **did not hold up**. Every sampled variant page had a genuinely distinct angle: real sunset times and named local events per month (e.g. December references the Liwa Festival and National Day specifically), native-language sections and local currency conversion per nationality (German-language blocks + EUR pricing on the Germans page, Hindi/Urdu content + vegetarian/Jain food detail on the Indians page). Titles and meta descriptions are unique per page, not templated. This is a meaningfully above-average on-page content operation for a programmatic-style site.

### Findings

**P1 — No page owns the exact primary keyword "Abu Dhabi Desert Safari"**
There is no `/abu-dhabi-desert-safari/` URL. The closest functional pillar is `/abu-dhabi-desert-safari-tours/`, and the homepage also directly targets the phrase in its H1. Five URLs currently compete for this territory: homepage, `/abu-dhabi-desert-safari-tours/`, `/abu-dhabi-desert-safari-prices/`, `/abu-dhabi-desert-safari-tickets/`, `/abu-dhabi-desert-safari-reviews/`. **Action needed:** pull GSC query data for these five URLs against "abu dhabi desert safari" and its near-variants to see which one Google is actually already choosing, then confirm it as the owner (or fix internal linking/canonicalization to make the intended one win). Do not create a new pillar page before that check — see `seo-db/keyword_url_map.json`.

**P1 — Likely cannibalization / content-duplication inside the two mega pages**
`/abu-dhabi-desert-safari-tours/` and `/abu-dhabi-desert-safari-prices/` are both extremely long (90–100+ H2 sections each) and cover heavily overlapping ground: packages, pricing, FAQs, cancellation policy, booking process. Within a *single page*, several section headings repeat verbatim or near-verbatim — e.g. `/abu-dhabi-desert-safari-tours/` has "Abu Dhabi Desert Safari Packages — Book Direct, Best Price Guaranteed" as a heading twice, "Book this tour" twice, "If we have to cancel, what happens?" twice, and two separate FAQ blocks; `/abu-dhabi-desert-safari-prices/` shows the same pattern. This reads like several content modules were appended over time rather than authored as one coherent page. That's a real risk for both user experience (guests re-reading the same answer) and page weight/Core Web Vitals on mobile. **Action needed:** a structural content-audit pass on these two pages specifically — consolidate duplicate sections, decide what belongs on "tours" vs "prices" — once WordPress access is available. See `seo-db/cannibalization.json` cluster `core-pillar-cluster`.

**P2 — Unverified review-count claim on a nationality page**
`/desert-safari-abu-dhabi-for-indians/`'s meta description states "4.9★ 5,000+ reviews." This is fine as marketing copy but must be a real, checkable number before it's ever used as the basis for `AggregateRating`/review schema — the operating rules for this system explicitly forbid fabricated or unverifiable ratings in structured data. **Action needed:** confirm the figure against an actual review source (Google Business Profile, TripAdvisor, etc.) before any schema work touches it.

**P3 — Minor robots-meta token-order inconsistency**
Sampled pages mix `index, follow, ...` and `follow, index, ...` token order in the robots meta tag. Functionally identical, cosmetically inconsistent — likely just two different page templates/plugin defaults. Not worth a dedicated fix; note for whoever next touches the SEO plugin template.

**P2 — Listed brief topics with no owning page yet**
"Dubai City Tour" and "Abu Dhabi City Tour" (from the related-topics list in the brief) have no dedicated URL in the current 206-page inventory — closest are attraction-specific pages (`/abu-dhabi-itinerary/`, `/dubai-night-tour/`, `/dubai-to-hatta-tour/`). Per the New Page Creation Rule, this is *not* an automatic "go build these pages" — check GSC for existing impressions against these terms first.

---

## 4. Cannibalization clusters flagged for review

Full detail with per-cluster evidence and recommended next step in `seo-db/cannibalization.json`. Summary:

| Cluster | Risk | Recommended action |
|---|---|---|
| Core pillar (`tours`/`prices`/`tickets`/`what-to-expect`/`reviews`/home) | High | Verify via GSC, then differentiate — not merge |
| Booking-policy pages (cancellation/refund/pay-on-arrival/payment-methods) | Medium | Not yet sampled — sample + verify next cycle |
| Safety/trust pages (safety guide/scams/ladies/sandstorm/solo-female) | Low | Likely fine — distinct sub-intents |
| Seasonal months (12 pages) | Low | No action — good differentiation observed |
| Nationality variants (9 pages) | Low | No action — good differentiation observed |

**No merges, redirects, or content removals have been performed or scheduled.** Per this system's approval rules, any of those require explicit sign-off and query-level evidence, neither of which exists yet.

---

## 5. Notes on the existing `daily_report.py` pipeline

Not modified this pass, but worth flagging while it's fresh:
- It fetches `GA4_PROPERTY_ID` from the environment but never calls the GA4 API — the variable is read and unused. Either wire in a real GA4 pull or drop the unused secret.
- It queries GSC once per run for the trailing 7 days only, with no historical comparison (no 1/7/14/28/90-day or YoY comparison as the operating brief calls for), and no persistent storage — every day's data lands in one Sheets cell and is never reconciled with the day before.
- `get_pagespeed()` is defined but never called from `main()` — dead code.
- Broad `except:` clauses swallow errors silently in `get_pagespeed`.

These are candidates for a follow-up hardening pass (extend the script to write structured, comparable data instead of one text blob) — not done in this pass since the user asked for the live-site audit first.

---

## 6. Priority action queue

| # | Priority | Item | Blocked on |
|---|---|---|---|
| 1 | P1 | Confirm true owner of "abu dhabi desert safari" head term via GSC | GSC access |
| 2 | P1 | Content-structure cleanup of `/abu-dhabi-desert-safari-tours/` and `/abu-dhabi-desert-safari-prices/` (remove duplicated sections) | WordPress access |
| 3 | P2 | Verify the "4.9★ 5,000+ reviews" claim before any schema use | Review-source access |
| 4 | P2 | Sample remaining 9/12 month pages + 6/9 nationality pages to confirm differentiation holds | None — can do next cycle |
| 5 | P2 | Sample the booking-policy cluster (4 pages) for overlap | None — can do next cycle |
| 6 | P2 | Decide whether "Dubai City Tour" / "Abu Dhabi City Tour" need dedicated pages, based on GSC impressions | GSC access |
| 7 | P3 | Harden `daily_report.py`: wire up or remove unused GA4 call, add historical comparison, fix silent `except` | None — code-only |
| 8 | P3 | Standardize robots-meta token order across templates | WordPress access |

---

*This is a seed audit (10/206 pages sampled). The persistent data behind it lives in `seo-db/` and is meant to be extended by future sessions, not rebuilt from scratch.*
