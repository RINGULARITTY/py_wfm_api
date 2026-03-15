from typing import List
from py_wfm_api.api.core import get_request_wfm, validate_slug
from py_wfm_api.objects.riven import Riven, RivenAttribute

def get_tradable_riven_items() -> List[Riven]:
    """Get list of all tradable riven items"""
    return [Riven(**ri) for ri in get_request_wfm(f"riven/weapons")]

def get_riven_info(slug: str) -> List[Riven]:
    """Get full info about one, particular riven item"""
    return [Riven(**ri) for ri in get_request_wfm(f"riven/weapon/{validate_slug(slug)}")]

def get_riven_attributes() -> List[RivenAttribute]:
    """Get list of all attributes for riven weapons"""
    return [RivenAttribute(**ra) for ra in get_request_wfm(f"riven/attributes")]