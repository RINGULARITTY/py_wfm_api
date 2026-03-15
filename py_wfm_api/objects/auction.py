from dataclasses import dataclass, field
from typing import List, Optional
from py_wfm_api.objects.user import UserShort


@dataclass
class AuctionBid:
    id: str
    value: int          # Bid amount in platinum
    createdAt: str
    updatedAt: str
    user: Optional[UserShort] = None

    def __post_init__(self):
        if isinstance(self.user, dict):
            self.user = UserShort(**self.user)


@dataclass
class AuctionEntryLich:
    """Item payload for a Lich auction."""
    weaponUrlName: str  # Slug of the lich weapon
    element: str        # Element type (e.g. 'heat', 'cold', 'toxin', ...)
    damage: float       # Damage bonus percentage (0–60)
    havingEphemera: bool
    type: str = "lich"
    quirk: Optional[str] = None  # Slug of the lich quirk


@dataclass
class AuctionEntrySister:
    """Item payload for a Sister of Parvos auction."""
    weaponUrlName: str
    element: str
    damage: float
    havingEphemera: bool
    type: str = "sister"
    quirk: Optional[str] = None


@dataclass
class Auction:
    id: str
    type: str           # 'lich' or 'sister'
    note: str
    isClosed: bool
    isPrivate: bool
    createdAt: str
    updatedAt: str
    buyoutPrice: Optional[int] = None
    startingPrice: Optional[int] = None
    topBid: Optional[int] = None
    owner: Optional[UserShort] = None
    winner: Optional[UserShort] = None
    item: Optional[object] = None   # AuctionEntryLich | AuctionEntrySister
    bids: List[AuctionBid] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.owner, dict):
            self.owner = UserShort(**self.owner)
        if isinstance(self.winner, dict):
            self.winner = UserShort(**self.winner)
        if self.bids:
            self.bids = [AuctionBid(**b) if isinstance(b, dict) else b for b in self.bids]
        if isinstance(self.item, dict):
            entry_type = self.item.get("type")
            if entry_type == "lich":
                self.item = AuctionEntryLich(**self.item)
            elif entry_type == "sister":
                self.item = AuctionEntrySister(**self.item)
