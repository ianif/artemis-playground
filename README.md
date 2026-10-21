# artemis-playground

A small, deliberately imperfect product-catalogue tool, built as a practice
target for **Artemis Maintain** (find and fix issues) and **Artemis Discovery**
(make it faster).

Everything here works and every test passes — the problems are real but none of
them are crashes. That is on purpose: Discovery can only prove an optimisation
is safe if the tests were green to begin with.

**Setup instructions live in [ARTEMIS_SETUP.md](ARTEMIS_SETUP.md).**

## What it does

Builds a catalogue of 20,000 products, then repeatedly looks products up, ranks
them, caches them and prints a report.

```
src/playground/
  catalogue.py       builds the product data
  search.py          looks products up
  ranking.py         sorts by rating and price
  cache.py           a small LRU cache
  report.py          renders a text report
  pipeline.py        runs all of the above  <- the hot path
  security_utils.py  deliberately weak security helpers
  db.py              a tiny SQLite layer
```

## Running it yourself

```bash
python3 -m compileall -q src benchmarks tests                                  # build
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests -q     # tests
PYTHONPATH=src python3 -u benchmarks/run_benchmark.py                          # benchmark
```

Expect 21 passing tests and a benchmark around 4 seconds.

## The issues planted in it

There are **21 deliberate issues** across four categories. Full map in
[ISSUES.md](ISSUES.md) — read that *after* you've let Maintain scan, so you can
compare what it found against what is actually there.
QA-MT 21 Oct 3018b round trip edit
QA-MT 21 Oct 3018b TC-10b never published
