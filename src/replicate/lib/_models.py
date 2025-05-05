from __future__ import annotations

from typing import Tuple, Union, Optional
from typing_extensions import TypedDict


class Model:
    """A Replicate model."""

    def __init__(self, owner: str, name: str):
        self.owner = owner
        self.name = name


class Version:
    """A specific version of a Replicate model."""

    def __init__(self, id: str):
        self.id = id


class ModelVersionIdentifier(TypedDict, total=False):
    """A structure to identify a model version."""

    owner: str
    name: str
    version: str


def resolve_reference(
    ref: Union[Model, Version, ModelVersionIdentifier, str],
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Resolve a reference to a model or version to its components.

    Returns a tuple of (version, owner, name, version_id).
    """
    version = None
    owner = None
    name = None
    version_id = None

    if isinstance(ref, Model):
        owner = ref.owner
        name = ref.name
    elif isinstance(ref, Version):
        version_id = ref.id
    elif isinstance(ref, dict):
        owner = ref.get("owner")
        name = ref.get("name")
        version_id = ref.get("version")
    else:
        # Check if the string is a version ID (assumed to be a hash-like string)
        if "/" not in ref and len(ref) >= 32:
            version_id = ref
        else:
            # Handle owner/name or owner/name/version format
            parts = ref.split("/")
            if len(parts) >= 2:
                owner = parts[0]
                name = parts[1]
                if len(parts) >= 3:
                    version_id = parts[2]

    return version, owner, name, version_id
