---
title: Anchor Text & Link Velocity — Myth vs Evidence
topic_id: 03-off-page-seo/anchor-text-link-velocity
tags: [off-page-seo, backlinks, anchor-text, link-velocity, penguin, link-building]
last_updated: 2026-07-18
confidence: robust
sources: [S33, S58, S97, S104, S105, S106, S107, S108, S109]
---

## TL;DR
- **Anchor text is a real (but weak) relevance signal** Google uses to understand what a linked page is about; it is *not* a strong standalone ranking lever, and over-optimizing it (stuffing exact-match anchors) can trigger a Penguin-style demotion.
- **There is no published "safe" anchor-text ratio.** A 384,614-page Ahrefs study found the *median* exact-match anchor share at every ranking position is ~0% — many top pages have zero exact-match anchors — so vendor "keep exact-match to 1–5%" rules are folklore, not confirmed fact (S105).
- **Link velocity is not a confirmed ranking factor or penalty trigger.** Google's own search reps (Mueller, Illyes) say the speed of link acquisition doesn't matter; what matters is whether individual links are natural vs manipulative (S106).
- Practical takeaway: write **descriptive, natural anchor text**, don't engineer ratios, and stop fearing "too many links too fast" for legitimately earned coverage.

## Core explanation

### What anchor text is
Anchor text is the visible, clickable words in a hyperlink (the content of the `<a>` element). Google's original research (Brin & Page, 1998) treated link text as a special signal — anchors often describe a target page *better* than the page describes itself, and let Google infer the topic of non-text assets (images, files). Google's current link best-practices doc still instructs webmasters to "write good anchor text" that is descriptive, concise, and relevant to both pages (S58). John Mueller (Google) has reiterated that anchor text helps Google understand a link's context and may act as a relevance signal (quoted via S105).

### The manipulation problem and Penguin
Because anchor text was heavily weighted early on, SEOs gamed it: point many keyword-rich links at a page and it ranked. "Google bombing" (e.g., a page ranking #1 for "miserable failure") made the weakness obvious. Google's **Penguin** algorithm (first launched April 2012) explicitly targeted unnatural, over-optimized anchor-text link schemes; Google stated it affected ~3.1% of English queries at launch (S105). Penguin later became part of the core algorithm (Penguin 4.0, Sept 2016), running in real time and *devaluing* spammy links rather than sitewide-demoting (S104, S33).

### What "link velocity" means
Link velocity is the *theory* that the **speed** at which a site gains backlinks (links/month) affects rankings — positively (old "more faster = better") or negatively (a fast spike "looks manipulative" and gets you penalized). The concept traces to a 2003 Google patent, *Information Retrieval Based on Historical Data* (US7346839B2), which mentions that a "spiky rate of growth" in backlinks "may signal an attempt to spam" (S107). That is the entire evidentiary basis — a *patent*, not a statement of what Google runs today.

## Mechanics / how-to

### Writing good anchor text (what Google actually asks for)
From Google's link best practices (S58):
1. Use real, crawlable `<a href="…">` links (anchor must appear in rendered HTML; JS-injected anchors must be in the rendered DOM).
2. Make anchor text **descriptive, concise, and relevant** to the destination page — not to the source.
3. Avoid generic anchors ("click here", "article", "page") — they give Google (and users) no context.
4. **Do not keyword-stuff** anchor text; forced optimized anchors violate Google's spam policies (S97).
5. Don't chain adjacent links to the same target with different anchors just to "spread" keywords.

Good vs bad example:
```html
<!-- Good: descriptive, natural -->
<a href="/seo-audit-checklist">download our SEO audit checklist</a>

<!-- Bad: keyword-stuffed, manipulative -->
<a href="/seo-audit-checklist">SEO audit checklist, free SEO audit, best SEO audit template</a>
```

### Building a natural profile (no ratio engineering)
- Earn links editorially (digital PR, linkable assets, genuine citations). For the few links where you control the anchor (e.g., guest-bio, resource page), default to **branded or naked-URL** anchors (S105).
- Vary phrasing naturally — real linkers use your brand name, the page title, a sentence fragment, or "this study," not a uniform keyword.
- Monitor your distribution with the script below, but treat it as a **health check**, not a target to hit. There is no official number to aim for.
- If a manual action or Penguin-style drop is suspected from old exact-match spam, use the disavow tool (see `03-off-page-seo/link-schemes.md`) — but only when warranted (S97/S102).

### Link velocity: what to actually do
- Acquire links at whatever rate they come — a viral piece earning hundreds of links in a week is **normal and not penalized** (S106; S109).
- Don't throttle legitimate outreach to "stay under" a made-up monthly cap.
- Do avoid *manipulative* acquisition spikes: buying link bundles, PBN blasts, automated comment spam — those are penalized because the **links are unnatural**, not because they arrived quickly (S97, S109).
- Watch for sudden link spikes in your monitoring tools as a *signal to audit link quality*, not as a ranking risk in themselves.

## Worked example / code

Reproducible anchor-text distribution analyzer. Reads a backlink export with at least an `Anchor` column (e.g., from Ahrefs Site Explorer, Semrush, or GSC Links report). It buckets anchors by type using the taxonomy used in the Ahrefs and Moz studies (S105, S108). **It applies no "safe ratio"** — it only reports the mix so you can sanity-check against Google's spam guidance.

```python
"""
Anchor-text distribution analyzer.
Reproduces the anchor-type taxonomy used in large-scale anchor-text studies
(Ahrefs S105; Moz S108). Reports the distribution only — no official "safe"
ratio is applied, because none has been published by Google.

Requirements: python>=3.11, pandas>=2.0
Usage:
    python anchor_text_audit.py links.csv --brand "Ahrefs" --keyword "seo tool"
"""
import argparse
import re
import pandas as pd

GENERIC = {
    "click here", "here", "this site", "this article", "this website",
    "read more", "learn more", "more", "website", "site", "article",
    "link", "page", "this page", "visit site", "view here", "this post",
}
URL_RE = re.compile(r"https?://|www\.|\.\w{2,}/", re.I)


def classify(anchor: str, brand: str = None, keyword: str = None) -> str:
    a = (anchor or "").strip()
    low = a.lower()
    if not a:
        return "empty"
    if URL_RE.search(a):
        return "naked_url"
    if brand and brand.lower() in low:
        return "branded"
    if low in GENERIC:
        return "generic"
    if keyword:
        kw = keyword.lower()
        toks = re.findall(r"[a-z0-9]+", kw)
        if low == kw:
            return "exact_match"
        if kw in low:
            return "phrase_match"
        if toks and all(t in low for t in toks):
            return "partial_match"
    return "other_keyword"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--anchor-col", default="Anchor")
    ap.add_argument("--brand")
    ap.add_argument("--keyword")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    df["type"] = df[args.anchor_col].apply(lambda x: classify(x, args.brand, args.keyword))
    counts = df["type"].value_counts()
    total = len(df)

    print(f"Total linking anchors analyzed: {total}\n")
    print(f"{'Type':<14}{'Count':>8}{'Share':>10}")
    for t, c in counts.items():
        print(f"{t:<14}{c:>8}{c / total * 100:>9.1f}%")

    if args.keyword:
        em = counts.get("exact_match", 0)
        print(f"\nExact-match share: {em / total * 100:.1f}%")
        print("  (Ahrefs S105: median exact-match share at EVERY ranking")
        print("   position is ~0%. No published 'safe' ceiling exists.)")
    if args.brand:
        br = counts.get("branded", 0) + counts.get("naked_url", 0)
        print(f"Branded + naked-URL share: {br / total * 100:.1f}%")
        print("  (Natural profiles skew heavily branded / naked-URL.)")


if __name__ == "__main__":
    main()
```

**Data source:** export `Anchor` column from Ahrefs Site Explorer → Anchors report, Semrush Backlink Analytics → Anchors, or Bing Webmaster Tools / GSC Links. Pin: `pandas>=2.0`, run on `python>=3.11`.

## Assumptions & limitations
- Anchor text is a **relevance/context** signal, not a guaranteed ranking boost; Google has never published its weight, and correlation studies show it is weak (S105).
- The Ahrefs study (S105) isolates anchor text by selecting SERPs whose top results have similar URL Rating, but **correlation ≠ causation** — pages that rank also tend to attract more/diverse links, so residual confounds remain. The authors disclose this.
- The Google patent (S107) is a *patent application*, not confirmation that the "spiky growth" signal is deployed, weighted, or unchanged today. It describes *sustained* unnatural spikes, not a one-off burst (S106).
- "Natural" anchor distribution varies by niche, page type (homepage vs deep page), and language; Moz's 7:3 heuristic came from a tiny 10-site e-commerce sample and is explicitly "not fact" (S108).
- Google changes how anchor text is weighed over time; treat specifics as dated the day you read them.
- **No guaranteed rankings** follow from any anchor-text strategy.

## Empirical evidence

| Claim | Evidence | Strength |
|---|---|---|
| Exact-match anchor % weakly correlates with rank | Ahrefs: 384,614 pages / 19,840 keywords; Spearman 0.14 (avg) / 0.19 (median) for exact-match; **median exact-match share = 0% at all positions** (S105) | Strong (large n, transparent method, correlation disclosed) |
| Phrase/partial-match anchors even weaker | Ahrefs: Spearman ~0.11 (phrase), ~0.11 (partial) (S105) | Strong |
| Random/generic anchors ~uncorrelated with rank | Ahrefs: Spearman ~0.016 (avg) / 0.013 (median) (S105) | Strong (so "click here" isn't harmful, just unhelpful) |
| Over-optimized exact-match triggered Penguin | Google: Penguin launched Apr 2012, ~3.1% of queries affected (S105); Penguin folded into core algos Sept 2016, now devalues (S104, S33) | Strong (first-party + corroborated) |
| "Natural" profiles skew branded/naked | Moz: 10-site e-commerce study found 34.6% targeted (exact+phrase) overall, but it's a small sample and the author calls it a rough estimate (S108) | Weak–moderate (small n, dated, self-disclosed) |
| Link velocity is not a ranking factor | SEJ review of patent + Mueller ("doesn't really matter how many or in which time") + Illyes ("made-up term") (S106); SEL concurs, owned-media caveat (S109) | Strong for "not a penalty" (multiple Google statements) |

**Sample limitations:** Ahrefs data is keyword-set biased to 2–4 word English queries at 2K–5K searches; excludes non-English and very long-tail. Moz's sample (n=10 sites, 59 pages) is not generalizable. Both studies are correlation-only.

## Conflicting views

- **"Exact-match anchors must stay under 1–5%."** Pushed by many vendor blogs (fatjoe, thehoth, etc.). **Conflicts with** Ahrefs' finding that the *median* top-ranking page has 0% exact-match anchors (S105) and with the absence of any Google-published ratio. Verdict: **folklore** — useful as a "don't be stupid" guardrail, not a law.
- **"Anchor text is still a top-tier ranking factor."** Correlation studies show only a *weak* relationship (S105). It is a genuine relevance signal (S58, original Page/Brin paper) but not a high-weight standalone lever in modern Google. Balanced view: real but minor.
- **"Link velocity will get you penalized."** Directly contradicted by Google reps (S106). The nuance both sides agree on: a spike *from manipulative links* is penalized — but because the links are unnatural, not because of the speed (S97, S109).
- **Sponsored vs editorial on link velocity.** Search Engine Land's piece (S109) is a *sponsored opinion* by a link-building vendor; treat its "monitor your link velocity" advice as vendor perspective, weaker than SEJ's editorial analysis (S106).

## Common mistakes
1. **Keyword-stuffing anchor text** ("best seo tool, seo tool free, buy seo tool" all pointing at one URL) — a spam-policy violation (S97) and classic Penguin trigger.
2. **Engineering a fake ratio** — deliberately varying anchors to hit a "natural" percentage. Google wants *earned* variety; manufactured variety is still manipulation.
3. **Over-using exact-match on guest posts / PBNs** — the highest-risk pattern; default to branded/naked there.
4. **Fear of link velocity** — throttling legitimate PR outreach or worrying a viral week will hurt you. It won't (S106).
5. **Generic anchors everywhere** ("click here") — not penalized, but wastes a free relevance cue (S58).
6. **Reading averages, not medians** — as Ahrefs shows, the *average* exact-match share looks correlated but the *median* is zero; don't be fooled by mean-skew (S105).
7. **Treating a patent as a current feature** — citing the 2003 "spiky growth" patent as proof Google penalizes fast link growth (S107 vs S106).

## Further reading
- **S58** Google Search Central, *SEO Link Best Practices* — what Google asks for in anchor text (developers.google.com/search/docs/crawling-indexing/links-crawlable) — Tier 1
- **S97** Google Search Central, *Spam Policies — Link spam* — exact-match stuffing as a violation (developers.google.com/search/docs/essentials/spam-policies) — Tier 1
- **S33 / S104** Google ranking-systems guide & Penguin history — how unnatural-link demotion works today — Tier 1 / Tier 2
- **S105** Ahrefs, *Anchor Text: A Data-Driven Guide (384,614 Web Pages Studied)* — the core correlation evidence (ahrefs.com/blog/anchor-text) — Tier 2
- **S108** Moz, *Anchor Text Distribution: Avoiding Over Optimization* — heuristic 7:3 and small-sample data (moz.com/blog/anchor-text-distribution-avoiding-over-optimization) — Tier 2
- **S106** Search Engine Journal, *Link Velocity: Is It A Ranking Factor?* — editorial verdict + Mueller/Illyes quotes (searchenginejournal.com/ranking-factors/link-velocity) — Tier 2
- **S107** Google patent US7346839B2, *Information Retrieval Based on Historical Data* — origin of "spiky rate of growth" (patents.google.com/patent/US7346839B2) — Tier 1 (patent, not current-feature confirmation)
- **S109** Search Engine Land, *Understanding link velocity: Truths and myths* — vendor-sponsored perspective, read with caveat (searchengineland.com/understanding-link-velocity-truths-and-myths-442673) — Tier 2 (sponsored)
