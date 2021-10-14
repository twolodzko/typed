from typing import Any, get_origin


def istype(obj: Any, annotation: type) -> bool:
    """Check if object is consistent with the annotation"""
    if get_origin(annotation) is None:
        if annotation is None:
            return obj is None
        return isinstance(obj, annotation)
    else:
        raise NotImplementedError("Currently only the basic types are supported")
