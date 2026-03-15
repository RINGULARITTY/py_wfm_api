from typing import List
from py_wfm_api.api.core import get_request_wfm, validate_slug
from py_wfm_api.objects.lich_weapons import SisterWeapon, SisterEphemera, SisterQuirk


def get_sister_weapons() -> List[SisterWeapon]:
    """Get list of all tradable Sister of Parvos weapons."""
    return [SisterWeapon(**w) for w in get_request_wfm("sister/weapons")]


def get_sister_weapon_info(slug: str) -> SisterWeapon:
    """Get full info about a specific Sister weapon."""
    return SisterWeapon(**get_request_wfm(f"sister/weapon/{validate_slug(slug)}"))


def get_sister_ephemeras() -> List[SisterEphemera]:
    """Get list of all Sister ephemeras."""
    return [SisterEphemera(**e) for e in get_request_wfm("sister/ephemeras")]


def get_sister_quirks() -> List[SisterQuirk]:
    """Get list of all Sister quirks."""
    return [SisterQuirk(**q) for q in get_request_wfm("sister/quirks")]
