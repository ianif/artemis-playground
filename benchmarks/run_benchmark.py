"""Benchmark for the catalogue pipeline.

Run it from the project root:

    PYTHONPATH=src python3 -u benchmarks/run_benchmark.py

It measures how long a realistic workload takes and writes the numbers to
`artemis_results.json` in the project root, which is where Artemis looks for
custom metrics.

Author: ioanna-from-cli
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from playground import catalogue, pipeline  # noqa: E402

CATALOGUE_SIZE = 20000
LOOKUPS = 8000
REPEATS = 3

# The pipeline must keep returning these, whatever anyone does to make it
# faster. If they change, the optimisation broke the behaviour.
EXPECTED_FOUND = LOOKUPS
EXPECTED_CATEGORIES = 5


def percentile(values, fraction):
    """Simple percentile over a list of numbers."""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * fraction))
    return ordered[index]


def main():
    products = catalogue.build_catalogue(CATALOGUE_SIZE)
    # Spread the ids across the whole catalogue so the linear scan is exercised
    # properly rather than always finding a match near the front.
    lookup_ids = [(i * 7919) % CATALOGUE_SIZE for i in range(LOOKUPS)]

    durations = []
    correct = 1

    for attempt in range(REPEATS):
        started = time.perf_counter()
        stats = pipeline.run_pipeline(products, lookup_ids)
        elapsed = time.perf_counter() - started
        durations.append(elapsed)

        if stats["found_count"] != EXPECTED_FOUND:
            correct = 0
        if stats["categories_ranked"] != EXPECTED_CATEGORIES:
            correct = 0
        if stats["report_length"] <= 0:
            correct = 0

        print("run %d/%d: %.3f s  found=%d" % (attempt + 1, REPEATS, elapsed, stats["found_count"]))

    total_seconds = sum(durations)
    mean_seconds = total_seconds / len(durations)

    results = {
        "total_runtime_ms": round(total_seconds * 1000.0, 3),
        "mean_run_ms": round(mean_seconds * 1000.0, 3),
        "p95_run_ms": round(percentile(durations, 0.95) * 1000.0, 3),
        "lookups_per_second": round((LOOKUPS * REPEATS) / total_seconds, 2),
        "correctness_ok": correct,
    }

    output = os.path.join(os.getcwd(), "artemis_results.json")
    with open(output, "w") as handle:
        json.dump(results, handle, indent=2)

    print("\nwrote %s" % output)
    print(json.dumps(results, indent=2))

    # A broken optimisation should fail the benchmark, not quietly score well.
    return 0 if correct == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
