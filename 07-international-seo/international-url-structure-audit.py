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
