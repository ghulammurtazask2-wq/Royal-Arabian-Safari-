# 5 Fixes That Need a Manual wp-admin Edit

**Date:** 2026-09-30

## Why these can't be applied automatically

Two independent write attempts were tried against the live site — RankMath's own SEO meta-update endpoint, and a fallback attempt writing RankMath's real internal field names through WordPress's standard, stable REST API. Both returned success (HTTP 200) on every attempt, but the live pages never actually changed. This was confirmed with cache-busting, uncached GET requests showing genuinely fresh content (not a caching artifact) still displaying the old values.

This session has no way to open a browser with your WordPress login — that path was explicitly blocked earlier as a data-exfiltration risk and that restriction stands. So these 5 need a 2-minute manual edit each, in **wp-admin → [page] → Edit → RankMath SEO box** (usually below the content editor, or a sidebar panel in the block editor).

---

## 1. Evening Desert Safari Abu Dhabi
**Page:** `/evening-desert-safari-abu-dhabi/`
**In RankMath's SEO Title field, paste:**
```
Evening Desert Safari Abu Dhabi, From AED 35 With Dinner
```
**In RankMath's Meta Description field, paste:**
```
Evening desert safari in Abu Dhabi with dune bashing, sunset, BBQ dinner and live shows. From AED 35 per person, no deposit, pay after, free cancellation.
```

## 2. Terms & Conditions
**Page:** `/terms-conditions/`
**In RankMath's Meta Description field, paste:**
```
The terms and conditions for booking a desert safari or tour with Royal Arabian Safari: booking, cancellation, payment and liability terms.
```

## 3. Privacy Policy
**Page:** `/privacy-policy/`
**In RankMath's Meta Description field, paste:**
```
Royal Arabian Safari's privacy policy: what information we collect when you book a tour or contact us, and how it is used and protected.
```

## 4. Stargazing Page Typo
**Page:** `/stargazing-desert-safari-abu-dhabi/`
**In RankMath's Meta Description field, paste (replacing the current one that starts with a stray "a"):**
```
See the Milky Way from Abu Dhabi's darkest deserts on an overnight stargazing safari. Zero light pollution, Bedouin camp, BBQ dinner and telescope.
```

## 5. Self-Drive Dubai Stub Page
**Page:** `/self-drive-desert-safari-dubai/`
**In RankMath's Advanced tab:**
- Set **Robots Meta → No Index** (checked)
- Set **Canonical URL** to:
```
https://www.arabiansafariroyal.com/dubai-desert-safari/
```

---

After editing each one, click Update/Publish as normal. No other fields need to change.
