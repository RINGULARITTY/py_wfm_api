import py_wfm_api as wfm
from py_wfm_api.objects.categories import Language


# ─────────────────────────────────────────────────────────────────────────────
# 1. List tradable items
# ─────────────────────────────────────────────────────────────────────────────

def example_01_items():
    print("\n=== 1. Tradable items (first 5) ===")

    items = wfm.get_tradable_items()

    for item in items[:5]:
        name = item.i18n.get(Language.EN)
        print(f"  {item.slug:<40}  {name.name if name else '?'}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Item real time price
# ─────────────────────────────────────────────────────────────────────────────

def example_02_top_orders():
    print("\n=== 2. Top 5 buy / sell orders — boltor-prime-set ===")

    buys, sells = wfm.get_top_orders_item("boltor-prime-set")

    print("  Buy  :")
    for o in buys:
        user = o.user.ingameName if o.user else "?"
        status = o.user.status.value if o.user else "?"
        print(f"    {o.platinum:>4} pt  x{o.quantity}  [{status}]  {user}")

    print("  Sell :")
    for o in sells:
        user = o.user.ingameName if o.user else "?"
        status = o.user.status.value if o.user else "?"
        print(f"    {o.platinum:>4} pt  x{o.quantity}  [{status}]  {user}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Public player profile
# ─────────────────────────────────────────────────────────────────────────────

def example_03_player_profile():
    print("\n=== 3. Public profile — Brozime ===")

    user = wfm.get_profile("Brozime")
    print(f"  Name      : {user.ingameName}")
    print(f"  Reputation: {user.reputation}")
    print(f"  Platform  : {user.platform.value}")
    print(f"  Status    : {user.status.value}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Recent orders
# ─────────────────────────────────────────────────────────────────────────────

def example_04_recent_orders():
    print("\n=== 4. Last 10 orders on the global market ===")

    orders = wfm.get_recent_orders()

    for o in orders[:10]:
        user = o.user.ingameName if o.user else "?"
        print(f"  [{o.type:<4}]  {o.platinum:>4} pt  x{o.quantity}  item={o.itemId}  by={user}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Price history
# ─────────────────────────────────────────────────────────────────────────────

def example_05_statistics():
    print("\n=== 5. Price statistics — ash-prime-set (last 7 days) ===")

    stats = wfm.get_item_statistics("ash-prime-set")

    entries_90d = stats.get("statistics_closed", {}).get("90days", [])
    for entry in entries_90d[-7:]:
        print(
            f"  {entry.get('datetime', '?')[:10]}  "
            f"avg={str(entry.get('avgPrice', '?')):>6}  "
            f"med={str(entry.get('median', '?')):>6}  "
            f"vol={entry.get('volume', '?'):>4}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 6. Rivens
# ─────────────────────────────────────────────────────────────────────────────

def example_06_rivens():
    print("\n=== 6. Rivens (first 5 weapons) + positive attributes ===")

    weapons = wfm.get_tradable_riven_items()
    for w in weapons[:5]:
        print(f"  {w.slug:<35}  disposition={w.disposition}  MR={w.reqMasteryRank}")

    print("\n  Riven attributes (positive only, first 5) :")
    attrs = wfm.get_riven_attributes()
    positives = [a for a in attrs if not a.negativeOnly]
    for a in positives[:5]:
        effect = a.i18n.get(Language.EN)
        print(f"  {a.slug:<40}  {effect.effect if effect else '?'}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Lich
# ─────────────────────────────────────────────────────────────────────────────

def example_07_lich_auctions():
    print("\n=== 7. Lich weapons + active auctions ===")

    weapons = wfm.get_lich_weapons()
    print(f"  {len(weapons)} Lich weapons available.")
    for w in weapons[:3]:
        name = w.i18n.get(Language.EN)
        print(f"  {w.slug:<35}  {name.itemName if name else '?'}  MR={w.reqMasteryRank}")

    print("\n  Active Lich auctions (first 3) :")
    auctions = wfm.search_auctions("lich")
    for a in auctions[:3]:
        item = a.item
        owner = a.owner.ingameName if a.owner else "?"
        if item:
            print(
                f"  {owner:<20}  weapon={item.weaponUrlName}  "
                f"element={item.element}  dmg={item.damage}%  "
                f"ephemera={'yes' if item.havingEphemera else 'no'}  "
                f"starting={a.startingPrice} pt"
            )


# ─────────────────────────────────────────────────────────────────────────────
# 8. Manage account
# ─────────────────────────────────────────────────────────────────────────────

def example_08_authenticated():
    print("\n=== 8. Authenticated example (disabled) ===")

    # Option A — Using email + password
    # wfm.signin("ur@email.com", "password")
    # Option B — From browser token
    # F12 → Application → Cookies → jwt or Authorization
    # wfm.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

    profile = wfm.get_my_profile()
    print(f"  Logged in as: {profile.ingameName}  ({profile.credits} credits)")

    my_orders = wfm.get_my_orders()
    print(f"  Active orders: {len(my_orders)}")

    # Create a sell order
    item_info = wfm.get_item_info("boltor-prime-set")
    new_order = wfm.create_order(
        item_id=item_info.id,
        order_type="sell",
        platinum=150,
        quantity=1,
        visible=True,
    )
    print(f"  Order created: {new_order.id}")

    # Update the price
    wfm.update_order(new_order.id, platinum=140)
    print("  Price updated: 140 pt")

    # Delete the order
    wfm.delete_order(new_order.id)
    print("  Order deleted.")

    wfm.signout()
    print("  (example commented out — uncomment after filling in your credentials)")


# ─────────────────────────────────────────────────────────────────────────────
# 9. Advanced example — set vs parts arbitrage
# ─────────────────────────────────────────────────────────────────────────────

def example_09_arbitrage():
    print("\n=== 9. Arbitrage — Ash Prime: set vs sum of parts ===")

    _, parts = wfm.get_item_set_info("ash-prime-set")

    part_prices: dict[str, int] = {}
    for part in parts:
        if part.setRoot:
            continue  # skip the set entry itself
        try:
            _, sells = wfm.get_top_orders_item(part.slug)
            if sells:
                part_prices[part.slug] = sells[0].platinum
        except Exception:
            pass

    try:
        _, set_sells = wfm.get_top_orders_item("ash-prime-set")
        set_price = set_sells[0].platinum if set_sells else None
    except Exception:
        set_price = None

    total_parts = sum(part_prices.values())
    print(f"  Set price        : {set_price} pt")
    print(f"  Sum of parts     : {total_parts} pt")
    for slug, price in sorted(part_prices.items()):
        print(f"    {slug:<45}  {price:>4} pt")

    if set_price and total_parts:
        diff = total_parts - set_price
        advice = "buy the set and resell parts" if diff > 0 else "buy parts separately"
        sign = "+" if diff >= 0 else ""
        print(f"\n  Difference (parts - set): {sign}{diff} pt  → {advice}")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    example_01_items()
    example_02_top_orders()
    example_03_player_profile()
    example_04_recent_orders()
    example_05_statistics()
    example_06_rivens()
    example_07_lich_auctions()
    example_08_authenticated()
    example_09_arbitrage()
