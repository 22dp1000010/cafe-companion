from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.firebase import get_firestore, is_firebase_configured, FirebaseNotConfiguredError
from app.gemini import get_gemini_client
from datetime import datetime
import uuid

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and optionally create an order."""

    try:
        gemini_client = get_gemini_client()
    except ValueError:
        raise HTTPException(
            status_code=503,
            detail="Gemini API not configured. Set GEMINI_API_KEY environment variable.",
        )

    # Get user data and menu (if Firebase configured)
    user_name = "Friend"
    menu = []
    order_history = []
    preferences = []

    if is_firebase_configured():
        try:
            db = get_firestore()
            user_doc = db.collection("users").document(request.user_id).get()
            if user_doc.exists():
                user_data = user_doc.to_dict()
                user_name = user_data.get("name", "Friend")
                order_history = user_data.get("order_history", [])
                preferences = user_data.get("preferences", [])

            menu_docs = db.collection("menu").stream()
            menu = [doc.to_dict() for doc in menu_docs]
        except FirebaseNotConfiguredError:
            pass
    else:
        # Use default menu if Firebase not available
        menu = [
            {
                "id": "espresso",
                "name": "Espresso",
                "description": "Classic espresso shot",
                "price": 2.50,
                "category": "coffee",
                "prepTimeMinutes": 2,
            },
            {
                "id": "latte",
                "name": "Latte",
                "description": "Espresso with steamed milk",
                "price": 4.00,
                "category": "coffee",
                "prepTimeMinutes": 3,
            },
            {
                "id": "cappuccino",
                "name": "Cappuccino",
                "description": "Espresso with equal parts steamed milk and foam",
                "price": 4.00,
                "category": "coffee",
                "prepTimeMinutes": 3,
            },
        ]

    # Get Gemini response
    response_data = gemini_client.chat_with_recommendations(
        user_message=request.message,
        user_name=user_name,
        menu=menu,
        order_history=order_history,
        preferences=preferences,
    )

    # If order intent detected and Firebase configured, save order
    if response_data["order_intent"] and is_firebase_configured():
        try:
            db = get_firestore()
            order_id = str(uuid.uuid4())[:8]
            order_doc = {
                "id": order_id,
                "user_id": request.user_id,
                "items": response_data["order_intent"].get("items", []),
                "status": "queued",
                "created_at": datetime.now(),
                "instructions": response_data["order_intent"].get("instructions", ""),
                "total_price": sum(
                    [item["price"] for item in menu if item["name"] in response_data["order_intent"].get("items", [])]
                ),
            }
            db.collection("orders").document(order_id).set(order_doc)
        except Exception as e:
            response_data["reply"] += f"\n(Order saved locally but backend error: {str(e)})"

    return ChatResponse(
        reply=response_data["reply"],
        order_intent=response_data["order_intent"],
        recommendation=response_data["recommendation"],
    )
