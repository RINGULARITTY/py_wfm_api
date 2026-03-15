from typing import List
from py_wfm_api.api.core import get_request_wfm, validate_slug
from py_wfm_api.objects.lich_weapons import LichWeapon, LichEphemera, LichQuirk


def get_lich_weapons() -> List[LichWeapon]:
    """Get list of all tradable Lich weapons."""
    return [LichWeapon(**w) for w in get_request_wfm("lich/weapons")]


def get_lich_weapon_info(slug: str) -> LichWeapon:
    """Get full info about a specific Lich weapon."""
    return LichWeapon(**get_request_wfm(f"lich/weapon/{validate_slug(slug)}"))


def get_lich_ephemeras() -> List[LichEphemera]:
    """Get list of all Lich ephemeras."""
    return [LichEphemera(**e) for e in get_request_wfm("lich/ephemeras")]


def get_lich_quirks() -> List[LichQuirk]:
    """Get list of all Lich quirks."""
    return [LichQuirk(**q) for q in get_request_wfm("lich/quirks")]
