# SEO Audit: arabiansafariroyal.com

**Overall Health Score: 6.5/10** *(computed across 4 of 5 layers — Link Profile is unscored, not assumed; see below)*

## Executive Summary

The site's biggest strength is content quality: this is a large (244-page), genuinely well-differentiated WordPress operation with unusually strong E-E-A-T for a site this size — real operational specifics (exact prices, pickup logistics, cancellation policy), native-language sections for international visitors, and an explicit "we audited every price page ranking above us" competitor-transparency angle that's rare outside enterprise content teams. The most critical issue is technical, not content: **37 of 244 published pages (15%) are missing from the XML sitemap**, including nearly the entire Dubai/Abu Dhabi "city tours and attractions" vertical (Ferrari World, Warner Bros World, Louvre Abu Dhabi, Qasr Al Watan, multiple city-tour pages). **Update after checking internal linking:** this cluster is not actually a dead end — it's densely interlinked and reachable from the homepage within 3 hops (homepage → `/abu-dhabi-city-tour/` or `/dubai-city-tour/` → `/things-to-do-in-abu-dhabi/` / `/things-to-do-in-dubai/` → 20+ of the remaining orphaned pages), so a crawler following links would still find essentially the whole cluster. The accurate framing is: these pages are crawlable via internal links but missing the sitemap's discovery-priority and freshness signal, and missing from Search Console's submitted/indexed coverage reporting (which is sitemap-driven) — still a real, cheap, worth-fixing issue, just not literally invisible to Google as first framed. The highest-impact opportunity is still fixing that gap: it's a config/cache issue, not a content rewrite. Separately, a live SERP check shows the site is not currently visible in the top results for the exact head term "abu dhabi desert safari," which is dominated by TripAdvisor, Etihad, GetYourGuide and the official Visit Abu Dhabi tourism site — high-authority generalist/OTA players this site will need a different strategy to compete against than pure content depth alone.

**Veto conditions checked:** none fire based on available evidence. `robots.txt` explicitly allows Googlebot and all major crawlers (verified). 0 of 55+ sampled pages were noindexed, well under the 20% cap (verified). HTTPS is enforced with proper www canonicalization (verified). Core Web Vitals and Google Manual Action status could **not** be checked — no PageSpeed API quota was available in this session (daily quota already exhausted on this environment's shared allocation) and no Search Console access exists. These are flagged as **unknown**, not cleared.

## Layer Scores

| Layer | Score | Top Issue |
|---|---|---|
| Technical Foundation | 6/10 | 37 live pages (15% of the site) missing from the XML sitemap |
| On-Page Optimization | 7/10 | Missing commercial schema (Offer/TouristTrip) on money pages; one confirmed price mismatch |
| Content Quality | 8/10 | Strong E-E-A-T and differentiation; standout strength |
| Link Profile | **N/A — no data** | No backlink data source available in this session |
| Competitive Position | 4/10 | Not visible in a live top-9 SERP check for the primary head term |

## Critical Issues (fix immediately)

| Issue | Layer | Affected Pages | Impact | Fix |
|---|---|---|---|---|
| 37 live, indexable pages missing from XML sitemap (reachable via internal links, not a true dead end — see refinement below) | Technical | ~15% of site (city-tour/attractions cluster) | Medium-high — slower/less reliable discovery than sitemap-listed pages, and invisible to GSC's sitemap-driven coverage reporting | Purge LiteSpeed Cache on sitemap XML, trigger RankMath sitemap regeneration, re-verify count reaches ~243 |
| Price mismatch: title/meta price ≠ on-page H1 price — CONFIRMED ON 2 INDEPENDENT PAGES | On-Page | `/evening-desert-safari-abu-dhabi/` (AED 50 vs AED 35), `/dubai-desert-safari-price/` (USD 14 vs AED 35) | Medium-high — direct trust/conversion risk, and two occurrences suggest a systemic cause (e.g. SEO title field not updated alongside page content) rather than two typos | Confirm correct prices with the business, align title/meta/H1 on both; spot-check other money pages for the same drift |
| A fully-indexed commercial page has almost no content | On-Page/Content | `/self-drive-desert-safari-dubai/` (~50 words vs 14-64 min reads elsewhere; its Abu Dhabi counterpart is fully built) | Medium — reads as thin/doorway content to Google despite the site's otherwise strong depth | Build it out to match its Abu Dhabi sibling, or noindex + canonical it to the main Dubai safari page if it's meant to stay a short disambiguation note |
| No visible top-result presence for "abu dhabi desert safari" | Competitive | Site-wide (head term) | High (strategic) | Confirm true page-ownership via GSC once available (see keyword_url_map.json), then focus internal linking/authority on that one URL rather than splitting signal across 5 |

## High-Priority Improvements (fix this month)

| Improvement | Layer | Effort | Expected Impact |
|---|---|---|---|
| Add `Offer`/`TouristTrip` (or `Product`) schema consistently across all money pages (currently only spot-confirmed on homepage) | On-Page | Low-Medium | Enables price-in-SERP rich results, matching what GetYourGuide/TripAdvisor already show |
| Backfill alt text on review/award trust images (20% missing in a 50-image sample) | On-Page | Low | Accessibility + image-search visibility on exactly the images meant to build trust |
| Verify sitewide `Organization`/`LocalBusiness` schema exists in the theme head (only post-content schema was checked this pass, not the full rendered `<head>`) | On-Page | Low (verification only) | Confirms/fixes entity signals Google uses for brand recognition |
| Differentiate the shared "Standard/Premium/VIP Royal" package module duplicated between `/desert-safari-abu-dhabi-for-british-tourists/` and `/desert-safari-abu-dhabi-for-russians/` (verified against raw content, not a false positive) | Content | Low | Brings these 2 pages up to the same differentiation standard as the other 7 nationality pages |
| Resolve the core-pillar cluster's actual ranking owner (tours/prices/tickets/reviews/what-to-expect) once GSC access exists | Content/Competitive | Medium | Concentrates ranking signal instead of splitting it 5 ways |

## Opportunities (plan for next quarter)

| Opportunity | Layer | Description |
|---|---|---|
| Backlink audit and acquisition plan | Link Profile | Currently zero visibility into referring domains — needs a backlink data source (Ahrefs/Moz/Semrush/GSC Links report) before this layer can be scored or planned at all |
| Formal competitor content-gap analysis | Competitive | This pass identified *who* ranks (TripAdvisor, Etihad, GetYourGuide, VisitAbuDhabi, plus 3-4 smaller dedicated operators) but did not scrape their content depth/structure for a gap analysis |
| Core Web Vitals baseline | Technical | Needs either a PageSpeed API key (this session's shared quota is exhausted) or Search Console Core Web Vitals report access |

## Detailed Findings

### Layer 1: Technical Foundation — 6/10

**Crawlability:** `robots.txt` is clean — disallows only `/wp-admin/` (with `admin-ajax.php` explicitly allowed), and explicitly allows every major crawler including AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended). Sitemap directive present and correctly points to `sitemap_index.xml`. **However**, the sitemap itself is incomplete: WordPress's own REST API confirms 244 published pages/posts exist, while the sitemap lists only 206-207. All 38 orphaned URLs were individually checked; 37 are confirmed live and indexable (not noindexed, not redirects), 1 is a legitimate redirect correctly excluded. This is the single largest technical issue on the site. Root cause not confirmed without server access, but the pattern (most orphaned pages modified within the last 5 weeks, LiteSpeed Cache installed alongside RankMath) points to a stale cached sitemap rather than a RankMath misconfiguration.

**Internal-link follow-up on the sitemap gap:** checked whether the 37 orphaned pages are also unreachable via internal links (which would make them true dead ends) or just missing from the sitemap. They are not dead ends — the homepage links directly to 2 of them (`/abu-dhabi-city-tour/`, `/dubai-city-tour/`), and those two link onward to `/things-to-do-in-abu-dhabi/` and `/things-to-do-in-dubai/`, which between them link to 20+ of the remaining orphans (Ferrari World, Louvre Abu Dhabi, Qasr Al Watan, SeaWorld, Al Ain, city-tour price variants). A crawler following links from the homepage would reach essentially the whole cluster within 3 hops. This is a meaningful correction to the initial framing: the issue is a missing discovery-priority/freshness signal and a GSC-reporting blind spot, not total invisibility.

A full orphan-page and redirect-chain check across all 244 pages' link graphs was not performed at full-site scale this pass — flagged as a coverage gap, not a finding either way.

**Indexability:** Every sampled page (55 of 244) carries `robots: index, follow` with a self-referencing canonical. No accidental noindex found. The bare domain correctly redirects to `https://www.` — single canonical host confirmed, no www/non-www duplicate-content risk observed.

**Performance:** Not measurable this session — the PageSpeed Insights API's unauthenticated daily quota was already exhausted on this environment's shared allocation before this audit could pull data, and no Search Console CWV report access exists. **This is a real gap in this audit, not a clean bill of health** — recommend re-running once either a PSI API key or GSC access is available.

**Rendering:** Content is served as standard server-rendered WordPress HTML (Kadence theme/blocks) rather than a client-side-rendered app, which is low-risk for crawlability by default, but this wasn't independently verified against a JS-disabled fetch.

### Layer 2: On-Page Optimization — 7/10

Across 55 sampled pages: titles and meta descriptions are unique, compelling, and reasonably sized per page (not templated). Single H1 confirmed on every page checked, with logical H2/H3 hierarchy. URLs are clean and hyphenated throughout.

**Structured data:** the homepage carries `WebPage`, `FAQPage`, and `Product` JSON-LD. `/abu-dhabi-desert-safari-tours/` carries `WebPage` and `FAQPage` only — no `Offer`/`TouristTrip`/`Product` schema despite being the site's primary money page with explicit per-package pricing. This is a real, fixable gap: competitors visible in the SERP check (GetYourGuide, TripAdvisor) show "Verified Reviews" and rich snippet treatment that schema-eligible pages can compete for. Sitewide `Organization`/`LocalBusiness` schema (typically injected in the theme `<head>`, not post content) was **not verified** this pass — the check only covered the post-content field via the REST API, not the fully rendered page head.

**Confirmed defect:** `/evening-desert-safari-abu-dhabi/` shows "AED 50" in title/meta and "AED 35" in the on-page H1 — see technical_issues.json.

**Images:** 10 of 50 sampled media items (20%) have empty alt text, including customer-review screenshots and award/certification badges — exactly the trust-signal images worth prioritizing.

**Internal linking:** not audited at full-site scale this pass (would need the complete internal link graph across 244 pages) — flagged as a coverage gap.

### Layer 3: Content Quality — 8/10

This is the site's clearest strength. E-E-A-T signals are genuinely strong and specific, not generic: real pickup logistics, a published four-level complaint-escalation process, a cash-vs-card payment logistics page, native-language content blocks (German, Hindi/Urdu) with local currency conversion for international-visitor pages, and a "we audited every price page ranking above us" competitor-transparency section on the pricing page. WhatsApp message screenshots are used as evidence rather than typed testimonials.

Three large content clusters were checked specifically for thinness/duplication risk and all came back genuinely differentiated: the 12 seasonal-month pages (real sunset times, named local events per month), the 9 nationality-variant pages (native-language sections, culturally specific content), and the 4-page booking-policy cluster (cancellation/pay-on-arrival/refund/payment, each with a distinct angle). The 5-page "core pillar" cluster (tours/prices/tickets/reviews/what-to-expect) also resolved to distinct angles on inspection rather than duplication, though which one Google actually favors for the bare head term still needs GSC verification.

No formal content-gap analysis against competitor pages was done this pass (see Opportunities).

### Layer 4: Link Profile — unscored (no data)

No backlink data source (Ahrefs, Moz, Semrush, or a GSC Links report) was available in this session. Per this audit's own rules, this is reported as missing data, not assumed to be zero or scored by default — doing so would violate the "don't invent data" constraint this system operates under. **This is the single largest blind spot in the current audit** and should be the first data source added.

### Layer 5: Competitive Position — 4/10

A live search for "abu dhabi desert safari" (single snapshot, AE-localized, 2026-09-28) returned: abudhabideserttour.com, TripAdvisor, Etihad.com, GetYourGuide, the official Visit Abu Dhabi tourism site, Facebook, eatours.ae, abudhabi-desert-safari.com, and abudhabiadventuresafari.com in the top 9 — **arabiansafariroyal.com did not appear**. This is directional, not exhaustive rank tracking (no device/personalization control, single snapshot), but it's a real, current signal. The competitive set splits into two types: massive-authority generalist/OTA sites (TripAdvisor, GetYourGuide, Etihad, government tourism site) that compete on domain authority rather than content depth, and several smaller dedicated operator sites more directly comparable to this one. This site's per-page content depth (6,000-17,000 words on core commercial pages) is a genuine differentiator against the smaller operators, but competing with the OTA/authority sites for the bare head term will likely need backlink/authority work this audit can't currently measure (see Layer 4).

---

## 90-Day Action Plan

**Month 1: Fix the foundation**
- Purge sitemap cache / trigger RankMath sitemap regeneration to close the 37-page gap (needs WordPress admin access)
- Fix the AED 35/AED 50 price mismatch on the evening safari page
- Get a working Core Web Vitals baseline (PSI API key or GSC access)
- Verify sitewide Organization/LocalBusiness schema in the theme head

**Month 2: Strengthen content**
- Add Offer/TouristTrip schema to all money pages, starting with the 5-page core-pillar cluster
- Backfill alt text on trust-signal images (reviews, awards) first, then the rest of the media library
- Once GSC access exists: resolve which core-pillar page should be the head-term owner and adjust internal linking to concentrate signal on it

**Month 3: Build authority**
- Stand up a backlink data source and run a real Link Profile audit (currently the biggest blind spot)
- Run a formal content-gap analysis against the 4-5 directly comparable competitor operators identified in this pass
- Revisit the competitive SERP check with proper rank-tracking (not a single snapshot) to measure movement

---

*This audit builds on `seo-db/pages.json`, `technical_issues.json`, `cannibalization.json`, and `keyword_url_map.json` in this repo. Data sources used: live site crawl via public WordPress REST API + web fetch, one live SERP snapshot. Not used (unavailable this session): Google Search Console, Google Analytics 4, PageSpeed Insights (quota exhausted), any backlink data source.*
