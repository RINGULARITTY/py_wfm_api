"""
wfm — Warframe Market Python client
=====================================

Quick start (read-only)::

    import py_wfm_api as wfm

    items = wfm.get_tradable_items()
    buy, sell = wfm.get_top_orders_item("boltor-prime-set")

Quick start (authenticated)::

    import py_wfm_api as wfm

    wfm.signin("email@example.com", "password")
    # — or manually set a token extracted from the browser —
    wfm.set_token("your_jwt_token_here")

    my_orders = wfm.get_my_orders()
    wfm.create_order(item_id="...", order_type="sell", platinum=50, quantity=1)
    wfm.signout()
"""
from py_wfm_api.api import (
    # Auth
    set_auth_token, clear_auth_token,
    signin, signout, set_token,
    # Items
    get_tradable_items, get_item_info, get_item_set_info,
    # Orders
    get_recent_orders, get_recent_orders_item, get_top_orders_item,
    get_user_orders, get_user_id_orders, get_my_orders, get_order,
    create_order, update_order, delete_order,
    # Users
    get_profile, search_users, get_my_profile, update_my_profile,
    # Auctions
    search_auctions, get_auction, get_auction_bids,
    get_popular_auctions, get_user_auctions, get_my_auctions,
    create_auction, update_auction, close_auction, place_bid,
    # Rivens
    get_tradable_riven_items, get_riven_info, get_riven_attributes,
    # Lich weapons
    get_lich_weapons, get_lich_weapon_info, get_lich_ephemeras, get_lich_quirks,
    # Sister weapons
    get_sister_weapons, get_sister_weapon_info, get_sister_ephemeras, get_sister_quirks,
    # Game data
    get_locations, get_ncps, get_missions,
    # Reviews
    get_user_reviews, create_review,
    # Statistics
    get_item_statistics,
)
from wfm import api, objects

__all__ = [
    "api", "objects",
    # Auth
    "set_auth_token", "clear_auth_token",
    "signin", "signout", "set_token",
    # Items
    "get_tradable_items", "get_item_info", "get_item_set_info",
    # Orders
    "get_recent_orders", "get_recent_orders_item", "get_top_orders_item",
    "get_user_orders", "get_user_id_orders", "get_my_orders", "get_order",
    "create_order", "update_order", "delete_order",
    # Users
    "get_profile", "search_users", "get_my_profile", "update_my_profile",
    # Auctions
    "search_auctions", "get_auction", "get_auction_bids",
    "get_popular_auctions", "get_user_auctions", "get_my_auctions",
    "create_auction", "update_auction", "close_auction", "place_bid",
    # Rivens
    "get_tradable_riven_items", "get_riven_info", "get_riven_attributes",
    # Lich weapons
    "get_lich_weapons", "get_lich_weapon_info", "get_lich_ephemeras", "get_lich_quirks",
    # Sister weapons
    "get_sister_weapons", "get_sister_weapon_info", "get_sister_ephemeras", "get_sister_quirks",
    # Game data
    "get_locations", "get_ncps", "get_missions",
    # Reviews
    "get_user_reviews", "create_review",
    # Statistics
    "get_item_statistics",
]
