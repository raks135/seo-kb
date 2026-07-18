#!/usr/bin/env python3
"""rank_traffic_model.py — estimate organic clicks from a tracked average
position under the First Page Sage 2026 CTR-by-position curve (S221),
with optional AI-Overview / zero-click modifiers.

Stdlib only. Python 3.8+.
Usage:
    python3 rank_traffic_model.py --impressions 10000 --position 1
    python3 rank_traffic_model.py --impressions 10000 --position 3 --aio
    python3 rank_traffic_model.py --demo
"""
import argparse

# Organic CTR by position, Google "All" SERP with no other elements (S221, 2025).
CTR_BY_POSITION = {
    1: 0.398, 2: 0.187, 3: 0.102, 4: 0.072, 5: 0.051,
    6: 0.044, 7: 0.030, 8: 0.021, 9: 0.019, 10: 0.016,
}

def ctr_for_position(pos, aio_present=False):
    """Linear-interpolate the CTR curve for a (possibly fractional) position."""
    if pos < 1.0:
        pos = 1.0
    if pos > 10.0:
        pos = 10.0
    lo = int(pos)
    hi = min(10, lo + 1)
    if hi == lo:
        base = CTR_BY_POSITION[lo]
    else:
        frac = pos - lo
        base = CTR_BY_POSITION[lo] * (1 - frac) + CTR_BY_POSITION[hi] * frac
    if aio_present:
        # S219/S221: an AI Overview reduces organic CTR by ~60% when present.
        base *= 0.40
    return base

def estimate_clicks(impressions, position, aio_present=False):
    return int(round(impressions * ctr_for_position(position, aio_present)))

def demo():
    print(f"{'Pos':>3} | {'CTR (no AIO)':>12} | {'Clicks/10k':>10} | {'CTR (AIO)':>10} | {'Clicks/10k (AIO)':>16}")
    print("-" * 72)
    for p in range(1, 11):
        ctr = ctr_for_position(float(p))
        ctr_aio = ctr_for_position(float(p), aio_present=True)
        print(f"{p:>3} | {ctr*100:>11.1f}% | {estimate_clicks(10000, p):>10} | "
              f"{ctr_aio*100:>9.1f}% | {estimate_clicks(10000, p, aio_present=True):>16}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--impressions", type=int, default=10000)
    ap.add_argument("--position", type=float, default=1.0)
    ap.add_argument("--aio", action="store_true", help="apply AI-Overview CTR penalty")
    ap.add_argument("--demo", action="store_true", help="print the full position table")
    args = ap.parse_args()
    if args.demo:
        demo()
    else:
        ctr = ctr_for_position(args.position, args.aio)
        clicks = estimate_clicks(args.impressions, args.position, args.aio)
        print(f"Position {args.position:.1f} | CTR {ctr*100:.1f}% | "
              f"~{clicks} clicks per {args.impressions:,} impressions"
              f"{' (AI Overview present)' if args.aio else ''}")
