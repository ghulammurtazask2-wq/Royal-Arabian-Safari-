# Round 2 — WordPress REST API Deep-Dive & Corrections
**Date:** 2026-09-28 (same day as the seed audit, follow-up pass)
**What changed since the seed audit:** WordPress's REST API (`/wp-json/`) turned out to be publicly readable with no login required. That gave direct access to the actual stored page content, the full page/post list (244 published items vs. the 206 the sitemap exposes), and the media library — real data instead of scraped HTML. This pass corrects one finding from the seed audit and adds two new, higher-confidence ones.

**Still true from the seed audit:** no WordPress *write* access exists in this session (no application password / admin login was provided), so nothing on the live site was changed. This pass is still read-only. See §4 for exactly what unlocks write access.

---

## 1. New finding (P0) — 37 live pages are missing from the XML sitemap

The WP REST API lists **244 published pages/posts**. The sitemap the site advertises in `robots.txt` (`sitemap_index.xml` → `page-sitemap.xml` + `post-sitemap.xml`) lists only **206**. Diffing the two turns up **37 URLs that are live, public, and fully built, but simply aren't in the sitemap Google/Bing actually crawl from.**

This isn't a guess — I spot-checked 6 of the 37 directly:
- 5 are confirmed live and indexable (`robots: index, follow`), with full Open Graph/Twitter/geo metadata and substantial content (30–50 minute estimated reading time): `/dubai-city-tour/`, `/abu-dhabi-city-tour/`, `/evening-desert-safari-abu-dhabi/`, `/sheikh-zayed-grand-mosque-tour/`, `/things-to-do-in-dubai/`.
- 1 (`/desert-safari-dubai-price/`) turned out to be a legitimate 301 redirect to `/dubai-desert-safari-price/` — correctly excluded, not a bug.

**Why this matters:** the orphaned set is overwhelmingly the site's "Dubai/Abu Dhabi city tour + attractions" cluster — over 30 pages covering Sheikh Zayed Grand Mosque, Qasr Al Watan, Louvre Abu Dhabi, Ferrari World, Warner Bros World, Al Ain, and general "things to do" guides. **This directly corrects §3's P2 finding in the seed audit**, which said "Dubai City Tour" / "Abu Dhabi City Tour" had no owning page and should be checked before building one. That was wrong — the pages exist, are well-built, and are simply invisible to search engines' primary discovery mechanism.

**Likely cause (not confirmed without admin access):** most of the 37 orphaned pages were last modified between Aug 23 and Sep 27, 2026 — i.e. this looks like a large content cluster built very recently that the sitemap generator hasn't caught up with. The site runs both RankMath (which normally regenerates its sitemap on publish) and LiteSpeed Cache (which commonly caches static/XML output). A stale cached `sitemap.xml` being served by LiteSpeed is the more likely explanation than a RankMath misconfiguration, but this needs a WP-admin check to confirm.

**Fix (needs WordPress admin, not a content edit):**
1. Purge LiteSpeed Cache, specifically the cached sitemap files (or exclude `sitemap*.xml` from full-page cache going forward).
2. In RankMath → Sitemap Settings, trigger a re-save/regeneration.
3. Re-fetch `sitemap_index.xml` and confirm the count reaches ~243 (244 minus the one legitimate redirect, and minus any pages intentionally noindexed).

This is the single highest-value fix currently available on this site: it's a cache/config action, zero content risk, and could bring 30+ already-written, substantial pages into normal search discovery.

---

## 2. New finding (P1) — price mismatch on `/evening-desert-safari-abu-dhabi/`

- **Title tag:** "Evening Desert Safari Abu Dhabi, From AED 50 With Dinner"
- **Meta description:** "...From AED 50 per person..."
- **On-page H1:** "Evening Desert Safari Abu Dhabi From AED 35 per person"

Two different headline prices on the same page. This is exactly the kind of trust/conversion issue the brief calls out — a visitor who clicks through from a AED 50 snippet and lands on a AED 35 headline (or vice versa) has reason to distrust the rest of the page. **I have not guessed which number is correct** — that's a business fact, not something to infer from crawl data. Needs a quick confirmation from whoever owns pricing, then a one-line fix to whichever of the three (title/meta/H1) is wrong.

---

## 3. Correction — the "duplicate content blocks" finding is retracted

The seed audit flagged `/abu-dhabi-desert-safari-tours/` and `/abu-dhabi-desert-safari-prices/` as showing apparent duplicated sections (a "Book this tour" heading twice, two FAQ blocks, etc.), based on TinyFish's *rendered*-HTML extraction of the live page.

Pulling the actual stored content straight from `wp/v2/pages/{id}` and checking it programmatically shows this was a **false positive**:
- `/abu-dhabi-desert-safari-tours/`: 47 H2 headings, all 47 unique.
- `/abu-dhabi-desert-safari-prices/`: 42 H2 headings, all 42 unique.
- Every specific phrase flagged before ("Book this tour", "If we have to cancel, what happens?", the FAQ heading, the packages heading) occurs **exactly once** in the stored content on both pages.

The most likely explanation is that a template/widget element (e.g. a responsive mobile vs. desktop CTA button, or a sticky element) rendered twice in the live DOM but is stored once in the database — a rendering artifact, not a content problem. **No action is needed on these two pages.** This is a good illustration of why this system verifies against ground truth before recommending changes rather than acting on a single crawl signal.

---

## 4. Other data pulled this pass

- **Plugin/theme stack confirmed via REST discovery:** RankMath SEO (with Redirections and a Google-connected Analytics module — `/rankmath/v1/an/*` — meaning if RankMath is linked to GSC/GA4 on the backend, that data may already be sitting inside WordPress even without separate Google API credentials), LiteSpeed Cache, Kadence theme + page-builder blocks, Contact Form 7, a WebP converter. WordPress version 7.1.1/7.1.2 across recently-modified pages.
- **Media alt-text spot-check:** 10 of 50 sampled media items (20%) have empty alt text, including customer-review screenshots and award/certification images (TripAdvisor Traveller's Choice, World Travel Award) — exactly the trust-building images worth having descriptive alt text on. This was a 50-item sample, not exhaustive (P2, logged in `technical_issues.json`).
- **Application Passwords authentication is enabled** on this WordPress install (`wp-json` → `authentication.application-passwords`). This is the standard, scoped way to grant REST API *write* access without sharing the main admin password: a user generates one under **Users → Profile → Application Passwords** in wp-admin (or via `https://www.arabiansafariroyal.com/wp-admin/authorize-application.php`), and shares the resulting username + generated password. With that, I could push the two fixes above directly (regenerating the sitemap likely still needs a plugin-settings click in wp-admin itself, but the price-text fix could go through the REST API).

---

## 5. Updated priority queue (supersedes the seed audit's §6 items 1, 2 and 6)

| # | Priority | Item | Blocked on |
|---|---|---|---|
| 1 | **P0** | Fix the sitemap gap — purge/regenerate so all 37 orphaned pages are discoverable | WordPress admin access |
| 2 | **P1** | Resolve the AED 50 vs AED 35 price mismatch on `/evening-desert-safari-abu-dhabi/` | A pricing decision from the business, then a content edit |
| 3 | P1 | Confirm true owner of "abu dhabi desert safari" head term via GSC (unchanged from seed audit) | GSC access |
| 4 | P2 | Backfill alt text on review/award images first, then the rest of the media library | WordPress edit access |
| 5 | P2 | ~~Decide whether Dubai/Abu Dhabi City Tour need dedicated pages~~ — **closed, no longer applicable**: they already exist, see §1 | n/a |
| ~~2~~ | ~~P1~~ | ~~Content-structure cleanup of the two mega pages~~ — **retracted, no action needed**, see §3 | n/a |

*Data behind this report lives in `seo-db/pages.json` (now sourced from the WP REST API, 244 pages, sitemap-presence flagged per page), `seo-db/technical_issues.json` (new), and `seo-db/cannibalization.json`.*
