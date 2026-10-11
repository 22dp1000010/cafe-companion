"""Script to seed sample menu and demo users into Firestore."""

import sys
from datetime import datetime
from app.firebase import get_firestore, is_firebase_configured


def seed_menu(db):
    """Seed sample menu items."""
    menu_items = [
        {
            "id": "espresso",
            "name": "Espresso",
            "description": "Classic single or double shot",
            "price": 2.50,
            "category": "coffee",
            "prepTimeMinutes": 2,
        },
        {
            "id": "latte",
            "name": "Latte",
            "description": "Smooth espresso with steamed milk and foam",
            "price": 4.00,
            "category": "coffee",
            "prepTimeMinutes": 3,
        },
        {
            "id": "cappuccino",
            "name": "Cappuccino",
            "description": "Rich espresso with equal parts steamed milk and foam",
            "price": 4.00,
            "category": "coffee",
            "prepTimeMinutes": 3,
        },
        {
            "id": "americano",
            "name": "Americano",
            "description": "Espresso shots with hot water",
            "price": 3.00,
            "category": "coffee",
            "prepTimeMinutes": 2,
        },
        {
            "id": "macchiato",
            "name": "Macchiato",
            "description": "Espresso with a small amount of steamed milk",
            "price": 3.50,
            "category": "coffee",
            "prepTimeMinutes": 2,
        },
        {
            "id": "cold_brew",
            "name": "Cold Brew",
            "description": "Smooth cold brew coffee",
            "price": 3.50,
            "category": "coffee",
            "prepTimeMinutes": 1,
        },
        {
            "id": "cappuccino_iced",
            "name": "Iced Cappuccino",
            "description": "Cappuccino served over ice",
            "price": 4.50,
            "category": "coffee",
            "prepTimeMinutes": 3,
        },
        {
            "id": "matcha_latte",
            "name": "Matcha Latte",
            "description": "Creamy matcha green tea with milk",
            "price": 5.00,
            "category": "tea",
            "prepTimeMinutes": 2,
        },
        {
            "id": "chai_latte",
            "name": "Chai Latte",
            "description": "Spiced tea with steamed milk",
            "price": 4.50,
            "category": "tea",
            "prepTimeMinutes": 3,
        },
        {
            "id": "croissant",
            "name": "Croissant",
            "description": "Buttery flaky pastry",
            "price": 3.50,
            "category": "pastry",
            "prepTimeMinutes": 1,
        },
        {
            "id": "muffin_blueberry",
            "name": "Blueberry Muffin",
            "description": "Fresh blueberry muffin",
            "price": 3.00,
            "category": "pastry",
            "prepTimeMinutes": 1,
        },
        {
            "id": "sandwich_turkey",
            "name": "Turkey Sandwich",
            "description": "Roasted turkey with avocado and tomato",
            "price": 8.50,
            "category": "food",
            "prepTimeMinutes": 5,
        },
    ]

    for item in menu_items:
        db.collection("menu").document(item["id"]).set(item)

    print(f"Seeded {len(menu_items)} menu items")


def seed_users(db):
    """Seed demo users with preferences and order history."""
    users = [
        {
            "id": "user_001",
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "preferences": ["latte", "cappuccino", "croissant"],
            "order_history": ["latte", "cappuccino", "croissant"],
            "interests": ["reading", "photography", "hiking"],
            "opted_in_matching": True,
        },
        {
            "id": "user_002",
            "name": "Bob Smith",
            "email": "bob@example.com",
            "preferences": ["espresso", "americano"],
            "order_history": ["espresso", "americano", "blueberry muffin"],
            "interests": ["hiking", "coding", "music"],
            "opted_in_matching": True,
        },
        {
            "id": "user_003",
            "name": "Carol Davis",
            "email": "carol@example.com",
            "preferences": ["chai latte", "matcha latte"],
            "order_history": ["chai latte", "turkey sandwich"],
            "interests": ["yoga", "photography", "cooking"],
            "opted_in_matching": True,
        },
    ]

    for user in users:
        db.collection("users").document(user["id"]).set(user)

    print(f"Seeded {len(users)} demo users")


if __name__ == "__main__":
    if not is_firebase_configured():
        print("Error: Firebase not configured")
        print("Set FIREBASE_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS environment variables")
        sys.exit(1)

    try:
        db = get_firestore()
        print("Connected to Firestore")
        seed_menu(db)
        seed_users(db)
        print("Seeding complete!")
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        sys.exit(1)
