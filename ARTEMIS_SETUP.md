# Artemis setup — copy/paste guide

Everything you need to point Artemis at this project.

---

## 1. Scripts for the Project Settings page

Open **Project Settings → Runner and Scripts** and paste these three, exactly as written.

### Build command
```
python3 -m compileall -q src benchmarks tests
```

### Test command
```
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests -q
```

### Benchmark command
```
PYTHONPATH=src python3 -u benchmarks/run_benchmark.py
```

All three were verified on this machine and exit `0`.

### Why they look like that

| Bit | Reason |
|---|---|
| `python3 -m compileall` | This project has no compile step, but Artemis wants a build command. This one byte-compiles every file, so a syntax error fails the build instead of surfacing later as a confusing test error. |
| `PYTHONPATH=src` | The package lives in `src/`. This makes it importable **without installing**, which matters because your machine is PEP 668 "externally managed" — a plain `pip install -e .` is refused. |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` | Your global `site-packages` has a broken `urllib3`. A pytest plugin imports it and crashes collection. This flag stops pytest loading third-party plugins; we don't use any. |
| `-u` | Unbuffered output, so benchmark logs stream into the Artemis UI live instead of arriving in one lump at the end. |

### Nicer variant (optional, needs one sudo)

If you'd rather use a proper virtual environment:

```bash
sudo apt install python3.12-venv
```

Then the three commands become:

```
python3 -m venv .venv && .venv/bin/python -m pip install --quiet --upgrade pip && .venv/bin/python -m pip install --quiet -e ".[dev]"
```
```
.venv/bin/python -m pytest tests -q
```
```
.venv/bin/python -u benchmarks/run_benchmark.py
```

This is cleaner (no env-var workarounds) but adds ~10 s to every build, because Artemis copies the repo to a **fresh temporary folder for every run** — nothing is cached between runs.

---

## 2. How Artemis runs these

1. You press Run in the web UI.
2. Your runner picks up the job.
3. Artemis copies the whole repo to `.artemis/{task-id}/.../project/`.
4. Your command runs **inside that folder** — it is the working directory.
5. Logs stream back to the UI.

Two consequences worth remembering:

- Every run starts clean. No leftovers from last time.
- Paths must be relative to the project root. Don't hardcode `/home/ioanna/...`.

---

## 3. Custom metrics

The benchmark writes `artemis_results.json` to the **project root** before exiting. Artemis picks it up automatically.

```json
{
  "total_runtime_ms": 4249.689,
  "mean_run_ms": 1416.563,
  "p95_run_ms": 1429.443,
  "lookups_per_second": 5647.47,
  "correctness_ok": 1
}
```

Rules that matter:

- Filename must be exactly `artemis_results.json` (or `.csv`).
- It must sit in the working directory, **not** a subfolder.
- **Every value must be a number.** No strings, no `true`/`false`, no nesting. That's why correctness is `1`/`0` rather than `true`/`false`.
- Metric names must stay spelled identically between runs, or Artemis sees them as different metrics.

---

## 4. Connecting the project

Artemis needs the code in a Git repository it can reach.

```bash
cd artemis-playground
git init
git add .
git commit -m "Artemis practice project"
git branch -M main
git remote add origin git@github.com:<you>/artemis-playground.git
git push -u origin main
```

Then in Artemis: **New project → paste the repo URL → pick your runner**.

---

## 5. Order to do things in

1. Run the three commands **in a plain terminal first**. If they don't work there, they won't work on the runner.
2. Paste them into Project Settings.
3. Press Run on each one and watch the logs.
4. Go to **Maintain** → run a Scan → triage what it finds.
5. Go to **Discover** → set an objective → complete setup → let it optimise.
