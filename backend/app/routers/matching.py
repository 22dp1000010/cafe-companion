from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.firebase import (
    get_firestore,
    is_firebase_configured,
    FirebaseNotConfiguredError,
)
from datetime import datetime
import uuid
from typing import List

router = APIRouter(prefix="/api", tags=["matching"])


class InterestRequest(BaseModel):
    user_id: str
    interests: List[str]


class MatchResponse(BaseModel):
    matches: List[dict]


def normalize_interests(interests: List[str]) -> List[str]:
    """Normalize interests to lowercase and remove duplicates."""
    return list(set([interest.lower().strip() for interest in interests]))


def calculate_match_score(interests_1: List[str], interests_2: List[str]) -> float:
    """Calculate similarity score based on tag overlap."""
    if not interests_1 or not interests_2:
        return 0.0

    set_1 = set(interests_1)
    set_2 = set(interests_2)
    intersection = len(set_1 & set_2)
    union = len(set_1 | set_2)

    return intersection / union if union > 0 else 0.0


@router.post("/interests")
async def register_interests(request: InterestRequest):
    """Register user interests and find potential matches."""

    if not is_firebase_configured():
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured. Interest matching requires Firestore.",
        )

    try:
        db = get_firestore()

        # Normalize and save interests
        normalized_interests = normalize_interests(request.interests)
        user_ref = db.collection("users").document(request.user_id)
        user_ref.update({
            "interests": normalized_interests,
            "opted_in_matching": True,
            "updated_at": datetime.now(),
        })

        # Find matches with other opted-in users
        other_users = db.collection("users").where(
            "opted_in_matching", "==", True
        ).stream()

        matches_found = []
        for user_doc in other_users:
            other_user = user_doc.to_dict()
            other_user_id = user_doc.id

            if other_user_id == request.user_id:
                continue

            other_interests = normalize_interests(other_user.get("interests", []))
            score = calculate_match_score(normalized_interests, other_interests)

            if score > 0.3:  # Only match if score > 0.3
                matches_found.append({
                    "user_id": other_user_id,
                    "name": other_user.get("name", "Café Friend"),
                    "common_interests": list(set(normalized_interests) & set(other_interests)),
                    "score": round(score, 2),
                })

        # Save matches to Firestore
        for match in matches_found:
            match_id = str(uuid.uuid4())[:8]
            match_doc = {
                "id": match_id,
                "user_1_id": request.user_id,
                "user_2_id": match["user_id"],
                "common_interests": match["common_interests"],
                "score": match["score"],
                "created_at": datetime.now(),
            }
            db.collection("matches").document(match_id).set(match_doc)

        return {
            "user_id": request.user_id,
            "interests": normalized_interests,
            "matches_found": len(matches_found),
            "matches": matches_found,
        }
    except FirebaseNotConfiguredError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/matches/{user_id}")
async def get_matches(user_id: str):
    """Get all matches for a user."""

    if not is_firebase_configured():
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured. Match retrieval requires Firestore.",
        )

    try:
        db = get_firestore()

        matches_docs = db.collection("matches").where(
            "user_1_id", "==", user_id
        ).stream()

        matches = []
        for doc in matches_docs:
            match_data = doc.to_dict()
            other_user_doc = db.collection("users").document(
                match_data["user_2_id"]
            ).get()
            if other_user_doc.exists():
                other_user = other_user_doc.to_dict()
                match_data["matched_user_name"] = other_user.get("name", "Café Friend")
            matches.append(match_data)

        return {
            "user_id": user_id,
            "matches": matches,
        }
    except FirebaseNotConfiguredError as e:
        raise HTTPException(status_code=503, detail=str(e))
