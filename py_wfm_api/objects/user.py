from dataclasses import dataclass, field
from typing import List, Optional
from py_wfm_api.objects.categories import Language, Platform, Status, Role, Tier, ActivityType


def _try_enum(enum_cls, value):
    """Safely convert a string to an enum, returning the value unchanged on failure."""
    if value is None or not isinstance(value, str):
        return value
    try:
        return enum_cls(value)
    except ValueError:
        return value


@dataclass
class UserShort:
    id: str
    ingameName: str
    avatar: Optional[str] = None
    reputation: int = 0
    locale: Language = Language.EN
    platform: Platform = Platform.PC
    crossplay: bool = False
    status: Status = Status.OFFLINE
    activity: str = ""
    lastSeen: str = ""

    def __post_init__(self):
        self.locale = _try_enum(Language, self.locale)
        self.platform = _try_enum(Platform, self.platform)
        self.status = _try_enum(Status, self.status)


@dataclass
class User:
    id: str
    ingameName: str
    avatar: Optional[str] = None
    background: Optional[str] = None
    about: Optional[str] = None
    reputation: int = 0
    masteryLevel: Optional[int] = None
    platform: Platform = Platform.PC
    crossplay: bool = False
    locale: Language = Language.EN
    achievementShowcase: List[str] = field(default_factory=list)
    status: Status = Status.OFFLINE
    activity: str = ""
    lastSeen: str = ""
    banned: Optional[bool] = None
    banUntil: Optional[str] = None
    warned: Optional[bool] = None
    warnMessage: Optional[str] = None
    banMessage: Optional[str] = None

    def __post_init__(self):
        self.locale = _try_enum(Language, self.locale)
        self.platform = _try_enum(Platform, self.platform)
        self.status = _try_enum(Status, self.status)


@dataclass
class UserPrivate:
    id: str
    role: Role
    ingameName: str
    avatar: Optional[str] = None
    background: Optional[str] = None
    about: Optional[str] = None
    aboutRaw: Optional[str] = None
    reputation: int = 0
    masteryRank: int = 0
    credits: int = 0
    platform: Platform = Platform.PC
    crossplay: bool = False
    locale: Language = Language.EN
    theme: str = ""
    achievementShowcase: List[str] = field(default_factory=list)
    verification: bool = False
    checkCode: str = ""
    tier: Tier = Tier.NONE
    subscription: bool = False
    warned: Optional[bool] = None
    warnMessage: Optional[str] = None
    banned: Optional[bool] = None
    banUntil: Optional[str] = None
    banMessage: Optional[str] = None
    reviewsLeft: int = 0
    unreadMessages: int = 0
    ignoreList: List[str] = field(default_factory=list)
    deleteInProgress: Optional[bool] = None
    deleteAt: Optional[str] = None
    linkedAccounts: dict = field(default_factory=dict)
    hasEmail: bool = False
    lastSeen: str = ""
    createdAt: str = ""

    def __post_init__(self):
        self.role = _try_enum(Role, self.role)
        self.platform = _try_enum(Platform, self.platform)
        self.locale = _try_enum(Language, self.locale)
        self.tier = _try_enum(Tier, self.tier)


@dataclass
class Activity:
    activity_type: ActivityType = ActivityType.UNKNOWN
    details: Optional[str] = None
    startedAt: Optional[str] = None

    def __post_init__(self):
        self.activity_type = _try_enum(ActivityType, self.activity_type)
