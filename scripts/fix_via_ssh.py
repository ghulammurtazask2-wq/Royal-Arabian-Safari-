"""
Applies the 5 fixes that RankMath's REST endpoints would not persist,
by connecting over SSH and running WP-CLI directly against the
WordPress database. This bypasses RankMath's REST layer entirely --
WP-CLI's `wp post meta update` writes straight to wp_postmeta via
WordPress core, the same underlying mechanism RankMath's own admin
UI uses when you save a page, and it was found to be the only
avenue with two independent REST write paths both silently no-op'ing
for these specific items (see seo-db/technical_issues.json for the
full trail).

Runs from GitHub Actions (workflow_dispatch), authenticated with
SSH_HOST / SSH_PORT / SSH_USER / SSH_PASSWORD repo secrets. Never
run this with credentials pasted inline -- it reads them from the
environment only.

RankMath's real postmeta key names (rank_math_title,
rank_math_description, rank_math_robots, rank_math_canonical_url)
are public in RankMath's own source code, not guessed -- same values
already tried (and logged) via the REST fallback in apply_wp_fixes.py.
"""

import json
import os
import shlex
import sys

import paramiko

SITE = "https://www.arabiansafariroyal.com"
SSH_HOST = os.environ["SSH_HOST"]
SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
SSH_USER = os.environ["SSH_USER"]
SSH_PASSWORD = os.environ["SSH_PASSWORD"]

results = []


def log(item_id, ok, detail):
    results.append({"id": item_id, "ok": ok, "detail": detail})
    print(f"[{'OK' if ok else 'FAIL'}] {item_id}: {detail}")


def run(client, wp_path, command_parts, item_id):
    """Runs a wp-cli command via SSH, quoting every argument safely.
    Always logs full stdout/stderr, never assumes success."""
    quoted = " ".join(shlex.quote(p) for p in command_parts)
    full_cmd = f"wp --path={shlex.quote(wp_path)} {quoted}"
    stdin, stdout, stderr = client.exec_command(full_cmd, timeout=30)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors="replace").strip()
    err = stderr.read().decode(errors="replace").strip()
    ok = exit_code == 0
    log(item_id, ok, f"exit {exit_code} | cmd: {full_cmd[:200]} | stdout: {out[:300]} | stderr: {err[:300]}")
    return ok


def find_wp_path(client):
    """Locate the WordPress install directory by finding wp-config.php,
    since the SSH login directory isn't guaranteed to be the WP root."""
    stdin, stdout, stderr = client.exec_command(
        "find ~ -maxdepth 5 -iname wp-config.php 2>/dev/null | head -1", timeout=30
    )
    stdout.channel.recv_exit_status()
    path = stdout.read().decode(errors="replace").strip()
    if not path:
        return None
    return path.rsplit("/", 1)[0]


def verify_live(check_id, url, expect_substring=None, unexpect_substring=None):
    """Same approach as apply_wp_fixes.py: fetch the actual public URL
    (cache-busting query param + no-cache headers, no auth) and check
    whether the change is really visible, rather than trusting the
    write command's exit code alone."""
    import random
    import requests
    bust_url = f"{url}{'&' if '?' in url else '?'}_verify={random.randint(100000, 999999)}"
    try:
        r = requests.get(bust_url, timeout=30, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
        cache_headers = {k: v for k, v in r.headers.items()
                          if "cache" in k.lower() or k.lower() in ("age", "cf-cache-status", "x-litespeed-cache")}
        has_expected = expect_substring is None or expect_substring in r.text
        has_unexpected = unexpect_substring is not None and unexpect_substring in r.text
        ok = has_expected and not has_unexpected
        parts = []
        if expect_substring is not None:
            parts.append(f"expected {'FOUND' if has_expected else 'MISSING'}")
        if has_unexpected:
            parts.append("unwanted text still present")
        parts.append(f"cache headers: {cache_headers}")
        log(check_id, ok, "live GET " + url + " -> " + "; ".join(parts))
    except Exception as exc:
        log(check_id, False, f"verify request error on {url}: {exc}")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=30)
    except Exception as exc:
        print(f"SSH CONNECTION FAILED: {exc}")
        sys.exit(1)
    print(f"Connected to {SSH_HOST}:{SSH_PORT} as {SSH_USER}")

    wp_path = find_wp_path(client)
    if not wp_path:
        print("Could not locate wp-config.php under the home directory -- cannot proceed.")
        sys.exit(1)
    print(f"Found WordPress install at: {wp_path}")

    if not run(client, wp_path, ["--info"], "wp-cli-available"):
        print("wp-cli is not usable at this path -- cannot proceed.")
        client.close()
        sys.exit(1)

    # --- price-mismatch-evening-safari (post 1696) ---
    run(client, wp_path,
        ["post", "meta", "update", "1696", "rank_math_title",
         "Evening Desert Safari Abu Dhabi, From AED 35 With Dinner"],
        "ssh-price-evening-safari-title")
    run(client, wp_path,
        ["post", "meta", "update", "1696", "rank_math_description",
         "Evening desert safari in Abu Dhabi with dune bashing, sunset, BBQ dinner and live shows. "
         "From AED 35 per person, no deposit, pay after, free cancellation."],
        "ssh-price-evening-safari-desc")

    # --- mismatched-utility-page-meta (terms 1628, privacy 1627) ---
    run(client, wp_path,
        ["post", "meta", "update", "1628", "rank_math_description",
         "The terms and conditions for booking a desert safari or tour with Royal Arabian Safari: "
         "booking, cancellation, payment and liability terms."],
        "ssh-terms-meta")
    run(client, wp_path,
        ["post", "meta", "update", "1627", "rank_math_description",
         "Royal Arabian Safari's privacy policy: what information we collect when you book a tour "
         "or contact us, and how it is used and protected."],
        "ssh-privacy-meta")

    # --- typo-stargazing-meta (page 2599) ---
    run(client, wp_path,
        ["post", "meta", "update", "2599", "rank_math_description",
         "See the Milky Way from Abu Dhabi's darkest deserts on an overnight stargazing safari. "
         "Zero light pollution, Bedouin camp, BBQ dinner and telescope."],
        "ssh-stargazing-typo")

    # --- thin-stub-page-self-drive-dubai (page 9971): noindex + canonical ---
    run(client, wp_path,
        ["post", "meta", "update", "9971", "rank_math_robots",
         json.dumps(["noindex", "follow"]), "--format=json"],
        "ssh-stub-robots")
    run(client, wp_path,
        ["post", "meta", "update", "9971", "rank_math_canonical_url",
         f"{SITE}/dubai-desert-safari/"],
        "ssh-stub-canonical")

    client.close()

    # --- VERIFY: same public-page check as apply_wp_fixes.py ---
    verify_live("ssh-verify-price-evening-safari", f"{SITE}/evening-desert-safari-abu-dhabi/",
                "AED 35", unexpect_substring="AED 50 per person")
    verify_live("ssh-verify-terms-meta", f"{SITE}/terms-conditions/",
                "booking, cancellation, payment and liability", unexpect_substring="Quad biking in Abu Dhabi")
    verify_live("ssh-verify-privacy-meta", f"{SITE}/privacy-policy/",
                "what information we collect")
    verify_live("ssh-verify-stargazing-typo", f"{SITE}/stargazing-desert-safari-abu-dhabi/",
                unexpect_substring="aSee the Milky Way")
    verify_live("ssh-verify-stub-noindex", f"{SITE}/self-drive-desert-safari-dubai/",
                'name="robots" content="noindex')

    print("\n\n===== SUMMARY =====")
    ok = sum(1 for r in results if r["ok"])
    print(f"{ok}/{len(results)} operations reported success")
    for r in results:
        print(f"  [{'OK' if r['ok'] else 'FAIL'}] {r['id']}")

    with open("ssh_fix_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
