
import os
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import track_order, check_refund_eligibility

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY or API_KEY == "paste_your_api_key_here":
    raise ValueError(
        "Gemini API key missing. Please add your key to the .env file."
    )

client = genai.Client(api_key=API_KEY)

# Evaluation tracking
LAST_RESPONSE_SOURCE = "unknown"
LAST_API_ERROR = None


def get_fallback_response(message: str):
    """Provide basic answers when Gemini is unavailable."""

    text = message.lower()

    if any(word in text for word in ["cancel", "cancellation"]):
        return (
            "To request an order cancellation, contact customer support "
            "with your order ID as soon as possible. Cancellation may "
            "depend on the order's current status. This demo does not "
            "cancel real orders."
        )

    if any(word in text for word in ["delayed", "delay", "late delivery"]):
        return (
            "If your delivery is delayed, check your order status and "
            "estimated delivery date. If the order is still delayed, "
            "contact customer support with your order ID."
        )

    if any(word in text for word in ["refund", "money back", "return"]):
        return (
            "For a return or refund request, contact customer support "
            "with your order ID. Refund eligibility depends on the "
            "order details and applicable return policy. This demo "
            "can check sample refund eligibility but cannot process "
            "a real refund."
        )

    if any(word in text for word in ["delivery", "deliver", "shipping"]):
        return (
            "You can check your order status using your order ID. "
            "Please share your order ID, for example ORD1001."
        )

    if any(word in text for word in ["order status", "track my order"]):
        return "Please share your order ID, for example ORD1001."

    return None


def get_local_order_response(message: str):
    """Handle order tracking and refund checks without Gemini."""

    text = message.lower()
    match = re.search(r"\bord\d+\b", message, re.IGNORECASE)

    if not match:
        return None

    order_id = match.group(0).upper()

    if any(word in text for word in ["refund", "money back", "return"]):
        result = check_refund_eligibility(order_id)

        if not result["success"]:
            return (
                f"Sorry, we could not find order {order_id}. "
                "Please double-check the order number."
            )

        if result["refund_eligible"]:
            return (
                f"Order {order_id} is eligible for a refund according "
                "to our sample records. No refund has been processed."
            )

        return (
            f"Order {order_id} is not eligible for a refund "
            "according to our sample records."
        )

    result = track_order(order_id)

    if not result["success"]:
        return (
            f"Sorry, we could not find order {order_id}. "
            "Please double-check the order number."
        )

    order = result["order"]

    return (
        f"Order {order['order_id']} is {order['status']}.\n\n"
        f"- Product: {order['product']}\n"
        f"- Estimated delivery: {order['estimated_delivery']}\n"
        f"- Payment status: {order['payment_status']}\n"
        f"- Amount: ₹{order['amount']:,}"
    )


def get_support_response(message: str) -> str:
    """Handle local questions, Gemini responses, and fallback responses."""

    global LAST_RESPONSE_SOURCE, LAST_API_ERROR

    LAST_RESPONSE_SOURCE = "unknown"
    LAST_API_ERROR = None

    # 1. Handle order-specific questions locally.
    local_response = get_local_order_response(message)

    if local_response is not None:
        LAST_RESPONSE_SOURCE = "local_tool"
        return local_response

    # 2. Prepare fallback for common support questions.
    fallback_response = get_fallback_response(message)

    config = types.GenerateContentConfig(
        system_instruction=(
            "You are a helpful e-commerce customer support assistant. "
            "Answer politely in simple language. "
            "Do not invent order details or claim a real refund was processed. "
            "For order-specific facts, ask the customer for an order ID. "
            "Never claim an order was cancelled unless a real cancellation "
            "tool confirms it."
        ),
        temperature=0.2,
    )

    # 3. Ask Gemini.
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config=config,
        )

        if response.text:
            LAST_RESPONSE_SOURCE = "gemini"
            return response.text

        if fallback_response is not None:
            LAST_RESPONSE_SOURCE = "fallback"
            return fallback_response

        LAST_RESPONSE_SOURCE = "empty_response"
        return "Sorry, I couldn't generate a response. Please try again."

    except Exception as error:
        error_text = str(error)
        LAST_API_ERROR = error_text
        print(f"Gemini API error: {error_text}")

        # Use fallback if Gemini fails.
        if fallback_response is not None:
            LAST_RESPONSE_SOURCE = "fallback_after_api_error"
            return fallback_response

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            LAST_RESPONSE_SOURCE = "api_error"
            return (
                "Our AI service has reached its temporary usage limit. "
                "Please try again later. You can still ask about order "
                "tracking and sample refund eligibility."
            )

        if "503" in error_text or "UNAVAILABLE" in error_text:
            LAST_RESPONSE_SOURCE = "api_error"
            return (
                "Our AI service is temporarily busy. "
                "Please try again in a moment."
            )

        if "504" in error_text or "DEADLINE_EXCEEDED" in error_text:
            LAST_RESPONSE_SOURCE = "api_error"
            return "The request took too long. Please try again."

        LAST_RESPONSE_SOURCE = "api_error"
        return (
            "Sorry, I'm unable to process your request right now. "
            "Please try again later."
        )


if __name__ == "__main__":
    question = input("Customer: ")
    print("Assistant:", get_support_response(question))
