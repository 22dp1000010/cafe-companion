import pytest
from app.routers.matching import normalize_interests, calculate_match_score


def test_normalize_interests():
    """Test interest normalization (lowercase, dedupe)."""
    interests = ["Hiking", "HIKING", "Photography", "hiking"]
    normalized = normalize_interests(interests)
    assert len(normalized) == 2
    assert "hiking" in normalized
    assert "photography" in normalized


def test_normalize_empty():
    """Test normalization with empty list."""
    interests = []
    normalized = normalize_interests(interests)
    assert normalized == []


def test_normalize_strips_whitespace():
    """Test that normalization strips whitespace."""
    interests = ["  hiking  ", "photography"]
    normalized = normalize_interests(interests)
    assert "hiking" in normalized
    assert "photography" in normalized


def test_match_score_perfect_match():
    """Test perfect overlap between interest sets."""
    interests_1 = ["hiking", "photography", "coding"]
    interests_2 = ["hiking", "photography", "coding"]
    score = calculate_match_score(interests_1, interests_2)
    assert score == 1.0  # 100% match


def test_match_score_partial_overlap():
    """Test partial overlap."""
    interests_1 = ["hiking", "photography", "coding"]
    interests_2 = ["hiking", "music", "yoga"]
    # Intersection: hiking (1), Union: hiking, photography, coding, music, yoga (5)
    # Score: 1/5 = 0.2
    score = calculate_match_score(interests_1, interests_2)
    assert abs(score - 0.2) < 0.01


def test_match_score_no_overlap():
    """Test no common interests."""
    interests_1 = ["hiking", "photography"]
    interests_2 = ["music", "coding"]
    score = calculate_match_score(interests_1, interests_2)
    assert score == 0.0


def test_match_score_empty_interests():
    """Test with empty interest lists."""
    score = calculate_match_score([], ["hiking"])
    assert score == 0.0

    score = calculate_match_score(["hiking"], [])
    assert score == 0.0

    score = calculate_match_score([], [])
    assert score == 0.0


def test_match_score_single_overlap():
    """Test with single common interest."""
    interests_1 = ["hiking"]
    interests_2 = ["hiking"]
    score = calculate_match_score(interests_1, interests_2)
    assert score == 1.0


def test_match_score_one_subset():
    """Test when one is a subset of the other."""
    interests_1 = ["hiking", "photography", "coding"]
    interests_2 = ["hiking", "photography"]
    # Intersection: hiking, photography (2), Union: hiking, photography, coding (3)
    # Score: 2/3
    score = calculate_match_score(interests_1, interests_2)
    assert abs(score - (2/3)) < 0.01
