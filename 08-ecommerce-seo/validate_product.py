import json, sys

def validate_product(data: dict) -> list:
    """Return a list of human-readable issues for a Product JSON-LD dict."""
    issues = []
    if data.get("@type") not in ("Product", ["Product"]):
        issues.append("Root @type is not 'Product'")
    for req in ("name", "image"):
        if req not in data or not data.get(req):
            issues.append(f"Product missing required '{req}'")
    offer = data.get("offers")
    if not isinstance(offer, dict):
        issues.append("Merchant listings require an 'offers' Offer object (not AggregateOffer)")
    elif offer.get("@type") == "AggregateOffer":
        issues.append("Merchant listings require a single 'Offer' object, not 'AggregateOffer'")
    else:
        ps = offer.get("priceSpecification") or {}
        price = offer.get("price")
        if price is None:
            price = ps.get("price")
        curr = offer.get("priceCurrency")
        if curr is None:
            curr = ps.get("priceCurrency")
        if price is None:
            issues.append("Offer missing required 'price' (or priceSpecification.price)")
        elif isinstance(price, (int, float)) and price <= 0:
            issues.append("Merchant listings require price > 0")
        if not curr:
            issues.append("Offer missing required 'priceCurrency'")
    ar = data.get("aggregateRating")
    if isinstance(ar, dict) and "ratingCount" not in ar and "reviewCount" not in ar:
        issues.append("aggregateRating present but missing ratingCount/reviewCount (will be ignored/invalid)")
    return issues

if __name__ == "__main__":
    blob = json.load(sys.stdin)
    node = blob
    if isinstance(blob, dict) and "@graph" in blob:
        node = next((n for n in blob["@graph"] if n.get("@type") == "Product"), {})
    found = validate_product(node)
    print("OK" if not found else "ISSUES:\n- " + "\n- ".join(found))
