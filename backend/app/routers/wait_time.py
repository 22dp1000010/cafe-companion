from fastapi import APIRouter, HTTPException
from app.models.schemas import WaitTimeResponse
from app.firebase import get_firestore, is_firebase_configured, FirebaseNotConfiguredError
from app.config import settings

router = APIRouter(prefix="/api", tags=["wait-time"])


def calculate_wait_time(orders: list[dict], baristas_available: int) -> int:
    """Calculate estimated wait time based on queued orders and their prep times."""

    queued_orders = [o for o in orders if o.get("status") in ["queued", "in_progress"]]

    total_prep_minutes = 0
    for order in queued_orders:
        items = order.get("items", [])
        # Assume max prep time of 5 minutes per item if not specified
        order_prep_time = len(items) * 3
        total_prep_minutes += order_prep_time

    # Distribute prep time across available baristas
    if baristas_available > 0:
        estimated_wait = max(0, (total_prep_minutes // baristas_available))
    else:
        estimated_wait = total_prep_minutes

    return estimated_wait


@router.get("/wait-time", response_model=WaitTimeResponse)
async def get_wait_time():
    """Get estimated wait time for orders."""

    queue_size = 0
    estimated_wait = 0

    if is_firebase_configured():
        try:
            db = get_firestore()
            orders_docs = db.collection("orders").where(
                "status", "in", ["queued", "in_progress"]
            ).stream()
            orders = [doc.to_dict() for doc in orders_docs]
            queue_size = len(orders)
            estimated_wait = calculate_wait_time(orders, settings.baristas_available)
        except FirebaseNotConfiguredError:
            pass

    return WaitTimeResponse(
        estimated_wait_minutes=estimated_wait,
        queue_size=queue_size,
        baristas_available=settings.baristas_available,
    )
