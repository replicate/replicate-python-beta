# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import TypeAlias

__all__ = ["PredictionOutput"]

# todo: this shouldn't need to be custom code. We should update the spec to include the `Optional[List[str]]` type
PredictionOutput: TypeAlias = Union[
    Optional[Dict[str, object]], Optional[List[Dict[str, object]]], Optional[List[str]], Optional[str], Optional[float], Optional[bool]
]
