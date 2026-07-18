---
title: International URL Structure — ccTLD vs Subdomain vs Subfolder
topic_id: 07-international-seo/international-url-structure
tags: [international, ccTLD, subdomain, subfolder, subdirectory, geo-targeting, hreflang]
last_updated: 2026-07-18
confidence: robust
sources: [S187, S188, S189, S179, S12]
---

## TL;DR
All three international URL structures — country-code top-level domains (`example.de`), subdomains (`de.example.com`), and subfolders (`example.com/de/`) — are valid in Google Search; Google says either subdomains or subfolders are fine and both rank (S187, S188). The real trade-off is **signal consolidation and operations, not a built-in ranking penalty**: ccTLDs send the strongest *country* signal but do **not** share link equity across countries and cost the most to run (S187); subfolders inherit the root domain's authority and are the lowest-maintenance default; subdomains are only treated as "part of the site" when you actually link them into it (S188). Pick the structure you can keep for years, set locale in the URL (never cookies/IP), and layer `hreflang` on top regardless of the choice (S187, S179).

## Core explanation
When a site serves users in multiple countries and/or languages, search engines need an explicit signal about which URL is for whom. The **URL structure** is the foundation of that signal. Three patterns are in common use:

- **ccTLD** (country-code top-level domain): `example.de`, `example.fr` — a separate domain per country, registered under that country's TLD.
- **Subdomain** (with a gTLD): `de.example.com`, `fr.example.com` — a host prefix on the same root domain.
- **Subfolder / subdirectory** (with a gTLD): `example.com/de/`, `example.com/fr/` — a path segment on the same host.

Google's official guidance is that all three are workable (S187). The choice is **not** a ranking on/off switch; it changes *how much of your existing authority each variant inherits, how clearly you signal country intent, and how much infrastructure you operate* (S187, S188, S189).

A second, orthogonal layer — `hreflang` annotations — tells Google which URL is the language/region equivalent of which other URL. Structure choice and hreflang are independent: you still need correct hreflang whether you use a subfolder, subdomain, or ccTLD (S179). See `hreflang-implementation.md` for that half.

## Mechanics / how-to
### The official trade-off table (Google, S187)
| Structure | What Google lists as strengths | What Google lists as weaknesses |
|---|---|---|
| **ccTLD** (`example.de`) | Clear geotargeting; server location irrelevant; easy separation of sites | Expensive (limited availability); more infrastructure; strict ccTLD requirements sometimes; **can only target a single country** |
| **Subdomain** (`de.example.com`) | Easy to set up; allows different server locations; easy separation of sites | Users may not read geotargeting from the URL alone (is `de` a language or a country?) |
| **Subfolder** (`example.com/de/`) | Easy to set up; low maintenance (same host) | Users may not read geotargeting from the URL alone; single server location; harder to separate sites |
| **URL parameters** (`example.com?country=de`) | — | **Not recommended** by Google (segmentation difficult, not user-recognizable) |

### Choosing a structure (decision framework)
1. **Default to subfolders** unless you have a specific reason not to. They inherit the root domain's accumulated authority and links, need the least infrastructure, and are the easiest to manage as you add markets (S187, S189). Most practitioners favor them for exactly this reason (S189).
2. **Use a ccTLD when** you need the strongest possible *country* signal, operate as a distinct local brand/legal entity in that market, or face regulatory/trust reasons to be on a local domain (e.g. `.ca`, `.de`). Accept that you must build authority for each ccTLD from scratch and run separate infrastructure (S187).
3. **Use a subdomain when** a section is genuinely a separate product/team/stack but still part of your brand, and you will **link it into the main site internally**. A subdomain that is not internally linked may be treated as a separate site and will not benefit from the root's authority (S188).
4. **Never** rely on cookies, JavaScript, or IP-based language switching to serve variants at the *same* URL — Googlebot crawls from the US and sends **no `Accept-Language` header**, so it may only ever see one variant (S187).

### Signals Google actually uses to pick a target locale (S187)
- **ccTLD** — the strongest country signal (`.de` → Germany). Some "vanity" ccTLDs (`.tv`, `.me`, `.io`, `.co`, …) are treated as gTLDs, not country signals.
- **`hreflang`** annotations (tags, HTTP headers, or sitemaps).
- **Server location (IP)** — a weak signal; often overridden by CDNs/hosting choices, so don't rely on it.
- **Other signals** — local addresses/phone numbers, local language and currency, links from local sites, Business Profile signals.
- **What Google does NOT use:** locational HTML meta tags (`geo.position`, `distribution`) are ignored; and Google does **not** vary its crawler per site to discover locale variants, so you must declare them explicitly (S187).

## Worked example / code
A small, dependency-free audit that flags the two structural mistakes Google explicitly warns against (S187): locale encoded in **query parameters** (not recommended) and URLs that don't encode locale in the host/path at all (cookie/IP switching risk). Run with Python 3.8+.

```python
#!/usr/bin/env python3
# international-url-structure-audit.py
# Classify international URLs by structure and flag Google-discouraged patterns.
# Source of rules: Google "Managing multi-regional and multilingual sites" (S187).
# Usage: python3 international-url-structure-audit.py urls.txt
import sys, re
from urllib.parse import urlsplit

# Minimal ccTLD set for demonstration; extend as needed.
CC_TLDS = {"de","fr","es","it","nl","ru","jp","cn","uk","ca","au","br","in","mx","se","pl","us"}

URL_PARAM_LOCALE = re.compile(r"[?&](lang|language|locale|country|region)=", re.I)

def classify(url):
    parts = urlsplit(url)
    host = parts.netloc.lower()
    labels = host.split(".")
    # ccTLD: last label is a ccTLD and there is a second-level domain before it
    if len(labels) >= 2 and labels[-1] in CC_TLDS and labels[-2] not in ("www",):
        return "ccTLD"
    # subdomain: first label looks like a 2-letter locale prefix
    if len(labels) >= 3 and len(labels[0]) == 2 and labels[0].isalpha():
        return "subdomain"
    # subfolder: path starts with /xx/ or /xx-yy/
    m = re.match(r"/(?:[a-z]{2}(?:-[a-z]{2})?)/", parts.path.lower())
    if m:
        return "subfolder"
    return "unknown"

def audit(urls):
    counts = {}
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
        struct = classify(url)
        counts[struct] = counts.get(struct, 0) + 1
        flags = []
        if URL_PARAM_LOCALE.search(url):
            flags.append("LOCALE-IN-QUERY-PARAM (Google: not recommended)")
        if struct == "unknown" and not URL_PARAM_LOCALE.search(url):
            flags.append("LOCALE-NOT-IN-HOST-OR-PATH (cookie/IP switching risk)")
        line = f"[{struct:9}] {url}"
        if flags:
            line += "  -> WARNING: " + "; ".join(flags)
        print(line)
    print("\nStructure distribution:", counts)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        # inline demo
        demo = [
            "https://example.de/",
            "https://de.example.com/",
            "https://example.com/de/",
            "https://example.com/fr-be/",
            "https://example.com/?country=de",   # flagged
            "https://example.com/",              # flagged (no locale in URL)
        ]
        audit(demo)
    else:
        with open(path, encoding="utf-8") as f:
            audit(f.read().splitlines())
```

Indicative output for the demo:
```
[ccTLD    ] https://example.de/
[subdomain] https://de.example.com/
[subfolder] https://example.com/de/
[subfolder] https://example.com/fr-be/
[unknown  ] https://example.com/?country=de  -> WARNING: LOCALE-IN-QUERY-PARAM (Google: not recommended)
[unknown  ] https://example.com/  -> WARNING: LOCALE-NOT-IN-HOST-OR-PATH (cookie/IP switching risk)
Structure distribution: {'ccTLD': 1, 'subdomain': 1, 'subfolder': 2, 'unknown': 2}
```

## Assumptions & limitations
- Google's published position is that subdomains and subfolders are treated equivalently for crawling and ranking (S187, S188). The *perceived* subdomain disadvantage in case studies is usually explained by a confound — a subdomain that isn't internally linked, or migrated alongside added content/links — not by the URL position itself (S188).
- A ccTLD's country signal is strong, but Google still **ignores** the *language* implied by a path like `/en/`; language is detected from visible page content, not the URL or `lang` attribute (S187). The URL encodes *country/structure*, not language definitively.
- Server location is a weak and often-overridden signal; with CDNs it is effectively meaningless for geotargeting, so ccTLDs' "server location irrelevant" advantage matters less than it once did (S187).
- None of these structures *guarantees* rankings. They affect signal consolidation and clarity, not relevance.
- Migrating from one structure to another is a high-risk operation: Google needs time to "settle" a changed URL structure, and equity transfer depends on correct 301 redirects + internal linking (S188). Don't change structure for a marginal SEO belief.

## Empirical evidence
- **Primary description:** Google's multi-regional-sites documentation (S187, last updated 2025-12-10) is the authoritative statement of the three options, their listed pros/cons, and the signals used for locale detection. This is first-party guidance, not a correlation study.
- **Practitioner observation:** Search Engine Journal reports that SEO experts "often favor subdirectories" because new URLs inherit the root's established authority, and recounts one client that regained ~15% traffic after moving a section back from a subdomain to the main domain (S189). This is a **single-client anecdote**, directional only; Ahrefs explicitly notes that subdomain-vs-subfolder case studies are routinely confounded by simultaneous internal-linking or content changes, so they do **not** prove the URL position caused the change (S188).
- **Strength of evidence:** The *mechanics* (what each structure is, what Google says) are Tier-1 established. The *performance difference* between subfolders and subdomains in the wild is **not** established by controlled study — only by correlation-prone case studies. Treat "subfolders rank better" as a practitioner preference, not a confirmed law.

## Conflicting views
- **"Subdirectories are strictly better for SEO."** Common practitioner view (S189). **Vs.** Google's position that there is no inherent difference and either is fine (S187, S188). Resolution: Google ranks both; the practical edge for subfolders is easier *authority consolidation and lower operations cost*, plus the fact that a neglected subdomain can be treated as separate (S188). It is a management/signal-efficiency advantage, not a ranking penalty on subdomains per se.
- **"ccTLDs share my domain authority."** Incorrect — a ccTLD is a separate domain and does **not** inherit the root gTLD's links/authority (S187, S12 on URL consolidation). This is the central cost of the strong country signal.
- **"The URL `lang`/path tells Google the language."** Google reads language from page content, not from the URL or `lang` attribute; only a ccTLD signals *country* (S187).

## Common mistakes
1. **Cookie/IP/JS language switching at one URL** — Googlebot crawls from the US with no `Accept-Language` header and may never see non-default variants (S187). Always use distinct URLs.
2. **Locale in query parameters** — Google lists URL parameters as "not recommended" for segmentation (S187).
3. **Auto-redirecting by detected language/IP** — can trap users and crawlers out of other variants; offer explicit language links instead (S187).
4. **Expecting a ccTLD to inherit root authority** — it won't; budget for building each market's links separately (S187).
5. **Subdomain left unlinked from the main site** — may be treated as a separate site and lose inherited authority; link it in (S188).
6. **Treating `/en/` as a language guarantee** — Google detects language from content, not the path; ensure each variant is genuinely in that language (S187).
7. **Relying on `geo.*` meta tags or server location** for targeting — ignored / weak; use ccTLD or hreflang (S187).
8. **Changing structure for a supposed SEO bump** — introduces migration risk for an unproven gain; pick once and keep it (S188).

## Further reading
- S187 — Google Search Central, "Managing multi-regional and multilingual sites" (developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) — Tier 1 (structure table, locale signals, what Google ignores).
- S188 — Ahrefs, "Subdomain vs Subdirectory" by Patrick Stox (ahrefs.com/blog/subdomain-vs-subfolder) — Tier 2 (Google-rep quotes: Cutts 2012, Mueller 2017, Illyes 2023; subdomain-as-separate nuance; case-study confounds).
- S189 — Search Engine Journal, "Subdomain, Subdirectory & ccTLD: Which One Should You Use?" (searchenginejournal.com/subdomain-subdirectory-cctld-which-one-should-you-use/448277) — Tier 2 (decision framework, expert preference, case study).
- S179 — Google Search Central, "Tell Google about localized versions of your page" (support.google.com/webmasters/answer/189077) — Tier 1 (hreflang, orthogonal to structure choice).
- S12 — Bing Webmaster Guidelines (bing.com/webmasters/help/webmaster-guidelines-30fba23a) — Tier 1 (URL consolidation / duplicate-URL principle; applies across all structures).
