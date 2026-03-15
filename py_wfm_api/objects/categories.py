from enum import Enum


class Status(Enum):
    INVISIBLE = "invisible"
    OFFLINE = "offline"
    ONLINE = "online"
    IN_GAME = "ingame"


class ActivityType(Enum):
    UNKNOWN = "unknown"
    IDLE = "idle"
    ON_MISSION = "on_mission"
    IN_DOJO = "in_dojo"
    IN_ORBITER = "in_orbiter"
    IN_RELAY = "in_relay"


class Role(Enum):
    USER = "user"           # Fixed: was "user," (trailing comma made it a tuple)
    MODERATOR = "moderator"
    ADMIN = "admin"


class Tier(Enum):
    NONE = "none"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    DIAMOND = "diamond"


class Language(Enum):
    KO = "ko"           # Fixed: was "ko," (trailing comma made it a tuple)
    RU = "ru"
    DE = "de"
    FR = "fr"
    PT = "pt"
    ZH_HANS = "zh-hans"
    ZH_HANT = "zh-hant"
    ES = "es"
    IT = "it"
    PL = "pl"           # Fixed: was "PL" (uppercase, inconsistent with API)
    UK = "uk"
    EN = "en"


class Platform(Enum):
    PC = "pc"
    PS4 = "ps4"
    XBOX = "xbox"
    SWITCH = "switch"
    MOBILE = "mobile"


class Scope(Enum):
    ME = "me"
    PROFILE = "profile"
    SETTINGS = "settings"
    CONTRACTS = "contracts"
    LEDGER = "ledger"
    REVIEWS = "reviews"
