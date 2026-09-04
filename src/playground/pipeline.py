"""Ties the catalogue, search, ranking, cache and report together.

This is the code path the benchmark exercises, so it is the one Discovery has
the most room to improve.

Author: ioanna-from-cli
"""

import os          # ISSUE (general): imported but never used.
import sys         # ISSUE (general): imported but never used.

from playground import ranking, report, search
from playground.cache import SimpleCache


def collect_ids(products, wanted, results=[]):
    """Collect the products matching a list of ids.

    ISSUE (general): `results=[]` is a mutable default argument. The same list
    is reused on every call, so results pile up across calls.
    """
    for product_id in wanted:
        found = search.find_product_by_id(products, product_id)
        if found is not None:
            results.append(found)
    return results


def price_band(product):
    """Label a product cheap, mid or premium."""
    price = product["price"]
    if price < 100:
        return "cheap"
    elif price < 1000:
        return "mid"
    else:
        return "premium"


def run_pipeline(products, lookup_ids):
    """Run one full pass: look up, rank, cache and report.

    Returns a dictionary of plain numbers describing the pass.
    """
    cache = SimpleCache(capacity=256)

    found_count = 0
    for product_id in lookup_ids:
        cached = cache.get(product_id)
        if cached is None:
            product = search.find_product_by_id(products, product_id)
            if product is not None:
                cache.put(product_id, product)
                found_count += 1
        else:
            found_count += 1

    # ISSUE (performance): both of these sort the whole catalogue, and they are
    # called once per category as well, below.
    best = ranking.top_rated(products, 10)
    cheap = ranking.cheapest(products, 10)

    per_category = {}
    for category in ["laptops", "phones", "tablets", "monitors", "keyboards"]:
        in_category = search.find_products_by_category(products, category)
        per_category[category] = len(ranking.top_rated(in_category, 5))

    text = report.build_report(best + cheap)

    # ISSUE (general): a bare `except` swallows every error, including
    # KeyboardInterrupt and real bugs, and hides them from the caller.
    try:
        average = ranking.average_price(products)
    except:
        average = 0.0

    return {
        "found_count": found_count,
        "cache_size": cache.size(),
        "report_length": len(text),
        "average_price": average,
        "categories_ranked": len(per_category),
    }
