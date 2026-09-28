"""
Applies the fixes tracked in seo-db/technical_issues.json to the live
WordPress site via its REST API.

Runs from GitHub Actions (workflow_dispatch), authenticated with
WP_USERNAME / WP_APP_PASSWORD repo secrets over HTTP Basic Auth. Never
run this with credentials pasted inline -- it reads them from the
environment only.

Design notes:
- Media alt-text and page-content edits use the core WP REST API
  (wp/v2/...), which is guaranteed stable.
- Title/meta-description/robots/canonical edits go through RankMath's
  own REST endpoint (rankmath/v1/updateMeta), since RankMath's SEO
  meta fields are NOT exposed as writable fields on the standard
  wp/v2 post objects (confirmed during the read-only audit -- the
  `meta` field on a page only exposes Kadence keys). The exact
  request shape for that endpoint was inferred from RankMath's public
  editor behaviour, not verified against a live response, so every
  call is logged in full (request + response) and failures are
  reported clearly rather than silently swallowed. If the shape is
  wrong, nothing is corrupted -- WordPress will just reject the
  request with a 4xx, visible in the workflow log.
- Every write is attempted independently and wrapped in try/except so
  one failure doesn't stop the rest of the run.
- This script makes NO business-fact decisions. The correct prices
  used below were confirmed by the site owner directly (see
  seo-db/technical_issues.json price-mismatch-evening-safari for the
  record of that confirmation) -- nothing here is guessed.
"""

import json
import os
import sys
import requests

SITE = "https://www.arabiansafariroyal.com"
WP_USERNAME = os.environ["WP_USERNAME"]
WP_APP_PASSWORD = os.environ["WP_APP_PASSWORD"]

session = requests.Session()
session.auth = (WP_USERNAME, WP_APP_PASSWORD)
session.headers.update({"User-Agent": "RAS-SEO-fix-script/1.0"})

results = []


def log(item_id, ok, detail):
    results.append({"id": item_id, "ok": ok, "detail": detail})
    print(f"[{'OK' if ok else 'FAIL'}] {item_id}: {detail}")


def verify_auth():
    r = session.get(f"{SITE}/wp-json/wp/v2/users/me")
    if r.status_code != 200:
        print(f"AUTH FAILED: {r.status_code} {r.text[:500]}")
        sys.exit(1)
    me = r.json()
    print(f"Authenticated as: {me.get('name')} (id {me.get('id')})")


def rankmath_update_meta(item_id, object_id, meta):
    """Best-effort call to RankMath's own meta-update REST endpoint.
    Logs the full response either way; never raises."""
    url = f"{SITE}/wp-json/rankmath/v1/updateMeta"
    payload = {"objectID": object_id, "objectType": "post", "meta": meta}
    try:
        r = session.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            log(item_id, True, f"RankMath updateMeta 200: {r.text[:300]}")
        else:
            log(item_id, False,
                f"RankMath updateMeta {r.status_code}: {r.text[:500]} "
                f"-- payload was {json.dumps(payload)[:300]}")
    except Exception as exc:
        log(item_id, False, f"Request error: {exc}")


def wp_update_media_alt(item_id, media_id, alt_text):
    url = f"{SITE}/wp-json/wp/v2/media/{media_id}"
    try:
        r = session.post(url, json={"alt_text": alt_text}, timeout=30)
        if r.status_code == 200:
            log(item_id, True, f"media {media_id} alt_text set")
        else:
            log(item_id, False, f"media {media_id} -> {r.status_code}: {r.text[:300]}")
    except Exception as exc:
        log(item_id, False, f"Request error on media {media_id}: {exc}")


def wp_resave_page(item_id, page_id):
    """PUT the page's own current content back unchanged, to trigger any
    on-save recalculation (e.g. reading-time estimate)."""
    try:
        get_r = session.get(f"{SITE}/wp-json/wp/v2/pages/{page_id}?_fields=content", timeout=30)
        if get_r.status_code != 200:
            log(item_id, False, f"could not read page {page_id} before resave: {get_r.status_code}")
            return
        content = get_r.json()["content"]["raw"] if "raw" in get_r.json()["content"] else None
        if content is None:
            log(item_id, False, "no editable 'raw' content field returned (app password may lack edit_posts context)")
            return
        put_r = session.post(f"{SITE}/wp-json/wp/v2/pages/{page_id}",
                              json={"content": content}, timeout=30)
        if put_r.status_code == 200:
            log(item_id, True, f"page {page_id} re-saved")
        else:
            log(item_id, False, f"page {page_id} resave -> {put_r.status_code}: {put_r.text[:300]}")
    except Exception as exc:
        log(item_id, False, f"Request error on page {page_id} resave: {exc}")


def rankmath_diagnostic_redirections():
    """Read-only: list RankMath redirections to see if anything targets
    the 403'ing stargazing URL. Never writes."""
    try:
        r = session.get(f"{SITE}/wp-json/rankmath/v1/status/getViewData", timeout=30)
        log("diag-redirections", r.status_code == 200,
            f"status/getViewData -> {r.status_code}: {r.text[:500]}")
    except Exception as exc:
        log("diag-redirections", False, f"Request error: {exc}")


def main():
    verify_auth()

    # --- P1: price mismatches (business-confirmed correct values) ---
    # /evening-desert-safari-abu-dhabi/ (post id 1696): confirmed correct
    # price is AED 35 (H1 was already right; title/meta said AED 50).
    rankmath_update_meta(
        "price-mismatch-evening-safari",
        1696,
        {
            "title": "Evening Desert Safari Abu Dhabi, From AED 35 With Dinner",
            "description": "Evening desert safari in Abu Dhabi with dune bashing, sunset, BBQ dinner and live shows. From AED 35 per person, no deposit, pay after, free cancellation.",
        },
    )

    # /dubai-desert-safari-price/ (page id 9962): confirmed correct price
    # is AED 35 (~USD 9.50) (H1 was already right; title/meta said USD 14).
    rankmath_update_meta(
        "price-mismatch-dubai-price-page",
        9962,
        {
            "title": "Dubai Desert Safari Price From AED 35, Flat Per-Car Rates",
            "description": "Dubai desert safari prices explained: shared from AED 35 (USD 9.50) per person, private from AED 599 per car, morning from AED 799. Per car not per person, no hidden or night fees.",
        },
    )

    # --- P1: mismatched utility-page meta descriptions ---
    rankmath_update_meta(
        "mismatched-utility-page-meta-terms",
        1628,
        {"description": "The terms and conditions for booking a desert safari or tour with Royal Arabian Safari: booking, cancellation, payment and liability terms."},
    )
    rankmath_update_meta(
        "mismatched-utility-page-meta-privacy",
        1627,
        {"description": "Royal Arabian Safari's privacy policy: what information we collect when you book a tour or contact us, and how it is used and protected."},
    )

    # --- P4: typo ---
    rankmath_update_meta(
        "typo-stargazing-meta",
        2599,
        {"description": "See the Milky Way from Abu Dhabi's darkest deserts on an overnight stargazing safari. Zero light pollution, Bedouin camp, BBQ dinner and telescope."},
    )

    # --- P1: thin stub page -> noindex + canonical to the main Dubai page ---
    rankmath_update_meta(
        "thin-stub-page-self-drive-dubai",
        9971,
        {
            "robots": ["noindex", "follow"],
            "canonicalUrl": f"{SITE}/dubai-desert-safari/",
        },
    )

    # --- P3: reading-time metadata bug -- trigger recalculation via resave ---
    wp_resave_page("reading-time-metadata-bug", 3254)

    # --- P2: media alt-text backfill ---
    alt_text_map = {
        21251: "Guest WhatsApp review screenshot praising a Royal Arabian Safari desert safari",
        21250: "Guest WhatsApp review screenshot praising a Royal Arabian Safari desert safari",
        21249: "Guest WhatsApp review screenshot praising a Royal Arabian Safari desert safari",
        21248: "Guest WhatsApp review screenshot praising a Royal Arabian Safari desert safari",
        21137: "TripAdvisor Travellers' Choice award presented to Royal Arabian Safari",
        21136: "TripAdvisor Travellers' Choice Award 2023 certificate for Royal Arabian Safari",
        21135: "World Travel Award certificate for Royal Arabian Safari",
        21020: "TripAdvisor Travellers' Choice badge for Royal Arabian Safari desert safari",
        20372: "Royal Arabian Safari desert safari experience photo",
        20371: "Royal Arabian Safari desert safari experience photo",
    }
    for media_id, alt in alt_text_map.items():
        wp_update_media_alt("media-alt-text-gap", media_id, alt)

    # --- Diagnostics only, no writes: check for anything tied to the 403 ---
    rankmath_diagnostic_redirections()

    print("\n\n===== SUMMARY =====")
    ok = sum(1 for r in results if r["ok"])
    print(f"{ok}/{len(results)} operations reported success")
    for r in results:
        print(f"  [{'OK' if r['ok'] else 'FAIL'}] {r['id']}")

    with open("fix_run_results.json", "w") as f:
        json.dump(results, f, indent=2)

    if any(not r["ok"] for r in results):
        print("\nSome operations failed -- see log above and fix_run_results.json. "
              "This is expected on the first run if the RankMath endpoint shape "
              "needs adjusting; nothing was corrupted, only rejected.")


if __name__ == "__main__":
    main()
