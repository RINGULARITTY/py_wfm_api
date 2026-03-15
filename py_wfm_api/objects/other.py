from dataclasses import dataclass, field
from typing import Dict, List, Optional   # Fixed: added List (was missing, caused NameError)
from py_wfm_api.objects.categories import Language


def _parse_i18n(cls, data: dict) -> dict:
    """Convert i18n dict: string keys → Language enum, dict values → dataclass instances."""
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
class NpcI18NJson:
    name: str
    icon: str
    thumb: str


@dataclass
class Npc:
    id: str
    slug: str
    gameRef: str
    i18n: Dict[Language, NpcI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = _parse_i18n(NpcI18NJson, self.i18n)


@dataclass
class LocationI18NJson:
    nodeName: str
    systemName: Optional[str] = None
    icon: str = ""
    thumb: str = ""


@dataclass
class Location:
    id: str
    slug: str
    gameRef: str
    faction: Optional[str] = None
    minLevel: Optional[int] = None
    maxLevel: Optional[int] = None
    i18n: Dict[Language, LocationI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = _parse_i18n(LocationI18NJson, self.i18n)


@dataclass
class MissionI18NJson:
    name: str
    icon: Optional[str] = None
    thumb: Optional[str] = None


@dataclass
class Mission:
    id: str
    slug: str
    gameRef: str
    i18n: Dict[Language, MissionI18NJson] = field(default_factory=dict)

    def __post_init__(self):
        self.i18n = _parse_i18n(MissionI18NJson, self.i18n)


@dataclass
class AchievementI18N:
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    thumb: Optional[str] = None


@dataclass
class AchievementState:
    featured: Optional[bool] = None
    hidden: Optional[bool] = None
    progress: Optional[int] = None
    completedAt: Optional[str] = None


@dataclass
class Achievement:
    id: str
    slug: str
    type: str
    secret: Optional[bool] = None
    reputationBonus: Optional[int] = None
    goal: Optional[int] = None
    i18n: Dict[Language, AchievementI18N] = field(default_factory=dict)
    state: Optional[AchievementState] = None

    def __post_init__(self):
        self.i18n = _parse_i18n(AchievementI18N, self.i18n)
        if isinstance(self.state, dict):
            self.state = AchievementState(**self.state)


@dataclass
class DashboardShowcaseI18NJson:
    title: str
    description: Optional[str] = None


@dataclass
class DashboardShowcaseItemJson:
    item: str
    background: str
    bigCard: bool


@dataclass
class DashboardShowcase:
    i18n: Dict[Language, DashboardShowcaseI18NJson] = field(default_factory=dict)
    items: List[DashboardShowcaseItemJson] = field(default_factory=list)

    def __post_init__(self):
        self.i18n = _parse_i18n(DashboardShowcaseI18NJson, self.i18n)
        if self.items:
            self.items = [
                DashboardShowcaseItemJson(**x) if isinstance(x, dict) else x
                for x in self.items
            ]


@dataclass
class Review:
    id: str
    text: str
    isPositive: bool
    createdAt: str
    updatedAt: str
    user: Optional[object] = None   # UserShort — lazy import to avoid circular dependency

    def __post_init__(self):
        if isinstance(self.user, dict):
            from py_wfm_api.objects.user import UserShort
            self.user = UserShort(**self.user)
