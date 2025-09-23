"""
Legacy compatibility module for replicate-python v1.x type names.

This module provides backward compatibility for code that imports types
using the old v1.x import paths like:
    from replicate.model import Model
    from replicate.model import Version
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .types import Prediction as Prediction

# Import the actual types from their new locations
from .lib._models import Model as Model, Version as Version

# Also provide aliases for the response types for type checking
if TYPE_CHECKING:
    from .types import ModelGetResponse as ModelResponse
    from .types.models.version_get_response import VersionGetResponse as VersionResponse
else:
    # At runtime, make the response types available under legacy names
    from .types import ModelGetResponse as ModelResponse
    from .types.models.version_get_response import VersionGetResponse as VersionResponse

__all__ = [
    "Model",
    "Version",
    "Prediction",
    "ModelResponse",
    "VersionResponse",
]

