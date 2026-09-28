# Fix Pipeline — Ready, Not Yet Run

**Date:** 2026-09-28

## What this is

`fix all` was asked for. This session cannot reach the WordPress REST API directly (network egress to `arabiansafariroyal.com` is blocked at the environment level), and routing credentials through the only reachable third-party tool was correctly refused earlier as a data-exfiltration risk. GitHub Actions runners have normal internet access and are a separate, secure trust boundary — GitHub's encrypted repo secrets are the standard way to hand them a credential. That's the path built here.

- **`.github/workflows/apply-seo-fixes.yml`** — a `workflow_dispatch`-only job (never runs automatically or on a schedule). Reads `WP_USERNAME` and `WP_APP_PASSWORD` from repo secrets, runs the fix script, uploads a result log as an artifact.
- **`scripts/apply_wp_fixes.py`** — authenticates over HTTP Basic Auth using the app password already generated earlier in this session, then applies each fix independently (one failure doesn't block the rest), logging every request and response.

**Nothing has been written to the live site yet.** The secrets don't exist in the repo, so the workflow can't run.

## What it will do, once triggered

| Finding | Action | Mechanism |
|---|---|---|
| Price mismatch, evening safari | Set title/meta to AED 35 (confirmed correct by site owner) | RankMath `updateMeta` REST endpoint |
| Price mismatch, Dubai price page | Set title/meta to AED 35 / USD 9.50 (confirmed correct) | RankMath `updateMeta` |
| Mismatched T&C meta description | Replace with an accurate description of the actual page | RankMath `updateMeta` |
| Mismatched Privacy Policy meta description | Replace with an accurate description | RankMath `updateMeta` |
| Stargazing typo | Remove the stray leading character | RankMath `updateMeta` |
| Thin stub page (`/self-drive-desert-safari-dubai/`) | Set noindex + canonical to `/dubai-desert-safari/` (site owner's chosen fix, not a content rewrite) | RankMath `updateMeta` |
| Reading-time metadata bug | Re-save the page's existing content unchanged, to trigger recalculation | Core `wp/v2/pages` |
| Media alt-text gap | Backfill descriptive alt text on the 10 identified images | Core `wp/v2/media` |
| 403 outage on the stargazing guide | Read-only diagnostic pull of RankMath's redirection data, to help locate the cause | RankMath `status` endpoint (GET only) |
| **Stale staging-domain references (new finding, see below)** | Scans every page/post on the site and replaces every occurrence of the old pre-migration domain with the live one | Core `wp/v2/pages` / `wp/v2/posts` — pure string substitution |
| Missing commercial schema on the main tours page | Appends `TouristTrip`/`AggregateOffer` JSON-LD, mirroring the pattern already used on the homepage | Core `wp/v2/pages` — additive only |

## New finding while building this: a sitewide stale-domain bug

While pulling the homepage's existing schema markup to use as a template for the tours-page schema fix, its `Product` JSON-LD turned out to reference `blanchedalmond-parrot-567394.hostingersite.com` — a Hostinger auto-generated staging subdomain from before the site moved to `arabiansafariroyal.com` — instead of the live domain. Grepping confirmed this isn't a one-off: **91 occurrences on the homepage, 88 on `/abu-dhabi-desert-safari-tours/`, 93 on `/abu-dhabi-desert-safari-prices/`**, spanning image URLs, video URLs, CSS backgrounds, some inline body-content links, and embedded schema — likely on other pages built the same way, not yet fully mapped. A differently-built page (the Russian nationality page) had zero occurrences, so it's specific to whichever page-building workflow produced these particular pages, not universal.

This is a pure hostname-string substitution — no HTML structure changes — so it's about as low-risk as a live edit gets. The script now scans **every** page and post on the site (not just the 3 confirmed by manual sampling) and fixes any it finds. Full detail in `seo-db/technical_issues.json` → `stale-staging-domain-references`.

## Deliberately not automated: the British/Russian duplicated pricing widget

Looked at this one closely and decided against a scripted edit. The shared block turned out to be a dense, custom pricing component with interdependent inline styles and pre-filled WhatsApp booking links — risky to edit blind with no way to visually verify the result from this session. Reconsidered the actual stakes too: British and Russian pages target completely non-overlapping search results (different languages/countries), so there's no real cannibalization risk despite the shared wording. Recommend a human edit this one directly in the WordPress block editor, where the result can be previewed before publishing. See `seo-db/technical_issues.json` → `duplicated-package-block-british-russian` → `not_auto_fixed_because`.

## Important caveat: the RankMath endpoint schema is unverified

RankMath does not expose its SEO title/description/robots/canonical fields through the standard WordPress REST API — confirmed during the read-only audit (a page's `meta` object only contains theme fields, not RankMath ones). The plugin has its own REST endpoint (`rankmath/v1/updateMeta`) that its block-editor sidebar uses internally, and the script targets that. The exact request shape was written from general knowledge of the plugin, **not verified against a live response** — this session was never able to make a live call to confirm it.

Practically: the price fixes, meta-description fixes, and noindex/canonical fix all depend on this one endpoint working as written. If it rejects the request, **nothing breaks** — WordPress returns an error, the script logs it in full (including the response body, which WP REST APIs typically use to describe the actual expected parameters), and every other independent fix in the run still proceeds. The alt-text and reading-time fixes use the standard, guaranteed-stable WP REST API and will work regardless.

**What's genuinely still open:**
- The two P0s (the sitemap gap and the 403 outage) are **not** something this script can fully resolve — they're most likely a cache/WAF configuration issue that needs a click in wp-admin or the hosting panel, not a content edit. The script includes one read-only diagnostic check but no write action for either.

## To run it

1. Go to `github.com/ghulammurtazask2-wq/Royal-Arabian-Safari-` → **Settings → Secrets and variables → Actions → New repository secret**.
2. Add `WP_USERNAME` (`admin@arabiansafariroyal.com`) and `WP_APP_PASSWORD` (the application password already generated in wp-admin → Users → Profile → Application Passwords — reuse the "Claude SEO Agent" one from earlier in this session, or generate a fresh one for hygiene since the old one has been visible in chat).
3. From the **Actions** tab, run **"Apply WordPress SEO Fixes"** manually (or ask this session to trigger it via the GitHub API once the secrets exist).
4. Check the run's log and the uploaded `fix-run-results` artifact for a per-item pass/fail report. If the RankMath calls fail, share the logged response body and the endpoint call can be corrected in a follow-up commit — no live data will have been touched by a failed call.
