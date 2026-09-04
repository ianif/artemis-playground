# What is deliberately wrong in this project

Read this **after** running a Maintain scan, then compare. Anything here that
Maintain missed is a gap in your rules; anything Maintain found that isn't here
is worth checking — it may be a real find, or a false positive to triage.

## Performance (7) — Discovery should fix these

| # | File | What | Cost |
|---|---|---|---|
| P1 | `search.py` `find_product_by_id` | Linear scan of the whole list per lookup | O(n) per call, ~80M steps per benchmark run |
| P2 | `search.py` `find_products_by_category` | Rebuilds the filtered list on every call | Repeated full scans |
| P3 | `ranking.py` `top_rated` | Full sort of the catalogue to take 10 items | O(n log n) where O(n) would do |
| P4 | `ranking.py` `cheapest` | Same full sort, again | Doubles P3 |
| P5 | `cache.py` `SimpleCache.get/put` | Recency kept in a list, scanned with `.index()` | O(n) per cache operation |
| P6 | `report.py` `build_report` | Builds output by repeated string concatenation | Copies the whole string per line |
| P7 | `pipeline.py` `run_pipeline` | Re-ranks per category inside a loop | Multiplies P3 by 5 |

## Security (6) — Maintain's security rule should flag these

| # | File | What |
|---|---|---|
| S1 | `security_utils.py` | API key and admin password hardcoded in source |
| S2 | `security_utils.py` `hash_password` | MD5, unsalted, for passwords |
| S3 | `security_utils.py` `generate_session_token` | `random` instead of `secrets` for tokens |
| S4 | `security_utils.py` `evaluate_discount_rule` | `eval()` on caller-supplied text |
| S5 | `security_utils.py` `check_disk_usage` | `subprocess` with `shell=True` and string interpolation |
| S6 | `db.py` `find_by_category` | SQL built by string concatenation — injection |

Note `db.py` `insert_products` does it **correctly** with bound parameters, so
the same file contains both the right and wrong pattern. A good rule flags one
and not the other.

## Spelling (5)

| # | File | Wrong | Right |
|---|---|---|---|
| W1 | `report.py` | `seperator` | `separator` |
| W2 | `report.py` | `occured_errors` | `occurred_errors` |
| W3 | `report.py` | `lenght` | `length` |
| W4 | `report.py` | `succesful` | `successful` |
| W5 | `report.py` | "succesful" in output text | "successful" |

`test_report.py` pins the misspelt output on purpose — fixing W5 should make a
test fail, which is exactly the conversation you want a fix agent to have.

## General mistakes (3)

| # | File | What |
|---|---|---|
| G1 | `pipeline.py` `collect_ids` | Mutable default argument `results=[]` |
| G2 | `pipeline.py` `run_pipeline` | Bare `except:` swallowing everything |
| G3 | `pipeline.py` | `os` and `sys` imported but never used |

## Suggested Maintain rules

Create these in **Maintain → Rules** to catch the above:

1. **Performance inefficiencies** — linear scans where a dict lookup would do, repeated sorting, string concatenation in loops.
2. **Common security weaknesses** — hardcoded credentials, weak hashing, `eval`, `shell=True`, SQL built by concatenation, `random` for secrets.
3. **Spelling in identifiers and comments** — flag misspelt words in names, docstrings and user-facing strings.
4. **Python correctness smells** — mutable default arguments, bare `except`, unused imports.
