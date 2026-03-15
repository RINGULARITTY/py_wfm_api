from dataclasses import dataclass
from typing import Optional
from py_wfm_api.objects.user import UserShort
from py_wfm_api.objects.item import TxItem
from py_wfm_api.objects.utils import dc_from_dict


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
            self.user = dc_from_dict(UserShort, self.user)


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
            self.item = dc_from_dict(TxItem, self.item)
        if isinstance(self.user, dict):
            self.user = dc_from_dict(UserShort, self.user)
