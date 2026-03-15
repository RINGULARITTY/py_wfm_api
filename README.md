# py_wfm_api

A typed Python client for the [Warframe Market](https://warframe.market) API v2.

```python
import py_wfm_api as wfm

buys, sells = wfm.get_top_orders_item("boltor_prime_set")
print(f"Best sell: {sells[0].platinum} pt  by {sells[0].user.ingameName}")
```

---

## Installation

```bash
pip install py_wfm_api
```

> **Requires Python ≥ 3.10**

---

## Quick start

### Read-only (no account needed)

```python
import py_wfm_api as wfm
from py_wfm_api.objects.categories import Language

# List all tradable items
items = wfm.get_tradable_items()
for item in items[:5]:
    print(item.slug, item.i18n[Language.EN].name)

# Top buy/sell orders for an item
buys, sells = wfm.get_top_orders_item("boltor_prime_set")

# Recent global orders
orders = wfm.get_recent_orders()

# Riven weapons & attributes
rivens   = wfm.get_tradable_riven_items()
attrs    = wfm.get_riven_attributes()

# Lich / Sister weapons, ephemeras, quirks
weapons  = wfm.get_lich_weapons()
ephemeras = wfm.get_lich_ephemeras()
```

### Authenticated (account required)

```python
import py_wfm_api as wfm

# Option A — email + password
wfm.signin("your@email.com", "your_password")

# Option B — JWT token extracted from browser
# F12 → Application → Cookies → jwt / Authorization header
wfm.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

# Read your profile and orders
profile   = wfm.get_my_profile()
my_orders = wfm.get_my_orders()

# Create a sell order
item = wfm.get_item_info("boltor_prime_set")
order = wfm.create_order(
    item_id=item.id,
    order_type="sell",
    platinum=150,
    quantity=1,
)

# Update and delete
wfm.update_order(order.id, platinum=140)
wfm.delete_order(order.id)

wfm.signout()
```

---

## API reference

> All functions are importable directly from `py_wfm_api`.
> **Slugs use underscores** — `boltor_prime_set`, not `boltor-prime-set`.

### Authentication

| Function | Description |
|---|---|
| `signin(email, password)` | Authenticate and store the JWT token |
| `set_token(token)` | Set a token manually (from browser) |
| `signout()` | Sign out and clear the token |
| `set_auth_token(token)` | Low-level: set the raw Bearer token |
| `clear_auth_token()` | Low-level: remove the stored token |

### Items

| Function | Description |
|---|---|
| `get_tradable_items()` | List all tradable items |
| `get_item_info(slug)` | Full details for one item |
| `get_item_set_info(slug)` | Set info: returns `(set_id, [ItemJson])` |

### Orders

| Function | Auth | Description |
|---|---|---|
| `get_recent_orders()` | — | Last ~500 global orders (≤ 4 h) |
| `get_recent_orders_item(slug)` | — | All orders for an item |
| `get_top_orders_item(slug, **filters)` | — | Top 5 buy + sell orders; returns `(buys, sells)` |
| `get_user_orders(username)` | — | Public orders for a user |
| `get_order(order_id)` | — | Single order by ID |
| `get_my_orders()` | ✓ | Your own orders |
| `create_order(item_id, order_type, platinum, quantity, ...)` | ✓ | Create a buy or sell order |
| `update_order(order_id, ...)` | ✓ | Update price / quantity / visibility |
| `delete_order(order_id)` | ✓ | Delete an order |

`get_top_orders_item` accepts optional filters: `rank`, `rankLt`, `charges`, `chargesLt`, `amberStars`, `cyanStars`, `subtype`.

### Users

| Function | Auth | Description |
|---|---|---|
| `get_my_profile()` | ✓ | Your private profile |
| `update_my_profile(about, status)` | ✓ | Update about / status |

### Auctions (Lich & Sister)

| Function | Auth | Description |
|---|---|---|
| `search_auctions(type, **filters)` | — | Search active auctions (`"lich"` or `"sister"`) |
| `get_auction(auction_id)` | — | Single auction by ID |
| `get_auction_bids(auction_id)` | — | All bids for an auction |
| `get_popular_auctions()` | — | Currently popular auctions |
| `get_my_auctions()` | ✓ | Your own auctions |
| `create_auction(type, weapon, element, damage, ...)` | ✓ | List a new auction |
| `update_auction(auction_id, ...)` | ✓ | Update note / prices |
| `close_auction(auction_id)` | ✓ | Close an auction |
| `place_bid(auction_id, platinum)` | ✓ | Place a bid |

### Rivens

| Function | Description |
|---|---|
| `get_tradable_riven_items()` | All tradable riven weapons |
| `get_riven_info(slug)` | Details for one riven weapon |
| `get_riven_attributes()` | All possible riven attributes |

### Lich weapons

| Function | Description |
|---|---|
| `get_lich_weapons()` | All Lich weapons |
| `get_lich_weapon_info(slug)` | Details for one Lich weapon |
| `get_lich_ephemeras()` | All Lich ephemeras |
| `get_lich_quirks()` | All Lich quirks |

### Sister weapons

| Function | Description |
|---|---|
| `get_sister_weapons()` | All Sister weapons |
| `get_sister_weapon_info(slug)` | Details for one Sister weapon |
| `get_sister_ephemeras()` | All Sister ephemeras |
| `get_sister_quirks()` | All Sister quirks |

### Game data

| Function | Description |
|---|---|
| `get_locations()` | All in-game locations |
| `get_ncps()` | All NPCs |
| `get_missions()` | All missions |

### Reviews

| Function | Auth | Description |
|---|---|---|
| `get_user_reviews(username)` | — | Reviews for a user |
| `create_review(username, text, is_positive)` | ✓ | Post a review |

---

## Data models

All API responses are deserialized into typed Python dataclasses.

```
py_wfm_api.objects
├── categories     Language, Platform, Status, Role, Tier, ActivityType
├── item           ItemJson, ItemI18NJson, TxItem
├── order          Order, OrderWithUser, Transaction
├── user           UserShort, User, UserPrivate, Activity
├── auction        Auction, AuctionBid, AuctionEntryLich, AuctionEntrySister
├── riven          Riven, RivenAttribute, RivenAttributeI18N
├── lich_weapons   LichWeapon, LichEphemera, LichQuirk  (+ Sister variants)
└── other          Npc, Location, Mission, Achievement, Review, DashboardShowcase
```

Models are forward-compatible: **unknown fields returned by the API are silently ignored**, so library updates are not required when Warframe Market adds new fields.

---

## Security

- Input slugs and IDs are validated with strict regex before being embedded in URLs — path traversal and injection are rejected at the call site.
- The JWT token is stored **in memory only** and is never written to disk.
- API error bodies are truncated in exceptions to avoid leaking sensitive data.

---

## Running tests

```bash
pip install pytest

# Unit tests only (no network, fast)
pytest

# Full suite including live API calls
pytest -m ""

# Integration tests only
pytest -m integration
```

The test suite is split into:
- **Unit tests** — validate input sanitisation and model deserialisation without any network calls.
- **Integration tests** — hit the real WFM API (read-only, no account needed).
- **Auth tests** — require a valid token; skipped by default.

---

## Known limitations

- `get_item_statistics()` and `get_profile()` are currently unavailable in WFM API v2. The corresponding tests are marked `xfail` and will pass automatically once Warframe Market implements these endpoints.

---

## License

MIT
