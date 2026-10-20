
import json
from datetime import datetime
from pathlib import Path

from tools import track_order, check_refund_eligibility

REPORT_FILE = Path(__file__).parent / "evaluation_report.json"


# These tests use local Python tools, not Gemini API calls.
TEST_CASES = [
    {
        "name": "Track existing shipped order",
        "run": lambda: track_order("ORD1001"),
        "check": lambda result: (
            result["success"]
            and result["order"]["order_id"] == "ORD1001"
            and result["order"]["status"].lower() == "shipped"
        ),
    },
    {
        "name": "Check eligible refund",
        "run": lambda: check_refund_eligibility("ORD1002"),
        "check": lambda result: (
            result["success"]
            and result["order_id"] == "ORD1002"
            and result["refund_eligible"] is True
        ),
    },
    {
        "name": "Handle unknown order",
        "run": lambda: track_order("ORD9999"),
        "check": lambda result: (
            result["success"] is False
            and "ORD9999" in result["message"]
            and "not found" in result["message"].lower()
        ),
    },
    {
        "name": "Track processing order",
        "run": lambda: track_order("ORD1003"),
        "check": lambda result: (
            result["success"]
            and result["order"]["order_id"] == "ORD1003"
            and result["order"]["status"].lower() == "processing"
        ),
    },
]


def run_evaluation():
    results = []

    print("\nStarting local order-tool evaluation...\n")

    for test in TEST_CASES:
        print(f"Test: {test['name']}")

        try:
            output = test["run"]()
            passed = test["check"](output)

            result = {
                "test_name": test["name"],
                "status": "PASS" if passed else "FAIL",
                "passed": passed,
                "output": output,
                "error": None,
            }

        except Exception as error:
            result = {
                "test_name": test["name"],
                "status": "ERROR",
                "passed": False,
                "output": None,
                "error": str(error),
            }

        results.append(result)

        print("Result:", result["status"])

        if result["output"] is not None:
            print("Output:", result["output"])

        if result["error"]:
            print("Error:", result["error"])

        print("-" * 50)

    passed_count = sum(r["status"] == "PASS" for r in results)
    failed_count = sum(r["status"] == "FAIL" for r in results)
    error_count = sum(r["status"] == "ERROR" for r in results)
    total_count = len(results)

    report = {
        "evaluated_at": datetime.now().isoformat(timespec="seconds"),
        "test_type": "Local Python tool evaluation",
        "total_tests": total_count,
        "passed": passed_count,
        "failed": failed_count,
        "errors": error_count,
        "pass_rate_percent": round(
            passed_count / total_count * 100, 2
        ),
        "results": results,
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\nEvaluation summary")
    print(f"Passed: {passed_count}/{total_count}")
    print(f"Failed: {failed_count}")
    print(f"Errors: {error_count}")
    print(f"Pass rate: {report['pass_rate_percent']}%")
    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    run_evaluation()
