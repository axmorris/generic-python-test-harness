# Generic Python Test Harness

I originally built this generic test harness to learn and practice more advanced Python concepts. At the time, I was reading "Fluent Python: Clear, Concise, and Effective Programming" by Luciano Ramalho. (If you haven't read it, I recommend it!) This was version 1. This repository is intentionally a small historical sample, and is not a modern test framework or a replacement for any of the recommended Python testing standards.

I later expanded upon this to build more substantial automated test frameworks that were used for system testing and regression testing for real production systems that exercised both Python and C++ applications. (That implementation is proprietary and is not included here).

Ultimately, I replaced my custom framework with `pytest`, which is what I would use and recommend today.

## What this version does

This bare-bones implementation does the following:

- `TestDriver` owns a list of tests.
- `Test` groups one or more test cases and optional setup/teardown.
- `TestCase` wraps a Python callable and records its result and duration.
- `ResultWriter` writes results to a local JSON-lines file. (My productionized versions wrote to MySQL databases).

## Run it

```bash
python3 example.py
```

```bash
TestResult(description='test_one', duration=datetime.timedelta(microseconds=2), success=True)
TestResult(description='test_two', duration=datetime.timedelta(microseconds=1), success=True)
PASS
```

The example writes results to `results.jsonl`.

```bash
{"timestamp": "2026-08-23T11:33:33", "description": "test_one", "success": true, "duration_seconds": 3e-06}
{"timestamp": "2026-08-23T11:33:33", "description": "test_two", "success": true, "duration_seconds": 1e-06}
{"timestamp": "2026-08-23T11:34:20", "description": "test_one", "success": true, "duration_seconds": 2e-06}
{"timestamp": "2026-08-23T11:34:20", "description": "test_two", "success": true, "duration_seconds": 1e-06}
```
