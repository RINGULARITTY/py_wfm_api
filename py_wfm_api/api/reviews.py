from typing import List
from py_wfm_api.api.core import get_request_wfm, post_request_wfm, validate_slug
from py_wfm_api.objects.other import Review

_MAX_REVIEW_LENGTH = 1000


def get_user_reviews(username: str) -> List[Review]:
    """Get all reviews for a user."""
    return [Review(**r) for r in get_request_wfm(f"profile/{validate_slug(username, 'username')}/reviews")]


def create_review(username: str, text: str, is_positive: bool) -> Review:
    """Post a review for a user. Requires auth token.

    Args:
        username:    In-game name of the user being reviewed.
        text:        Review text (max 1000 characters).
        is_positive: True for a positive review, False for negative.
    """
    if not text or not text.strip():
        raise ValueError("Review text must not be empty.")
    if len(text) > _MAX_REVIEW_LENGTH:
        raise ValueError(f"Review text must be at most {_MAX_REVIEW_LENGTH} characters.")

    payload = {"text": text.strip(), "isPositive": is_positive}
    return Review(**post_request_wfm(f"profile/{validate_slug(username, 'username')}/reviews", json=payload))
