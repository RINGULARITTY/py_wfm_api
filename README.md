<div align="center">

# py_wfm_api

**A typed Python client for the Warframe Market API v2**

[![PyPI](https://img.shields.io/pypi/v/py_wfm_api?color=blue&label=PyPI)](https://pypi.org/project/py_wfm_api/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![WFM API](https://img.shields.io/badge/WFM_API-v2-orange)](https://warframe.market)

</div>

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

> Requires **Python ≥ 3.10**

---

## Quick start

<details open>
<summary><strong>Read-only — no account needed</strong></summary>

```python
import py_wfm_api as wfm
from py_wfm_api.objects.categories import Language

# All tradable items
items = wfm.get_tradable_items()
for item in items[:5]:
    print(item.slug, item.i18n[Language.EN].name)

# Top 5 buy / sell orders
buys, sells = wfm.get_top_orders_item("boltor_prime_set")

# Recent global orders (last 4 h)
orders = wfm.get_recent_orders()

# Rivens
rivens = wfm.get_tradable_riven_items()
attrs  = wfm.get_riven_attributes()

# Lich / Sister weapons, ephemeras, quirks
weapons   = wfm.get_lich_weapons()
ephemeras = wfm.get_lich_ephemeras()
auctions  = wfm.search_auctions("lich", element="heat", damage_min=50)
```

</details>

<details>
<summary><strong>Authenticated — account required</strong></summary>

```python
import py_wfm_api as wfm

# Option A — email + password
wfm.signin("your@email.com", "your_password")

# Option B — JWT token from the browser
# F12 → Application → Cookies → jwt  or  Authorization header
wfm.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

# Profile & orders
profile   = wfm.get_my_profile()
my_orders = wfm.get_my_orders()

# Create a sell order
item  = wfm.get_item_info("boltor_prime_set")
order = wfm.create_order(
    item_id    = item.id,
    order_type = "sell",
    platinum   = 150,
    quantity   = 1,
)

# Update price, then delete
wfm.update_order(order.id, platinum=140)
wfm.delete_order(order.id)

wfm.signout()
```

</details>

> **Note on slugs** — the WFM v2 API uses **underscores**: `boltor_prime_set`, not `boltor-prime-set`.

---

## API reference

All functions are importable directly from `py_wfm_api`.

### Authentication

| Function | Description |
|:---|:---|
| `signin(email, password)` | Authenticate and store the JWT token |
| `set_token(token)` | Set a token manually (extracted from browser) |
| `signout()` | Sign out and clear the stored token |
| `set_auth_token(token)` | Low-level: set the raw Bearer token |
| `clear_auth_token()` | Low-level: remove the stored token |

### Items

| Function | Description |
|:---|:---|
| `get_tradable_items()` | All tradable items |
| `get_item_info(slug)` | Full details for one item |
| `get_item_set_info(slug)` | Set info → `(set_id, [ItemJson])` |

### Orders

| Function | Auth | Description |
|:---|:---:|:---|
| `get_recent_orders()` | | Last ~500 global orders (≤ 4 h) |
| `get_recent_orders_item(slug)` | | All orders for an item |
| `get_top_orders_item(slug, **filters)` | | Top 5 buy + sell → `(buys, sells)` |
| `get_user_orders(username)` | | Public orders for a user |
| `get_order(order_id)` | | Single order by ID |
| `get_my_orders()` | ✓ | Your own orders |
| `create_order(item_id, order_type, platinum, quantity, ...)` | ✓ | Create a buy or sell order |
| `update_order(order_id, ...)` | ✓ | Update price / quantity / visibility |
| `delete_order(order_id)` | ✓ | Delete an order |

`get_top_orders_item` optional filters: `rank`, `rankLt`, `charges`, `chargesLt`, `amberStars`, `cyanStars`, `subtype`.

### Users

| Function | Auth | Description |
|:---|:---:|:---|
| `get_my_profile()` | ✓ | Your private profile |
| `update_my_profile(about, status)` | ✓ | Update about / status |

### Auctions — Lich & Sister

| Function | Auth | Description |
|:---|:---:|:---|
| `search_auctions(type, **filters)` | | Search active auctions (`"lich"` or `"sister"`) |
| `get_auction(auction_id)` | | Single auction by ID |
| `get_auction_bids(auction_id)` | | All bids for an auction |
| `get_popular_auctions()` | | Currently popular auctions |
| `get_my_auctions()` | ✓ | Your own auctions |
| `create_auction(type, weapon, element, damage, ...)` | ✓ | List a new auction |
| `update_auction(auction_id, ...)` | ✓ | Update note / prices |
| `close_auction(auction_id)` | ✓ | Close an auction |
| `place_bid(auction_id, platinum)` | ✓ | Place a bid |

`search_auctions` optional filters: `weapon_url_name`, `element`, `damage_min`, `damage_max`, `having_ephemera`, `quirk`, `sort_by`, `buy_it_now`.

### Rivens

| Function | Description |
|:---|:---|
| `get_tradable_riven_items()` | All tradable riven weapons |
| `get_riven_info(slug)` | Details for one riven weapon |
| `get_riven_attributes()` | All possible riven attributes |

### Lich weapons

| Function | Description |
|:---|:---|
| `get_lich_weapons()` | All Lich weapons |
| `get_lich_weapon_info(slug)` | Details for one Lich weapon |
| `get_lich_ephemeras()` | All Lich ephemeras |
| `get_lich_quirks()` | All Lich quirks |

### Sister weapons

| Function | Description |
|:---|:---|
| `get_sister_weapons()` | All Sister weapons |
| `get_sister_weapon_info(slug)` | Details for one Sister weapon |
| `get_sister_ephemeras()` | All Sister ephemeras |
| `get_sister_quirks()` | All Sister quirks |

### Game data

| Function | Description |
|:---|:---|
| `get_locations()` | All in-game locations |
| `get_ncps()` | All NPCs |
| `get_missions()` | All missions |

### Reviews

| Function | Auth | Description |
|:---|:---:|:---|
| `get_user_reviews(username)` | | Reviews for a user |
| `create_review(username, text, is_positive)` | ✓ | Post a review |

---

## Data models

Every API response is deserialized into a **typed Python dataclass** — no raw dicts.

```
py_wfm_api.objects
│
├── categories    Language · Platform · Status · Role · Tier · ActivityType
├── item          ItemJson · ItemI18NJson · TxItem
├── order         Order · OrderWithUser · Transaction
├── user          UserShort · User · UserPrivate · Activity
├── auction       Auction · AuctionBid · AuctionEntryLich · AuctionEntrySister
├── riven         Riven · RivenAttribute · RivenAttributeI18N
├── lich_weapons  LichWeapon · LichEphemera · LichQuirk  (and Sister variants)
└── other         Npc · Location · Mission · Achievement · Review
```

Models are **forward-compatible**: unknown fields returned by the API are silently discarded, so the library keeps working when Warframe Market adds new fields without requiring an update.

---

## Security

| | |
|:---|:---|
| **Input validation** | Slugs and IDs are checked against a strict regex before being embedded in URLs. Path traversal and injection are rejected at the call site. |
| **Token storage** | The JWT token lives in memory only — it is never written to disk or logged. |
| **Error safety** | API error bodies are truncated in exceptions to avoid leaking sensitive payload data. |

---

## Tests

```bash
pip install pytest

pytest                  # unit tests only  (no network, fast)
pytest -m ""            # full suite       (requires internet)
pytest -m integration   # integration only (requires internet)
```

| Marker | Description |
|:---|:---|
| *(default)* | Input validation + model deserialisation — no network calls |
| `integration` | Live API calls — read-only, no account required |
| `auth` | Authenticated endpoints — requires a valid token, skipped by default |

---

## Known limitations

`get_item_statistics()` and `get_profile()` are not yet available in WFM API v2.
Their tests are marked `xfail` and will pass automatically once these endpoints are deployed by Warframe Market.

---

## License

Released under the [MIT License](LICENSE).
