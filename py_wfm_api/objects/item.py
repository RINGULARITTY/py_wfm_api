from dataclasses import dataclass, field
from typing import Dict, List, Optional
from py_wfm_api.objects.categories import Language
from py_wfm_api.objects.utils import parse_i18n


@dataclass
class ItemI18NJson:
    name: str
    description: Optional[str] = None
    wikiLink: Optional[str] = None
    icon: str = ""
    thumb: str = ""
    subIcon: Optional[str] = None


@dataclass
class ItemJson:
    id: str
    slug: str
    gameRef: str
    tags: List[str] = field(default_factory=list)
    setRoot: Optional[bool] = None
    setParts: List[str] = field(default_factory=list)
    quantityInSet: Optional[int] = None
    rarity: Optional[str] = None
    bulkTradable: Optional[bool] = None
    subtypes: List[str] = field(default_factory=list)
    maxRank: Optional[int] = None
    maxCharges: Optional[int] = None
    maxAmberStars: Optional[int] = None
    maxCyanStars: Optional[int] = None
    baseEndo: Optional[int] = None
    endoMultiplier: Optional[float] = None
    ducats: Optional[int] = None
    vosfor: Optional[int] = None
    reqMasteryRank: Optional[int] = None
    vaulted: Optional[bool] = None
    tradingTax: Optional[int] = None
    tradable: Optional[bool] = None
    i18n: Dict[Language, ItemI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(ItemI18NJson, self.i18n)


@dataclass
class TxItem:
    id: Optional[str] = None
    rank: Optional[int] = None
    charges: Optional[int] = None
    subtype: Optional[str] = None
    amberStars: Optional[int] = None
    cyanStars: Optional[int] = None
