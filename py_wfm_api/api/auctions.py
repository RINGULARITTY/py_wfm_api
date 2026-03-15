from typing import List, Optional
from py_wfm_api.api.core import get_request_wfm, post_request_wfm, put_request_wfm, delete_request_wfm, validate_slug, validate_id
from py_wfm_api.objects.auction import Auction, AuctionBid

_VALID_AUCTION_TYPES = {"lich", "sister"}


# ─── Read ─────────────────────────────────────────────────────────────────────

def search_auctions(
    auction_type: str,
    weapon_url_name: Optional[str] = None,
    element: Optional[str] = None,
    damage_min: Optional[float] = None,
    damage_max: Optional[float] = None,
    having_ephemera: Optional[bool] = None,
    quirk: Optional[str] = None,
    sort_by: Optional[str] = None,
    buy_it_now: Optional[bool] = None,
) -> List[Auction]:
    """Search active auctions.

    Args:
        auction_type:    'lich' or 'sister'.
        weapon_url_name: Filter by weapon slug.
        element:         Filter by element (e.g. 'heat', 'cold', 'toxin').
        damage_min:      Minimum damage bonus percentage.
        damage_max:      Maximum damage bonus percentage.
        having_ephemera: Filter by ephemera presence.
        quirk:           Filter by quirk slug.
        sort_by:         Sort field (e.g. 'price_asc', 'price_desc').
        buy_it_now:      If True, only return auctions with a buyout price.
    """
    if auction_type not in _VALID_AUCTION_TYPES:
        raise ValueError(f"auction_type must be 'lich' or 'sister', got '{auction_type}'")

    params = {
        k: v for k, v in {
            "type": auction_type,
            "weapon_url_name": weapon_url_name,
            "element": element,
            "damage_min": damage_min,
            "damage_max": damage_max,
            "having_ephemera": having_ephemera,
            "quirk": quirk,
            "sort_by": sort_by,
            "buy_it_now": buy_it_now,
        }.items() if v is not None
    }
    return [Auction(**a) for a in get_request_wfm("auctions/search", params=params)]


def get_auction(auction_id: str) -> Auction:
    """Get a specific auction by its ID."""
    return Auction(**get_request_wfm(f"auction/{validate_id(auction_id, 'auction_id')}"))


def get_auction_bids(auction_id: str) -> List[AuctionBid]:
    """Get all bids for a specific auction."""
    return [AuctionBid(**b) for b in get_request_wfm(f"auction/{validate_id(auction_id, 'auction_id')}/bids")]


def get_popular_auctions() -> List[Auction]:
    """Get currently popular auctions."""
    return [Auction(**a) for a in get_request_wfm("auctions/popular")]


def get_user_auctions(username: str) -> List[Auction]:
    """Get all auctions posted by a specific user."""
    return [Auction(**a) for a in get_request_wfm(f"profile/{validate_slug(username, 'username')}/auctions")]


def get_my_auctions() -> List[Auction]:
    """Get all auctions of the authenticated user. Requires auth token."""
    return [Auction(**a) for a in get_request_wfm("auctions/my")]


# ─── Write (requires authentication) ─────────────────────────────────────────

def create_auction(
    auction_type: str,
    weapon_url_name: str,
    element: str,
    damage: float,
    having_ephemera: bool,
    starting_price: int,
    buyout_price: Optional[int] = None,
    note: str = "",
    quirk: Optional[str] = None,
    is_private: bool = False,
) -> Auction:
    """Create a new Lich or Sister auction. Requires auth token.

    Args:
        auction_type:    'lich' or 'sister'.
        weapon_url_name: Slug of the weapon being auctioned.
        element:         Element type of the weapon.
        damage:          Damage bonus percentage (0–60).
        having_ephemera: Whether the Lich/Sister has an ephemera.
        starting_price:  Starting bid in platinum (> 0).
        buyout_price:    Buyout price in platinum (optional, must be >= starting_price).
        note:            Additional note for the listing.
        quirk:           Slug of the Lich/Sister quirk (optional).
        is_private:      Whether the auction is private.
    """
    if auction_type not in _VALID_AUCTION_TYPES:
        raise ValueError(f"auction_type must be 'lich' or 'sister', got '{auction_type}'")
    if not (0.0 <= damage <= 60.0):
        raise ValueError(f"damage must be between 0 and 60, got {damage}")
    if starting_price <= 0:
        raise ValueError(f"starting_price must be > 0, got {starting_price}")
    if buyout_price is not None and buyout_price < starting_price:
        raise ValueError(f"buyout_price ({buyout_price}) must be >= starting_price ({starting_price})")

    item: dict = {
        "type": auction_type,
        "weaponUrlName": weapon_url_name,
        "element": element,
        "damage": damage,
        "havingEphemera": having_ephemera,
    }
    if quirk is not None:
        item["quirk"] = quirk

    payload: dict = {
        "item": item,
        "startingPrice": starting_price,
        "note": note,
        "isPrivate": is_private,
    }
    if buyout_price is not None:
        payload["buyoutPrice"] = buyout_price

    return Auction(**post_request_wfm("auctions", json=payload))


def update_auction(
    auction_id: str,
    note: Optional[str] = None,
    starting_price: Optional[int] = None,
    buyout_price: Optional[int] = None,
    is_private: Optional[bool] = None,
) -> Auction:
    """Update an existing auction. Requires auth token."""
    if starting_price is not None and starting_price <= 0:
        raise ValueError(f"starting_price must be > 0, got {starting_price}")
    if buyout_price is not None and buyout_price <= 0:
        raise ValueError(f"buyout_price must be > 0, got {buyout_price}")

    payload = {
        k: v for k, v in {
            "note": note,
            "startingPrice": starting_price,
            "buyoutPrice": buyout_price,
            "isPrivate": is_private,
        }.items() if v is not None
    }
    return Auction(**put_request_wfm(f"auction/{validate_id(auction_id, 'auction_id')}", json=payload))


def close_auction(auction_id: str) -> None:
    """Close (delete) an auction. Requires auth token."""
    delete_request_wfm(f"auction/{validate_id(auction_id, 'auction_id')}")


def place_bid(auction_id: str, platinum: int) -> AuctionBid:
    """Place a bid on an auction. Requires auth token."""
    if platinum <= 0:
        raise ValueError(f"platinum must be > 0, got {platinum}")
    return AuctionBid(**post_request_wfm(
        f"auction/{validate_id(auction_id, 'auction_id')}/bid",
        json={"platinum": platinum},
    ))
