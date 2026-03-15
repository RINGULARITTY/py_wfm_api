from dataclasses import dataclass
from typing import Optional
from py_wfm_api.objects.user import UserShort
from py_wfm_api.objects.item import TxItem


@dataclass
class Order:
    id: str
    type: str           # 'buy' or 'sell'
    platinum: int
    quantity: int
    perTrade: Optional[int] = None
    rank: Optional[int] = None
    charges: Optional[int] = None
    subtype: Optional[str] = None
    amberStars: Optional[int] = None
    cyanStars: Optional[int] = None
    visible: bool = True
    createdAt: str = ""
    updatedAt: str = ""
    itemId: str = ""
    group: str = ""


@dataclass
class OrderWithUser(Order):
    user: Optional[UserShort] = None

    def __post_init__(self):
        if isinstance(self.user, dict):
            self.user = UserShort(**self.user)


@dataclass
class Transaction:
    id: str
    type: str
    originId: str
    platinum: int
    quantity: int
    createdAt: str
    updatedAt: str
    item: Optional[TxItem] = None
    user: Optional[UserShort] = None

    def __post_init__(self):
        if isinstance(self.item, dict):
            self.item = TxItem(**self.item)
        if isinstance(self.user, dict):
            self.user = UserShort(**self.user)
