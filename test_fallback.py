
from assistant import get_fallback_response

test_cases = [
    (
        "Cancellation",
        "How can I cancel an order?",
        ["cancel", "customer support"],
    ),
    (
        "Delayed delivery",
        "What should I do if my order is delayed?",
        ["delayed", "order id"],
    ),
    (
        "Refund guidance",
        "Can I get my money back?",
        ["refund", "order id"],
    ),
    (
        "Delivery guidance",
        "Where can I find delivery details?",
        ["order id"],
    ),
]

passed = 0
failed = 0

for name, question, keywords in test_cases:
    response = get_fallback_response(question)

    if response and all(
        word in response.lower() for word in keywords
    ):
        print(f"PASS: {name}")
        passed += 1
    else:
        print(f"FAIL: {name}")
        print(f"Response: {response}")
        failed += 1

print("\n--- Fallback Evaluation ---")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total: {len(test_cases)}")
