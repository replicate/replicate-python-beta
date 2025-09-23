"""
Custom models functionality with backward compatibility.
"""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Union, overload

from .._types import NOT_GIVEN, NotGiven
from ._models import ModelVersionIdentifier

if TYPE_CHECKING:
    import httpx

    from .._types import Body, Query, Headers
    from ..resources.models.models import ModelsResource, AsyncModelsResource
    from ..types.model_get_response import ModelGetResponse


def _parse_model_args(
    model_or_owner: str | NotGiven,
    model_owner: str | NotGiven,
    model_name: str | NotGiven,
) -> tuple[str, str]:
    """Parse model arguments and return (owner, name)."""
    # Handle legacy format: models.get("owner/name")
    if model_or_owner is not NOT_GIVEN:
        if model_owner is not NOT_GIVEN or model_name is not NOT_GIVEN:
            raise ValueError(
                "Cannot specify both positional 'model_or_owner' and keyword arguments "
                "'model_owner'/'model_name'. Use either the legacy format "
                "models.get('owner/name') or the new format models.get(model_owner='owner', model_name='name')."
            )

        # Type guard: model_or_owner is definitely a string here
        assert isinstance(model_or_owner, str)

        # Parse the owner/name format
        if "/" not in model_or_owner:
            raise ValueError(
                f"Invalid model reference '{model_or_owner}'. "
                "Expected format: 'owner/name' (e.g., 'stability-ai/stable-diffusion')"
            )

        try:
            parsed = ModelVersionIdentifier.parse(model_or_owner)
            return parsed.owner, parsed.name
        except ValueError as e:
            raise ValueError(
                f"Invalid model reference '{model_or_owner}'. "
                f"Expected format: 'owner/name' (e.g., 'stability-ai/stable-diffusion'). "
                f"Error: {e}"
            ) from e

    # Validate required parameters for new format
    if model_owner is NOT_GIVEN or model_name is NOT_GIVEN:
        raise ValueError(
            "model_owner and model_name are required. "
            "Use either models.get('owner/name') or models.get(model_owner='owner', model_name='name')"
        )

    return model_owner, model_name  # type: ignore[return-value]


@overload
def patch_models_resource(models_resource: "ModelsResource") -> "ModelsResource": ...


@overload
def patch_models_resource(models_resource: "AsyncModelsResource") -> "AsyncModelsResource": ...


def patch_models_resource(
    models_resource: Union["ModelsResource", "AsyncModelsResource"],
) -> Union["ModelsResource", "AsyncModelsResource"]:
    """Patch a models resource to add backward compatibility."""
    original_get = models_resource.get
    is_async = inspect.iscoroutinefunction(original_get)

    if is_async:

        async def async_get_wrapper(
            model_or_owner: str | NotGiven = NOT_GIVEN,
            *,
            model_owner: str | NotGiven = NOT_GIVEN,
            model_name: str | NotGiven = NOT_GIVEN,
            extra_headers: "Headers | None" = None,
            extra_query: "Query | None" = None,
            extra_body: "Body | None" = None,
            timeout: "float | httpx.Timeout | None | NotGiven" = NOT_GIVEN,
        ) -> "ModelGetResponse":
            owner, name = _parse_model_args(model_or_owner, model_owner, model_name)
            return await models_resource._original_get(  # type: ignore[misc,no-any-return,attr-defined]
                model_owner=owner,
                model_name=name,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )

        wrapper = async_get_wrapper
    else:

        def sync_get_wrapper(
            model_or_owner: str | NotGiven = NOT_GIVEN,
            *,
            model_owner: str | NotGiven = NOT_GIVEN,
            model_name: str | NotGiven = NOT_GIVEN,
            extra_headers: "Headers | None" = None,
            extra_query: "Query | None" = None,
            extra_body: "Body | None" = None,
            timeout: "float | httpx.Timeout | None | NotGiven" = NOT_GIVEN,
        ) -> "ModelGetResponse":
            owner, name = _parse_model_args(model_or_owner, model_owner, model_name)
            return models_resource._original_get(  # type: ignore[misc,return-value,attr-defined]
                model_owner=owner,
                model_name=name,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )

        wrapper = sync_get_wrapper  # type: ignore[assignment]

    # Store original method for tests and replace with wrapper
    models_resource._original_get = original_get  # type: ignore[attr-defined,union-attr]
    models_resource.get = wrapper  # type: ignore[method-assign]
    return models_resource
