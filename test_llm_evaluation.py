
import json
from datetime import datetime
from pathlib import Path

import assistant

REPORT_FILE = Path(__file__).parent / "llm_evaluation_report.json"

TEST_CASES = [
    {
        "name": "Order cancellation guidance",
        "question": "How can I cancel an order?",
        "expected_keywords": ["order", "cancel"],
    },
    {
        "name": "Delayed delivery guidance",
        "question": "What should I do if my order is delayed?",
        "expected_keywords": ["order", "delivery"],
    },
    {
        "name": "Missing order ID",
        "question": "Can you check my order status?",
        "expected_keywords": ["order", "id"],
    },
]


def evaluate_response(response, expected_keywords):
    """Basic keyword check for a non-empty LLM response."""

    if not isinstance(response, str) or not response.strip():
        return False, [], list(expected_keywords)

    response_lower = response.lower()

    matched = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in response_lower
    ]

    missing = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() not in response_lower
    ]

    return len(missing) == 0, matched, missing


def run_evaluation():
    results = []

    print("\nStarting LLM Evaluation")
    print("=" * 55)

    for index, test in enumerate(TEST_CASES, start=1):
        print(f"\nTest {index}/{len(TEST_CASES)}: {test['name']}")

        try:
            response = assistant.get_support_response(
                test["question"]
            )

            # Read updated values from the assistant module.
            source = getattr(
                assistant, "LAST_RESPONSE_SOURCE", "unknown"
            )
            api_error = getattr(
                assistant, "LAST_API_ERROR", None
            )

            response_text = (
                response if isinstance(response, str)
                else str(response) if response is not None
                else ""
            )

            matched = []
            missing = list(test["expected_keywords"])
            passed = False

            if source == "gemini":
                passed, matched, missing = evaluate_response(
                    response_text,
                    test["expected_keywords"],
                )
                status = "PASS" if passed else "FAIL"
                details = (
                    "All expected keywords matched."
                    if passed
                    else f"Missing expected keywords: {missing}"
                )

            elif source == "fallback_after_api_error":
                status = "API_ERROR"
                details = (
                    "Gemini failed; fallback response was used. "
                    "This is not a successful LLM evaluation."
                )

            elif source == "fallback":
                status = "FALLBACK"
                details = (
                    "Fallback response used; not counted as an "
                    "LLM evaluation."
                )

            elif source == "local_tool":
                status = "LOCAL_TOOL"
                details = (
                    "Local tool response; not counted as an "
                    "LLM evaluation."
                )

            elif source == "api_error":
                status = "API_ERROR"
                details = "The assistant reported an API error."

            else:
                status = "OTHER"
                details = f"Unrecognized response source: {source}"

            result = {
                "test_name": test["name"],
                "question": test["question"],
                "status": status,
                "response_source": source,
                "response": response_text,
                "api_error": str(api_error) if api_error else None,
                "matched_keywords": matched,
                "missing_keywords": missing,
                "evaluation_details": details,
            }

        except Exception as error:
            result = {
                "test_name": test["name"],
                "question": test["question"],
                "status": "ERROR",
                "response_source": "unknown",
                "response": None,
                "api_error": None,
                "matched_keywords": [],
                "missing_keywords": test["expected_keywords"],
                "evaluation_details": (
                    f"{type(error).__name__}: {error}"
                ),
            }

        results.append(result)

        print("Status:", result["status"])
        print("Source:", result["response_source"])
        print("Response:", result["response"])

        if result["api_error"]:
            print("API error:", result["api_error"])

        print("Details:", result["evaluation_details"])
        print("-" * 55)

    statuses = [
        "PASS",
        "FAIL",
        "FALLBACK",
        "API_ERROR",
        "LOCAL_TOOL",
        "OTHER",
        "ERROR",
    ]

    counts = {
        status: sum(
            result["status"] == status for result in results
        )
        for status in statuses
    }

    # Only actual Gemini responses count toward LLM accuracy.
    llm_tests_evaluated = counts["PASS"] + counts["FAIL"]

    accuracy = (
        round(counts["PASS"] / llm_tests_evaluated * 100, 2)
        if llm_tests_evaluated
        else None
    )

    evaluation_complete = (
        llm_tests_evaluated == len(TEST_CASES)
        and counts["ERROR"] == 0
    )

    report = {
        "evaluated_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "evaluation_type": (
            "Basic keyword matching on Gemini responses; "
            "not a comprehensive quality or correctness evaluation."
        ),
        "total_tests_planned": len(TEST_CASES),
        "total_tests_run": len(results),
        "llm_tests_evaluated": llm_tests_evaluated,
        "passed": counts["PASS"],
        "failed": counts["FAIL"],
        "llm_keyword_accuracy_percent": accuracy,
        "evaluation_complete": evaluation_complete,
        "fallback_responses": counts["FALLBACK"],
        "api_errors": counts["API_ERROR"],
        "local_tool_responses": counts["LOCAL_TOOL"],
        "other_responses": counts["OTHER"],
        "unexpected_errors": counts["ERROR"],
        "tests_not_run": len(TEST_CASES) - len(results),
        "results": results,
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 55)
    print("EVALUATION SUMMARY")
    print("=" * 55)
    print("Tests planned:", report["total_tests_planned"])
    print("Tests run:", report["total_tests_run"])
    print("LLM tests evaluated:", llm_tests_evaluated)
    print("Passed:", counts["PASS"])
    print("Failed:", counts["FAIL"])
    print("Fallback responses:", counts["FALLBACK"])
    print("API errors:", counts["API_ERROR"])
    print("Local tool responses:", counts["LOCAL_TOOL"])
    print("Other responses:", counts["OTHER"])
    print("Unexpected errors:", counts["ERROR"])

    if accuracy is None:
        print("LLM keyword accuracy: N/A (no valid Gemini responses)")
    else:
        print(f"LLM keyword accuracy: {accuracy}%")

    print("Evaluation complete:", evaluation_complete)
    print("Report saved to:", REPORT_FILE)

    if not evaluation_complete:
        print(
            "\nEvaluation is INCOMPLETE. Successful Gemini responses "
            "are required for every test."
        )


if __name__ == "__main__":
    run_evaluation()
