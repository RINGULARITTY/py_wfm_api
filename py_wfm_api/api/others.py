from typing import List
from py_wfm_api.api.core import get_request_wfm
from py_wfm_api.objects.other import Location, Npc, Mission  # Fixed: was scripts.wfm.src.objects.other


def get_locations() -> List[Location]:
    """Get list of all game locations."""
    return [Location(**l) for l in get_request_wfm("locations")]


def get_ncps() -> List[Npc]:
    """Get list of all NPCs."""
    return [Npc(**n) for n in get_request_wfm("npcs")]


def get_missions() -> List[Mission]:
    """Get list of all missions."""
    return [Mission(**m) for m in get_request_wfm("missions")]
