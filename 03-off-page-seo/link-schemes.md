---
title: Link Schemes to Avoid & the Disavow Process
topic_id: 03-off-page-seo/link-schemes
tags: [off-page-seo, link-spam, disavow, spambrain, penguin, manual-action, backlinks]
last_updated: 2026-07-18
confidence: robust
sources: [S97, S98, S101, S102, S60, S33, S103, S104]
---

## TL;DR
- Google defines **link spam** as links created *primarily to manipulate rankings*. The enumerated schemes are: buying/selling links that pass PageRank, excessive link exchanges, automated link generation, advertorial/guest-post/press-release links that pass ranking credit or use optimized anchors, and low-quality directory/widget/footer/forum links (S97).
- There is a **safe harbor**: paid/sponsored links are allowed *if* they carry `rel="nofollow"` or `rel="sponsored"` (S97, S60).
- The **Disavow Links tool** is for advanced users only. Google says the *vast majority of sites do not need it*; use it only when you have (1) a considerable volume of spammy/artificial/low-quality links **and** (2) a manual action, or imminent risk of one (S101, S102).
- Treat the disavow file as a **strong suggestion, not a command**; changes can take *multiple weeks* to take effect as Google recrawls (S101, S102).

## Core explanation
Google's anti-link-spam machinery has two layers: **algorithmic** detection (SpamBrain, the successor to the old Penguin filter) and **manual actions** taken by human reviewers. Both target the same behavior — *link spam* — which Google defines as "the practice of creating links to or from a site primarily for the purpose of manipulating search rankings" (S97).

A link is not spam merely because it is paid. Buying and selling links is "a normal part of the economy of the web" for advertising and sponsorship. The policy violation triggers when the link is *not qualified* with `rel="nofollow"` or `rel="sponsored"` and is therefore capable of passing ranking credit (S97). This is why every sponsored widget, advertorial, and native ad must be machine-discoverable as non-endorsing.

**Detection side (what happens to link spam):**
- **SpamBrain** is Google's AI-based spam-prevention system. The December 2022 link spam update extended it so it can detect *both* sites *buying* links and sites *used to pass outgoing links*. Impacted links are *neutralized at scale* — the ranking credit they passed is lost — across all languages, over a ~2-week rollout (S98).
- The historical **Penguin** filter (first launched April 2012, ~3.1% of queries affected) is now part of Google's core ranking systems and runs *real-time* and *more granular* (page/section level, not sitewide) since Penguin 4.0 (Sept 2016). The shift was from *demoting* a whole site to *devaluing* the specific spam signals (S104, S33). Google no longer announces Penguin refreshes because it is a continuous process (S104).

**Remediation side (the Disavow tool):** Because you cannot force third-party sites to remove links, Google provides a Disavow tool in Search Console: you upload a text file naming the URLs/domains you want Google to ignore. Google treats it as a strong suggestion (analogous to a canonical tag), not an absolute directive, and reserves judgment in corner cases (S101).

## Mechanics / how-to

### 1. Recognize the link schemes Google enumerates (S97)
- **Buying or selling links that pass PageRank** — exchanging money, goods, services, or a free product in return for a dofollow link.
- **Excessive link exchanges** — "you link to me and I'll link to you" at scale, where the purpose is manipulation rather than genuine reference.
- **Automated link generation** — programs or services that create links to your site automatically.
- **Links in advertorials / guest posts / press releases / articles** that *pass ranking credit* or use *optimized anchor text*, unless qualified.
- **Low-quality directory, widget, footer, or forum links** created mainly to manipulate rankings (e.g., keyword-rich links embedded in a distributed widget; irrelevant paid directory listings).

### 2. Use the safe harbor (S97, S60)
Qualify any non-editorial outbound link with one of:
- `rel="nofollow"` — generic "don't endorse / don't pass credit."
- `rel="sponsored"` — specifically for paid/sponsored/advertorial links (preferred).
- `rel="ugc"` — user-generated content such as forum posts and comments.

Note: since 2020, `nofollow`, `sponsored`, and `ugc` are treated as **hints**, not hard directives, for both ranking and crawling — Google may still choose to follow or count them (S60). The safe harbor works because the *intent* is declared; qualifying links is how you stay compliant while still running normal advertising.

### 3. Decide whether you need to disavow (S102, Step 0)
Disavow **only if both** are true:
1. You have a considerable number of spammy, artificial, or low-quality links pointing to your site, **AND**
2. Those links have caused a **manual action**, or you reasonably expect one (e.g., you bought links or ran link schemes that violate spam policies).

In most cases Google already assesses which links to trust without your input, so most sites never need the tool (S101, S102). *Remove links first, disavow second.*

### 4. Build the disavow file
- Plain text, UTF-8 or 7-bit ASCII, filename ending in `.txt`.
- One URL or `domain:` entry per line. You cannot disavow a subpath like `example.com/en/`.
- `domain:example.com` disavows all pages on that domain (and, for most free hosts, a specific subdomain).
- Lines starting with `#` are comments (ignored by Google — they are for *your* records, not Google's; S103).
- Limits: max **100,000 lines** and **2 MB** (S102). Older blog copy cited 2 MB only (S101).
- Domain properties are **not supported** — you must use a URL-prefix property; upload a list per relevant property (http + https) (S102).

### 5. Upload and (if applicable) request reconsideration
- Upload at Search Console → Disavow Links → select the URL-prefix property → upload `.txt` (S102).
- Re-uploading **replaces** the whole list; downloading first preserves history (S101, S102).
- If you received a **manual action**, you must still file a **reconsideration request** after cleaning up and uploading — the disavow alone does not lift a manual action (S101).
- Allow **multiple weeks** for recrawl/reindex before effects appear (S101, S102).

## Worked example / code

**Disavow file (`disavow.txt`):**
```text
# Disavow list for example.com — generated 2026-07-18
# Outreach removed ~40 links; the following remain and are unnatural.
# Paid link network (money-for-link, dofollow) — could not get taken down.
domain:cheap-link-network.example
# Sponsored widget with keyword-rich anchor, host refused to add rel=sponsored.
domain:free-widget-vendor.example
# Individual low-quality directory page passing optimized anchor text.
https://lowquality-directory.example.net/biz/listing-12345.html
```

**Reproducible Python: validate & build a disavow file from a backlink export**
This script reads a CSV from Ahrefs/Semrush/GSC (columns `url` = the *linking* page, and a `flag` column you set to `disavow`), validates format against Google's rules, and writes `disavow.txt`. Pinned for reproducibility.

```python
# Requires: python>=3.11, pandas>=2.0
# Usage: python build_disavow.py backlinks.csv disavow.txt
import sys
import re
import pandas as pd  # pandas>=2.0

DOMAIN_RE = re.compile(r"^domain:[a-z0-9.-]+\.[a-z]{2,}$", re.I)
URL_RE = re.compile(r"^https?://", re.I)
MAX_LINES = 100_000
MAX_BYTES = 2 * 1024 * 1024

def normalize(entry: str) -> str:
    entry = entry.strip()
    if entry.startswith("#") or not entry:
        return entry
    if entry.lower().startswith("domain:"):
        if not DOMAIN_RE.match(entry):
            raise ValueError(f"Bad domain entry: {entry}")
        return entry.lower()
    if not URL_RE.match(entry):
        raise ValueError(f"Not a URL and not a domain: entry: {entry}")
    if len(entry) > 2048:
        raise ValueError(f"URL too long (>2048 chars): {entry[:60]}...")
    return entry

def main(in_csv: str, out_txt: str) -> None:
    df = pd.read_csv(in_csv)
    # 'flag' column should contain 'disavow' for rows to include
    flagged = df[df.get("flag", pd.Series(dtype=str)).astype(str).str.lower() == "disavow"]
    lines = []
    for link in flagged["url"].astype(str):
        # allow either a full URL or a "domain:" prefix already present
        if link.lower().startswith("domain:"):
            lines.append(normalize(link))
        else:
            lines.append(normalize(link))
    # de-dup, preserve order
    seen, out = set(), []
    for ln in lines:
        if ln and ln not in seen:
            seen.add(ln); out.append(ln)
    assert len(out) <= MAX_LINES, f"Too many lines: {len(out)} > {MAX_LINES}"
    text = "\n".join(out) + "\n"
    assert len(text.encode("utf-8")) <= MAX_BYTES, "File exceeds 2 MB"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {len(out)} disavow entries to {out_txt}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

*Data source:* your own backlink export (GSC Links report, Ahrefs, or Semrush). The script performs only format validation — it does **not** judge link quality; you must set `flag` yourself after manual review.

## Assumptions & limitations
- **Google's judgment overrides yours.** The disavow file is a strong suggestion, not a command; Google "reserves the right to trust our own judgment for corner cases" (S101). Disavowing a *good* link can actively harm you.
- **Recrawl latency.** Effects take multiple weeks; there is no instant penalty removal (S101, S102).
- **Domain properties unsupported.** If you use a Domain property, the disavow UI does not apply — switch to a URL-prefix property (S102).
- **Disavow ≠ reconsideration.** For a manual action you must additionally submit a reconsideration request (S101).
- **Algorithmic vs. manual.** After Penguin 4.0's real-time/devaluing model, most purely algorithmic link-spam is neutralized automatically; the disavow tool's main job is cleaning up *before/after a manual action* (S102, S104, S103).
- **Google has NOT published** a definitive current weighting of links vs. other signals, nor a "safe link velocity." Claims that links are "still a top-3 ranking factor" or that a specific anchor-text ratio is optimal are **contested** — see the open Verify task (backlog) before asserting them.

## Empirical evidence
- **Policy stability:** Google's link-spam examples and safe harbor have been stable across many years of the spam-policies page (last updated 2026-05-15, S97), and the disavow philosophy ("vast majority of sites do not need this tool") has been constant since the tool launched in 2012 (S101) and is restated in the current support doc (S102). Strength: **strong** (first-party, repeated).
- **SpamBrain scale:** The December 2022 update neutralized unnatural-link credit "at scale" across all languages in ~2 weeks (S98). Strength: **strong** (first-party) but no public per-site quantification.
- **Penguin impact (historical):** Penguin 1.0 (April 2012) affected ~3.1% of queries; later refreshes 0.1–2.3% (S104). Strength: **moderate** (third-party reporting of Google's own percentages; dated 2016).
- **Practitioner view:** Ahrefs' complete guide (2018, dated) finds the field consensus is "it depends" and that the need for disavowing dropped after Penguin 4.0's shift from demotion to devaluation (S103). Treat as **directional, dated** — Google's current support doc is the authoritative answer (S102).
- **Sample/evidence limitations:** No public A/B study quantifies ranking recovery attributable to disavow vs. spontaneous algorithmic refresh; causes of recovery are confounded.

## Conflicting views
- **"Disavow everything suspicious" vs. "never disavow without a manual action."** Older SEO advice (pre-Penguin-4.0, ~2012–2016) treated disavow as essential defensive hygiene (S103). Google's current position is the opposite: only use it for manual actions / imminent manual-action risk (S101, S102). The conflict is largely explained by *timing* — the tool mattered far more when Penguin was a periodic, sitewide filter (S104).
- **Do links still matter as much?** Google removed the line "Google uses links as a factor in determining relevancy of web pages" from its Link Spam guidance around 2024, prompting speculation (e.g., Marie Haynes) that Google is de-emphasizing links in favor of vector/semantic matching. This is **speculation, not confirmation** — Google has not stated links are deprecated. Flagged as **contested**; do not assert a specific current weight.
- **nofollow as a directive vs. hint.** Pre-2019, `nofollow` was closer to a directive for PageRank sculpting; since the 2019 evolution it is a *hint* for both ranking and crawling (S60). Old "sculpt PageRank with nofollow" advice is obsolete.

## Common mistakes
1. **Disavowing good/editorial links** because a tool flagged them as "low DA." You can permanently lose legitimate equity; Google will typically ignore your disavow of a healthy link anyway, but a mistaken `domain:` entry can wipe many good links at once (S101).
2. **Using disavow as a preventative measure** with no manual action and no unnatural-link history — explicitly discouraged (S101, S102).
3. **Disavowing before attempting removal.** Google's first recommendation is to *remove* the links from the web; disavow is the fallback (S101, S102).
4. **Forgetting http vs. https.** If you have both properties, upload a list to each; a list on `example.com` also covers `m.example.com` but not necessarily a separate `https` property (S102).
5. **Assuming disavow lifts a manual action.** You must file a reconsideration request and demonstrate cleanup (S101).
6. **Qualifying a link incorrectly or not at all.** Selling a dofollow sponsored link without `rel="sponsored"`/`rel="nofollow"` is a textbook link scheme (S97).
7. **Trusting third-party "toxic link" scores blindly.** Vendor spam scores are heuristics; use them to *prioritize review*, not as automated disavow decisions.
8. **Thinking disavow hides links in reports.** Disavowed links still appear in the GSC Links report (S102) — the file only affects how Google *weights* them.

## Further reading
- **Tier 1 (authoritative):** Google spam policies — link spam (S97); Disavow tool launch blog (S101); Search Console Disavow help (S102); Evolving nofollow/sponsored/ugc (S60); ranking systems guide incl. SpamBrain/Penguin lineage (S33); December 2022 link spam update / SpamBrain (S98).
- **Tier 2 (practitioner):** Ahrefs "Google's Disavow Links Tool: The Complete Guide" (S103); Search Engine Land "Penguin now real-time, part of core" (S104).
- **Related KB articles:** `03-off-page-seo/backlinks.md` (link quality, PageRank), `03-off-page-seo/digital-pr.md` (earning editorial links compliantly), `15-pitfalls/buying-links-pbns.md` (penalty risk).
