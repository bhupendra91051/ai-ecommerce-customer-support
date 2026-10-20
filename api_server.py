
from fastapi import FastAPI, HTTPException
from tools import track_order, check_refund_eligibility

app = FastAPI(
    title="E-commerce Customer Support API",
    description="API for tracking orders and checking refund eligibility",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "E-commerce Customer Support API is running"
    }


@app.get("/order/{order_id}")
def get_order(order_id: str):
    result = track_order(order_id)

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])

    return result


@app.get("/refund/{order_id}")
def get_refund_status(order_id: str):
    result = check_refund_eligibility(order_id)

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])

    return result
