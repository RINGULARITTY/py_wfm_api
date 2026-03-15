import dataclasses
from typing import Type, TypeVar

T = TypeVar("T")


def dc_from_dict(cls: Type[T], data: dict) -> T:
    """Instantiate a dataclass, silently ignoring keys not declared in its fields.

    This makes deserialization resilient to API additions without requiring
    model updates every time the server adds a new field.
    """
    known = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in known})


def parse_i18n(cls: Type[T], data: dict) -> dict:
    """Convert a raw i18n dict from the API into {Language → dataclass} entries.

    - String keys are converted to Language enum values.
    - Dict values are instantiated as *cls*, with unknown fields silently ignored.
    """
    from py_wfm_api.objects.categories import Language

    if not data:
        return {}
    result = {}
    for k, v in data.items():
        try:
            lang = Language(k) if isinstance(k, str) else k
        except ValueError:
            lang = k
        result[lang] = dc_from_dict(cls, v) if isinstance(v, dict) else v
    return result
