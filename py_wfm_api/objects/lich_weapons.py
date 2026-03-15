from dataclasses import dataclass, field
from typing import Dict, Optional
from py_wfm_api.objects.categories import Language
from py_wfm_api.objects.utils import parse_i18n


# ─── Lich ────────────────────────────────────────────────────────────────────

@dataclass
class LichWeaponI18NJson:
    name: str
    wikiLink: Optional[str] = None
    icon: str = ""
    thumb: str = ""


@dataclass
class LichWeapon:
    id: str
    slug: str
    gameRef: str
    reqMasteryRank: int
    i18n: Dict[Language, LichWeaponI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(LichWeaponI18NJson, self.i18n)


@dataclass
class LichEphemeraI18NJson:
    name: str
    icon: str
    thumb: str


@dataclass
class LichEphemera:
    id: str
    slug: str
    gameRef: str
    animation: str
    element: str
    i18n: Dict[Language, LichEphemeraI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(LichEphemeraI18NJson, self.i18n)


@dataclass
class LichQuirkI18NJson:
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    thumb: Optional[str] = None


@dataclass
class LichQuirk:
    id: str
    slug: str
    group: Optional[str] = None
    i18n: Dict[Language, LichQuirkI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(LichQuirkI18NJson, self.i18n)


# ─── Sister ──────────────────────────────────────────────────────────────────

@dataclass
class SisterWeaponI18NJson:
    name: str
    wikiLink: Optional[str] = None
    icon: str = ""
    thumb: str = ""


@dataclass
class SisterWeapon:
    id: str
    slug: str
    gameRef: str
    reqMasteryRank: int
    i18n: Dict[Language, SisterWeaponI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(SisterWeaponI18NJson, self.i18n)


@dataclass
class SisterEphemeraI18NJson:
    name: str
    icon: str
    thumb: str


@dataclass
class SisterEphemera:
    id: str
    slug: str
    gameRef: str
    animation: str
    element: str
    i18n: Dict[Language, SisterEphemeraI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(SisterEphemeraI18NJson, self.i18n)


@dataclass
class SisterQuirkI18NJson:
    name: str
    description: Optional[str] = None
    icon: str = ""
    thumb: str = ""


@dataclass
class SisterQuirk:
    id: str
    slug: str
    group: Optional[str] = None
    i18n: Dict[Language, SisterQuirkI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = parse_i18n(SisterQuirkI18NJson, self.i18n)
