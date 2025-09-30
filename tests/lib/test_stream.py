from __future__ import annotations

import os
from typing import Any, Iterator

import httpx
import pytest
from respx import MockRouter

from replicate import Replicate, AsyncReplicate

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"


def create_mock_prediction_json(stream_url: str | None = None) -> dict[str, Any]:
    """Helper to create a complete prediction JSON response"""
    prediction: dict[str, Any] = {
        "id": "test-prediction-id",
        "created_at": "2023-01-01T00:00:00Z",
        "data_removed": False,
        "input": {"prompt": "Test"},
        "model": "test-model",
        "output": None,
        "status": "starting",
        "version": "test-version-id",
        "urls": {
            "get": f"{base_url}/predictions/test-prediction-id",
            "cancel": f"{base_url}/predictions/test-prediction-id/cancel",
            "web": "https://replicate.com/p/test-prediction-id",
        },
    }
    if stream_url:
        prediction["urls"]["stream"] = stream_url  # type: ignore[index]
    return prediction


def test_stream_with_model_owner_name(respx_mock: MockRouter) -> None:
    """Test streaming with owner/name format"""
    client = Replicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    # Mock the prediction creation
    respx_mock.post(f"{base_url}/models/meta/meta-llama-3-70b-instruct/predictions").mock(
        return_value=httpx.Response(
            201,
            json=create_mock_prediction_json(stream_url=f"{base_url}/stream/test-prediction-id"),
        )
    )

    # Mock the SSE stream endpoint
    def stream_content() -> Iterator[bytes]:
        yield b"data: Hello\n\n"
        yield b"data:  world\n\n"
        yield b"data: !\n\n"

    respx_mock.get(f"{base_url}/stream/test-prediction-id").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=stream_content(),
        )
    )

    # Stream the model
    output: list[str] = []
    for chunk in client.stream(
        "meta/meta-llama-3-70b-instruct",
        input={"prompt": "Say hello"},
    ):
        output.append(chunk)

    assert output == ["Hello", " world", "!"]


def test_stream_with_version_id(respx_mock: MockRouter) -> None:
    """Test streaming with version ID"""
    client = Replicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)
    version_id = "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa"

    # Mock the prediction creation
    respx_mock.post(f"{base_url}/predictions").mock(
        return_value=httpx.Response(
            201,
            json=create_mock_prediction_json(stream_url=f"{base_url}/stream/test-prediction-id"),
        )
    )

    # Mock the SSE stream endpoint
    def stream_content() -> Iterator[bytes]:
        yield b"data: Test\n\n"
        yield b"data: output\n\n"

    respx_mock.get(f"{base_url}/stream/test-prediction-id").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=stream_content(),
        )
    )

    # Stream the model
    output: list[str] = []
    for chunk in client.stream(
        version_id,
        input={"prompt": "Test"},
    ):
        output.append(chunk)

    assert output == ["Test", "output"]


def test_stream_no_stream_url_raises_error(respx_mock: MockRouter) -> None:
    """Test that streaming raises an error when model doesn't support streaming"""
    client = Replicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    # Mock the prediction creation without stream URL
    respx_mock.post(f"{base_url}/models/owner/model/predictions").mock(
        return_value=httpx.Response(
            201,
            json=create_mock_prediction_json(stream_url=None),
        )
    )

    # Try to stream and expect an error
    with pytest.raises(ValueError, match="Model does not support streaming"):
        for _ in client.stream("owner/model", input={"prompt": "Test"}):
            pass


@pytest.mark.asyncio
async def test_async_stream_with_model_owner_name(respx_mock: MockRouter) -> None:
    """Test async streaming with owner/name format"""
    async_client = AsyncReplicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    # Mock the prediction creation
    respx_mock.post(f"{base_url}/models/meta/meta-llama-3-70b-instruct/predictions").mock(
        return_value=httpx.Response(
            201,
            json=create_mock_prediction_json(stream_url=f"{base_url}/stream/test-prediction-id"),
        )
    )

    # Mock the SSE stream endpoint
    async def stream_content():
        yield b"data: Async\n\n"
        yield b"data:  test\n\n"

    respx_mock.get(f"{base_url}/stream/test-prediction-id").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=stream_content(),
        )
    )

    # Stream the model
    output: list[str] = []
    async for chunk in async_client.stream(
        "meta/meta-llama-3-70b-instruct",
        input={"prompt": "Say hello"},
    ):
        output.append(chunk)

    assert output == ["Async", " test"]


@pytest.mark.asyncio
async def test_async_stream_no_stream_url_raises_error(respx_mock: MockRouter) -> None:
    """Test that async streaming raises an error when model doesn't support streaming"""
    async_client = AsyncReplicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    # Mock the prediction creation without stream URL
    respx_mock.post(f"{base_url}/models/owner/model/predictions").mock(
        return_value=httpx.Response(
            201,
            json=create_mock_prediction_json(stream_url=None),
        )
    )

    # Try to stream and expect an error
    with pytest.raises(ValueError, match="Model does not support streaming"):
        async for _ in async_client.stream("owner/model", input={"prompt": "Test"}):
            pass


def test_stream_module_level(respx_mock: MockRouter) -> None:
    """Test that module-level stream function works"""
    import replicate

    # Set up module level client configuration
    replicate.base_url = base_url
    replicate.bearer_token = bearer_token

    # Mock the prediction creation
    respx_mock.post(f"{base_url}/models/meta/meta-llama-3-70b-instruct/predictions").mock(
        return_value=httpx.Response(
            201,
            json=create_mock_prediction_json(stream_url=f"{base_url}/stream/test-prediction-id"),
        )
    )

    # Mock the SSE stream endpoint
    def stream_content() -> Iterator[bytes]:
        yield b"data: Module\n\n"
        yield b"data:  level\n\n"

    respx_mock.get(f"{base_url}/stream/test-prediction-id").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=stream_content(),
        )
    )

    # Stream using module-level function
    output: list[str] = []
    for chunk in replicate.stream(
        "meta/meta-llama-3-70b-instruct",
        input={"prompt": "Test"},
    ):
        output.append(chunk)

    assert output == ["Module", " level"]
