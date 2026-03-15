from typing import List, Optional, Tuple
from py_wfm_api.api.core import get_request_wfm, post_request_wfm, put_request_wfm, delete_request_wfm, validate_slug, validate_id
from py_wfm_api.objects.order import Order, OrderWithUser

_VALID_ORDER_TYPES = {"buy", "sell"}


# ─── Read ─────────────────────────────────────────────────────────────────────

def get_recent_orders() -> List[OrderWithUser]:
    """Get the most recent orders (max 500, last 4 hours). Cached with 1 min refresh."""
    return [OrderWithUser(**o) for o in get_request_wfm("orders/recent")]


def get_recent_orders_item(slug: str) -> List[OrderWithUser]:
    """Get all orders for an item from users online within the last 7 days."""
    return [OrderWithUser(**o) for o in get_request_wfm(f"orders/item/{validate_slug(slug)}")]


def get_top_orders_item(
    slug: str,
    rank: Optional[int] = None,
    rankLt: Optional[int] = None,
    charges: Optional[int] = None,
    chargesLt: Optional[int] = None,
    amberStars: Optional[int] = None,
    amberStarsLt: Optional[int] = None,
    cyanStars: Optional[int] = None,
    cyanStarsLt: Optional[int] = None,
    subtype: Optional[str] = None,
) -> Tuple[List[OrderWithUser], List[OrderWithUser]]:
    """Fetch the top 5 buy and top 5 sell orders for an item (online users only).

    For each pair (rank/rankLt, charges/chargesLt, etc.) only the 'Lt' (less-than)
    variant is sent when both are provided — it takes precedence.
    Returns (buy_orders, sell_orders).
    """
    params = {
        k: v for k, v in {
            "rank": rank,
            "rankLt": rankLt,
            "charges": charges,
            "chargesLt": chargesLt,
            "amberStars": amberStars,
            "amberStarsLt": amberStarsLt,
            "cyanStars": cyanStars,
            "cyanStarsLt": cyanStarsLt,
            "subtype": subtype,
        }.items() if v is not None
    }

    # Lt variants take precedence over exact filters
    for base in ("rank", "charges", "amberStars", "cyanStars"):
        if f"{base}Lt" in params:
            params.pop(base, None)

    res = get_request_wfm(f"orders/item/{validate_slug(slug)}/top", params=params)
    return (
        [OrderWithUser(**o) for o in res["buy"]],
        [OrderWithUser(**o) for o in res["sell"]],
    )


def get_user_orders(username: str) -> List[Order]:
    """Get public orders from a user by their in-game name."""
    return [Order(**o) for o in get_request_wfm(f"orders/user/{validate_slug(username, 'username')}")]


def get_user_id_orders(user_id: str) -> List[Order]:
    """Get public orders from a user by their user ID."""
    return [Order(**o) for o in get_request_wfm(f"orders/userId/{validate_id(user_id, 'user_id')}")]


def get_my_orders() -> List[Order]:
    """Get all orders of the authenticated user. Requires auth token."""
    return [Order(**o) for o in get_request_wfm("orders/my")]


def get_order(order_id: str) -> OrderWithUser:
    """Get a specific order by its ID."""
    return OrderWithUser(**get_request_wfm(f"order/{validate_id(order_id, 'order_id')}"))


# ─── Write (requires authentication) ─────────────────────────────────────────

def create_order(
    item_id: str,
    order_type: str,
    platinum: int,
    quantity: int,
    visible: bool = True,
    rank: Optional[int] = None,
    charges: Optional[int] = None,
    subtype: Optional[str] = None,
    amberStars: Optional[int] = None,
    cyanStars: Optional[int] = None,
) -> Order:
    """Create a new buy or sell order. Requires auth token.

    Args:
        item_id:    ID of the item to trade.
        order_type: 'buy' or 'sell'.
        platinum:   Price in platinum (> 0).
        quantity:   Number of items (> 0).
        visible:    Whether the order is publicly visible (default True).
    """
    if order_type not in _VALID_ORDER_TYPES:
        raise ValueError(f"order_type must be 'buy' or 'sell', got '{order_type}'")
    if platinum <= 0:
        raise ValueError(f"platinum must be > 0, got {platinum}")
    if quantity <= 0:
        raise ValueError(f"quantity must be > 0, got {quantity}")

    payload: dict = {
        "itemId": item_id,
        "type": order_type,
        "platinum": platinum,
        "quantity": quantity,
        "visible": visible,
    }
    for key, val in {
        "rank": rank,
        "charges": charges,
        "subtype": subtype,
        "amberStars": amberStars,
        "cyanStars": cyanStars,
    }.items():
        if val is not None:
            payload[key] = val

    return Order(**post_request_wfm("orders", json=payload))


def update_order(
    order_id: str,
    platinum: Optional[int] = None,
    quantity: Optional[int] = None,
    visible: Optional[bool] = None,
    rank: Optional[int] = None,
) -> Order:
    """Update an existing order. Requires auth token.

    Only the fields provided (non-None) are sent in the request.
    """
    if platinum is not None and platinum <= 0:
        raise ValueError(f"platinum must be > 0, got {platinum}")
    if quantity is not None and quantity <= 0:
        raise ValueError(f"quantity must be > 0, got {quantity}")

    payload = {
        k: v for k, v in {
            "platinum": platinum,
            "quantity": quantity,
            "visible": visible,
            "rank": rank,
        }.items() if v is not None
    }
    return Order(**put_request_wfm(f"order/{validate_id(order_id, 'order_id')}", json=payload))


def delete_order(order_id: str) -> None:
    """Delete an order. Requires auth token."""
    delete_request_wfm(f"order/{validate_id(order_id, 'order_id')}")
