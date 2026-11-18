"""
Automated Verification Suite for CellRank Lineage Benchmark
Tests:
  1. Golden Solution Verification (Id2 @ 0.7579 -> Expected: PASS, Score: 1.0)
  2. Trap 1 Verification (Ccl5 Static DE -> Expected: FAIL, Trap 1 Identified)
  3. Trap 2 Verification (Cd74 Global Pseudotime -> Expected: FAIL, Trap 2 Identified)
"""

import os
import json
import tempfile
from pathlib import Path
from evaluator import evaluate

def test_golden_solution():
    print("\n[TEST 1] Testing Golden Solution Output...")
    payload = {
        "terminal_state": "0",
        "top_driver_gene": "Id2",
        "correlation": 0.7579
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        res = evaluate(temp_path)
        print(f"Result: passed_all={res['passed_all']}, score={res['score']}")
        assert res["passed_all"] is True, "Golden solution failed to pass evaluation!"
        assert res["rule_1_schema"] is True
        assert res["rule_2_gene"] is True
        assert res["rule_3_correlation"] is True
        print(">>> Golden Solution PASSED (1.0/1.0)")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_trap_1_static_de():
    print("\n[TEST 2] Testing Trap 1 (Static Differential Expression: Ccl5)...")
    payload = {
        "terminal_state": "0",
        "top_driver_gene": "Ccl5",
        "correlation": 0.88
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        res = evaluate(temp_path)
        print(f"Result: passed_all={res['passed_all']}, score={res['score']}")
        print(f"Feedback: {res['failure_reason']}")
        assert res["passed_all"] is False, "Trap 1 was unexpectedly marked as passed!"
        assert "Trap 1" in res["failure_reason"]
        print(">>> Trap 1 correctly caught and failed.")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_trap_2_global_pseudotime():
    print("\n[TEST 3] Testing Trap 2 (Global Pseudotime Shortcut: Cd74 @ 0.477)...")
    payload = {
        "terminal_state": "0",
        "top_driver_gene": "Cd74",
        "correlation": 0.477
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        res = evaluate(temp_path)
        print(f"Result: passed_all={res['passed_all']}, score={res['score']}")
        print(f"Feedback: {res['failure_reason']}")
        assert res["passed_all"] is False, "Trap 2 was unexpectedly marked as passed!"
        assert "Trap 2" in res["failure_reason"]
        print(">>> Trap 2 correctly caught and failed.")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    print("==================================================")
    print("Running Benchmark Verification & Trap Evaluation")
    print("==================================================")
    test_golden_solution()
    test_trap_1_static_de()
    test_trap_2_global_pseudotime()
    print("\n==================================================")
    print("ALL 3 BENCHMARK EVALUATION TESTS PASSED PERFECTLY!")
    print("==================================================")
