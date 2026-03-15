from py_wfm_api.api.core import get_request_wfm, validate_slug


def get_item_statistics(slug: str) -> dict:
    """Get price statistics for an item (48-hour and 90-day history).

    Returns the raw statistics dict as provided by the API. Each entry typically
    contains fields such as: datetime, volume, minPrice, maxPrice, avgPrice,
    median, movingAvg, waTradeCount, donchTop, donchBot, orderType.

    Example structure:
        {
            "statistics_live":   {"48hours": [...], "90days": [...]},
            "statistics_closed": {"48hours": [...], "90days": [...]},
        }
    """
    return get_request_wfm(f"items/{validate_slug(slug)}/statistics")
