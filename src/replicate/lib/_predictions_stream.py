from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union, Iterator, Optional
from collections.abc import AsyncIterator
from typing_extensions import Unpack

from replicate.lib._files import FileEncodingStrategy
from replicate.types.prediction_create_params import PredictionCreateParamsWithoutVersion

from ..types import PredictionCreateParams
from ._models import Model, Version, ModelVersionIdentifier, resolve_reference

if TYPE_CHECKING:
    from .._client import Replicate, AsyncReplicate

_STREAM_DOCSTRING = """
Stream output from a model prediction.

This creates a prediction and returns an iterator that yields output chunks
as strings as they become available from the streaming API.

Args:
    ref: Reference to the model or version to run. Can be:
        - A string containing a version ID
        - A string with owner/name format (e.g. "replicate/hello-world")
        - A string with owner/name:version format
        - A Model instance
        - A Version instance
        - A ModelVersionIdentifier dictionary
    file_encoding_strategy: Strategy for encoding file inputs
    **params: Additional parameters including the required "input" dictionary

Yields:
    str: Output chunks from the model as they become available

Raises:
    ValueError: If the reference format is invalid
    ReplicateError: If the prediction fails or streaming is not available
"""


def _resolve_reference(
    ref: Union[Model, Version, ModelVersionIdentifier, str],
) -> Tuple[Optional[Version], Optional[str], Optional[str], Optional[str]]:
    """Resolve a model reference to its components, with fallback for plain version IDs."""
    try:
        return resolve_reference(ref)
    except ValueError:
        # If resolution fails, treat it as a version ID if it's a string
        if isinstance(ref, str):
            return None, None, None, ref
        else:
            raise


def stream(
    client: "Replicate",
    ref: Union[Model, Version, ModelVersionIdentifier, str],
    *,
    file_encoding_strategy: Optional["FileEncodingStrategy"] = None,
    **params: Unpack[PredictionCreateParamsWithoutVersion],
) -> Iterator[str]:
    __doc__ = _STREAM_DOCSTRING
    version, owner, name, version_id = _resolve_reference(ref)

    # Create prediction
    if version_id is not None:
        params_with_version: PredictionCreateParams = {**params, "version": version_id}
        prediction = client.predictions.create(file_encoding_strategy=file_encoding_strategy, **params_with_version)
    elif owner and name:
        prediction = client.models.predictions.create(
            file_encoding_strategy=file_encoding_strategy, model_owner=owner, model_name=name, **params
        )
    else:
        if isinstance(ref, str):
            params_with_version = {**params, "version": ref}
            prediction = client.predictions.create(file_encoding_strategy=file_encoding_strategy, **params_with_version)
        else:
            raise ValueError(
                f"Invalid reference format: {ref}. Expected a model name ('owner/name'), "
                "a version ID, a Model object, a Version object, or a ModelVersionIdentifier."
            )

    # Check if streaming URL is available
    if not prediction.urls or not prediction.urls.stream:
        raise ValueError("Model does not support streaming. The prediction URLs do not include a stream endpoint.")

    stream_url = prediction.urls.stream

    with client._client.stream(
        "GET",
        stream_url,
        headers={
            "Accept": "text/event-stream",
            "Cache-Control": "no-store",
        },
        timeout=None,  # No timeout for streaming
    ) as response:
        response.raise_for_status()

        # Parse SSE events and yield output chunks
        decoder = client._make_sse_decoder()
        for sse in decoder.iter_bytes(response.iter_bytes()):
            # The SSE data contains the output chunks
            if sse.data:
                yield sse.data


async def async_stream(
    client: "AsyncReplicate",
    ref: Union[Model, Version, ModelVersionIdentifier, str],
    *,
    file_encoding_strategy: Optional["FileEncodingStrategy"] = None,
    **params: Unpack[PredictionCreateParamsWithoutVersion],
) -> AsyncIterator[str]:
    __doc__ = _STREAM_DOCSTRING
    version, owner, name, version_id = _resolve_reference(ref)

    # Create prediction
    if version_id is not None:
        params_with_version: PredictionCreateParams = {**params, "version": version_id}
        prediction = await client.predictions.create(
            file_encoding_strategy=file_encoding_strategy, **params_with_version
        )
    elif owner and name:
        prediction = await client.models.predictions.create(
            file_encoding_strategy=file_encoding_strategy, model_owner=owner, model_name=name, **params
        )
    else:
        if isinstance(ref, str):
            params_with_version = {**params, "version": ref}
            prediction = await client.predictions.create(
                file_encoding_strategy=file_encoding_strategy, **params_with_version
            )
        else:
            raise ValueError(
                f"Invalid reference format: {ref}. Expected a model name ('owner/name'), "
                "a version ID, a Model object, a Version object, or a ModelVersionIdentifier."
            )

    # Check if streaming URL is available
    if not prediction.urls or not prediction.urls.stream:
        raise ValueError("Model does not support streaming. The prediction URLs do not include a stream endpoint.")

    stream_url = prediction.urls.stream

    async with client._client.stream(
        "GET",
        stream_url,
        headers={
            "Accept": "text/event-stream",
            "Cache-Control": "no-store",
        },
        timeout=None,  # No timeout for streaming
    ) as response:
        response.raise_for_status()

        # Parse SSE events and yield output chunks
        decoder = client._make_sse_decoder()
        async for sse in decoder.aiter_bytes(response.aiter_bytes()):
            # The SSE data contains the output chunks
            if sse.data:
                yield sse.data
