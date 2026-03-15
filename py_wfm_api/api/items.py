from typing import List, Tuple
from py_wfm_api.api.core import get_request_wfm, validate_slug
from py_wfm_api.objects.item import ItemJson

def get_tradable_items() -> List[ItemJson]:
    """Get list of all tradable items"""
    return [ItemJson(**ti) for ti in get_request_wfm(f"items")] 

def get_item_info(slug: str) -> ItemJson:
    """Get full info about one, particular item"""
    return ItemJson(**get_request_wfm(f"items/{validate_slug(slug)}"))

def get_item_set_info(slug: str) -> Tuple[str, List[ItemJson]]:
    """Retrieve Information on Item Sets"""
    res = get_request_wfm(f"items/{validate_slug(slug)}/set")
    return res["id"], [ItemJson(**i) for i in res["items"]]