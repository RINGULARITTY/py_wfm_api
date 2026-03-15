from dataclasses import dataclass, field
from typing import Dict, List, Optional
from py_wfm_api.objects.categories import Language


def _parse_i18n(cls, data: dict) -> dict:
    if not data:
        return {}
    result = {}
    for k, v in data.items():
        try:
            lang = Language(k) if isinstance(k, str) else k
        except ValueError:
            lang = k
        result[lang] = cls(**v) if isinstance(v, dict) else v
    return result


@dataclass
class RivenI18NJson:
    itemName: Optional[str] = None
    wikiLink: Optional[str] = None
    icon: str = ""
    thumb: str = ""


@dataclass
class Riven:
    id: str
    slug: str
    gameRef: str
    group: Optional[str] = None
    rivenType: Optional[str] = None
    disposition: float = 0.0
    reqMasteryRank: int = 0
    i18n: Dict[Language, RivenI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = _parse_i18n(RivenI18NJson, self.i18n)


@dataclass
class RivenAttributeI18N:
    effect: str
    icon: str
    thumb: str


@dataclass
class RivenAttribute:
    id: str
    slug: str
    gameRef: str
    group: Optional[str] = None
    prefix: str = ""
    suffix: str = ""
    exclusiveTo: List[str] = field(default_factory=list)
    positiveIsNegative: Optional[bool] = None
    unit: Optional[str] = None
    positiveOnly: Optional[bool] = None
    negativeOnly: Optional[bool] = None
    i18n: Dict[Language, RivenAttributeI18N] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = _parse_i18n(RivenAttributeI18N, self.i18n)
