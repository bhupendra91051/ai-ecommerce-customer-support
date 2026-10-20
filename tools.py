
import json
from pathlib import Path

# Locate the sample orders file
DATA_FILE = Path(__file__).parent / "data" / "orders.json"


def load_orders():
    """Load order records from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def track_order(order_id: str) -> dict:
    """Return order details for a given order ID."""
    orders = load_orders()
    order_id = order_id.strip().upper()

    if order_id not in orders:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    return {
        "success": True,
        "order": orders[order_id]
    }


def check_refund_eligibility(order_id: str) -> dict:
    """Check the sample refund eligibility flag for an order."""
    result = track_order(order_id)

    if not result["success"]:
        return result

    order = result["order"]

    return {
        "success": True,
        "order_id": order["order_id"],
        "refund_eligible": order["refund_eligible"],
        "message": (
            "This order is eligible for a refund."
            if order["refund_eligible"]
            else "This order is not eligible for a refund."
        )
    }
