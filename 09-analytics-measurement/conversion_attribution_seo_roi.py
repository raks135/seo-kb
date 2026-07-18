#!/usr/bin/env python3
# conversion_attribution_seo_roi.py
# Stdlib only. Python 3.8+. DEMO DATA — replace with your GA4/CRM export.
# Companion to conversion-attribution-seo-roi.md.
from collections import defaultdict


def seo_roi(organic_revenue, seo_cost):
    """ROI as a percentage: (revenue - cost) / cost * 100."""
    if seo_cost <= 0:
        raise ValueError("SEO cost must be > 0")
    return (organic_revenue - seo_cost) / seo_cost * 100.0


# Five conversions; each path lists channels touched, in order.
CONVERSIONS = [
    {"path": ["organic", "organic", "branded_search"], "value": 2000.0},
    {"path": ["organic", "retargeting_ad", "direct"], "value": 2000.0},
    {"path": ["organic", "email", "branded_search"], "value": 2000.0},
    {"path": ["paid_search"], "value": 2000.0},
    {"path": ["direct"], "value": 2000.0},
]
MONTHLY_SEO_COST = 3000.0


def attribute(convs, model):
    totals = defaultdict(float)
    for c in convs:
        path, value, n = c["path"], c["value"], len(c["path"])
        if model == "last_click":
            credit = {path[-1]: 1.0}
        elif model == "first_click":
            credit = {path[0]: 1.0}
        elif model == "linear":
            credit = {ch: 1.0 / n for ch in path}
        elif model == "position":  # 40% first, 40% last, 20% split across middle
            credit = defaultdict(float)
            credit[path[0]] += 0.4
            credit[path[-1]] += 0.4
            if n > 2:
                for ch in path[1:-1]:
                    credit[ch] += 0.2 / (n - 2)
        else:
            raise ValueError(model)
        for ch, w in credit.items():
            totals[ch] += value * w
    return dict(totals)


if __name__ == "__main__":
    print("model         | organic attributed | SEO ROI")
    for m in ["last_click", "first_click", "linear", "position"]:
        a = attribute(CONVERSIONS, m)
        org = a.get("organic", 0.0)
        print(f"{m:12s} | ${org:8.0f}          | {seo_roi(org, MONTHLY_SEO_COST):6.1f}%")
