from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx
import pytest
from respx import MockRouter

import replicate
from replicate.lib._predictions_use import URLPath, SyncOutputIterator, AsyncOutputIterator

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"


# Mock prediction data for testing
def create_mock_prediction(
    status: str = "succeeded",
    output: Any = "test output",
    error: Optional[str] = None,
    logs: Optional[str] = None,
    urls: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    if urls is None:
        urls = {
            "get": "https://api.replicate.com/v1/predictions/test_prediction_id",
            "cancel": "https://api.replicate.com/v1/predictions/test_prediction_id/cancel",
            "web": "https://replicate.com/p/test_prediction_id",
        }

    return {
        "id": "test_prediction_id",
        "version": "test_version",
        "status": status,
        "input": {"prompt": "test prompt"},
        "output": output,
        "error": error,
        "logs": logs,
        "created_at": "2023-01-01T00:00:00Z",
        "started_at": "2023-01-01T00:00:01Z",
        "completed_at": "2023-01-01T00:00:02Z" if status in ["succeeded", "failed"] else None,
        "urls": urls,
        "model": "test-model",
        "data_removed": False,
    }


def create_mock_version() -> Dict[str, Any]:
    return {
        "cover_image_url": "https://replicate.delivery/xezq/7i7baf9dE93AP6bjmBZzqh3ZBkcB4pEtIb5dK9LajHbF0UyKA/output.mp4",
        "created_at": "2025-10-31T12:36:16.373813Z",
        "default_example": None,
        "description": "Fast GPU-powered concatenation of multiple videos, with short audio crossfades",
        "github_url": None,
        "latest_version": {
            "id": "11365b52712fbf76932e83bfef43a7ccb1af898fbefcd3da00ecea25d2a40f5e",
            "created_at": "2025-10-31T17:37:27.465191Z",
            "cog_version": "0.16.6",
            "openapi_schema": {
                "info": {"title": "Cog", "version": "0.1.0"},
                "paths": {},
                "openapi": "3.0.2",
                "components": {
                    "schemas": {
                        "Input": {
                            "type": "object",
                            "title": "Input",
                            "required": ["videos"],
                            "properties": {
                                "videos": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "title": "Videos",
                                    "description": "Videos to stitch together (can be uploaded files or URLs)",
                                },
                            },
                        },
                        "Output": {"type": "string", "title": "Output", "format": "uri"},
                        "Status": {
                            "enum": ["starting", "processing", "succeeded", "canceled", "failed"],
                            "type": "string",
                            "title": "Status",
                            "description": "An enumeration.",
                        },
                        "preset": {
                            "enum": [
                                "ultrafast",
                                "superfast",
                                "veryfast",
                                "faster",
                                "fast",
                                "medium",
                                "slow",
                                "slower",
                                "veryslow",
                            ],
                            "type": "string",
                            "title": "preset",
                            "description": "An enumeration.",
                        },
                        "WebhookEvent": {
                            "enum": ["start", "output", "logs", "completed"],
                            "type": "string",
                            "title": "WebhookEvent",
                            "description": "An enumeration.",
                        },
                        "ValidationError": {
                            "type": "object",
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "properties": {
                                "loc": {
                                    "type": "array",
                                    "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                                    "title": "Location",
                                },
                                "msg": {"type": "string", "title": "Message"},
                                "type": {"type": "string", "title": "Error Type"},
                            },
                        },
                        "PredictionRequest": {
                            "type": "object",
                            "title": "PredictionRequest",
                            "properties": {
                                "id": {"type": "string", "title": "Id", "Noneable": True},
                                "input": {"$ref": "#/components/schemas/Input", "Noneable": True},
                                "context": {
                                    "type": "object",
                                    "title": "Context",
                                    "Noneable": True,
                                    "additionalProperties": {"type": "string"},
                                },
                                "webhook": {
                                    "type": "string",
                                    "title": "Webhook",
                                    "format": "uri",
                                    "Noneable": True,
                                    "maxLength": 65536,
                                    "minLength": 1,
                                },
                                "created_at": {
                                    "type": "string",
                                    "title": "Created At",
                                    "format": "date-time",
                                    "Noneable": True,
                                },
                                "output_file_prefix": {
                                    "type": "string",
                                    "title": "Output File Prefix",
                                    "Noneable": True,
                                },
                                "webhook_events_filter": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/WebhookEvent"},
                                    "default": ["start", "output", "logs", "completed"],
                                    "Noneable": True,
                                },
                            },
                        },
                        "PredictionResponse": {
                            "type": "object",
                            "title": "PredictionResponse",
                            "properties": {
                                "id": {"type": "string", "title": "Id", "Noneable": True},
                                "logs": {"type": "string", "title": "Logs", "default": ""},
                                "error": {"type": "string", "title": "Error", "Noneable": True},
                                "input": {"$ref": "#/components/schemas/Input", "Noneable": True},
                                "output": {"$ref": "#/components/schemas/Output"},
                                "status": {"$ref": "#/components/schemas/Status", "Noneable": True},
                                "metrics": {
                                    "type": "object",
                                    "title": "Metrics",
                                    "Noneable": True,
                                    "additionalProperties": True,
                                },
                                "version": {"type": "string", "title": "Version", "Noneable": True},
                                "created_at": {
                                    "type": "string",
                                    "title": "Created At",
                                    "format": "date-time",
                                    "Noneable": True,
                                },
                                "started_at": {
                                    "type": "string",
                                    "title": "Started At",
                                    "format": "date-time",
                                    "Noneable": True,
                                },
                                "completed_at": {
                                    "type": "string",
                                    "title": "Completed At",
                                    "format": "date-time",
                                    "Noneable": True,
                                },
                            },
                        },
                        "HTTPValidationError": {
                            "type": "object",
                            "title": "HTTPValidationError",
                            "properties": {
                                "detail": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/ValidationError"},
                                    "title": "Detail",
                                }
                            },
                        },
                    }
                },
            },
        },
        "license_url": None,
        "name": "video-stitcher",
        "owner": "andreasjansson",
        "is_official": False,
        "paper_url": None,
        "run_count": 73,
        "url": "https://replicate.com/andreasjansson/video-stitcher",
        "visibility": "public",
        "weights_url": None,
    }


def async_list_fixture():
    async def inner():
        for x in ["https://example.com/image.png"]:
            yield x

    return inner()


class TestUse:
    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.parametrize(
        "inputs",
        [
            URLPath("https://example.com/image.png"),
            [URLPath("https://example.com/image.png")],
            {URLPath("https://example.com/image.png")},
            (x for x in [URLPath("https://example.com/image.png")]),
            {"file": URLPath("https://example.com/image.png")},
            SyncOutputIterator(lambda: (x for x in ["https://example.com/image.png"]), schema={}, is_concatenate=False),
        ],
    )
    def test_run_with_url_path(self, respx_mock: MockRouter, inputs) -> None:
        """Test basic model run functionality."""
        respx_mock.post("https://api.replicate.com/v1/models/andreasjansson/video-stitcher/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction())
        )
        respx_mock.get("https://api.replicate.com/v1/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction())
        )
        respx_mock.get("https://api.replicate.com/v1/models/andreasjansson/video-stitcher").mock(
            return_value=httpx.Response(200, json=create_mock_version())
        )
        respx_mock.get("https://api.replicate.com/v1/models/andreasjansson/video-stitcher/versions").mock(
            return_value=httpx.Response(404, json={})
        )

        model = replicate.use("andreasjansson/video-stitcher")
        output: Any = model(prompt=inputs)

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.parametrize(
        "inputs",
        [
            URLPath("https://example.com/image.png"),
            [URLPath("https://example.com/image.png")],
            {URLPath("https://example.com/image.png")},
            (x for x in [URLPath("https://example.com/image.png")]),
            {"file": URLPath("https://example.com/image.png")},
            AsyncOutputIterator(async_list_fixture, schema={}, is_concatenate=False),
        ],
    )
    async def test_run_with_url_path_async(self, respx_mock: MockRouter, inputs) -> None:
        """Test basic model run functionality."""
        respx_mock.post("https://api.replicate.com/v1/models/andreasjansson/video-stitcher/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction())
        )
        respx_mock.get("https://api.replicate.com/v1/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction())
        )
        respx_mock.get("https://api.replicate.com/v1/models/andreasjansson/video-stitcher").mock(
            return_value=httpx.Response(200, json=create_mock_version())
        )
        respx_mock.get("https://api.replicate.com/v1/models/andreasjansson/video-stitcher/versions").mock(
            return_value=httpx.Response(404, json={})
        )

        model = replicate.use("andreasjansson/video-stitcher", use_async=True)
        output: Any = await model(prompt=inputs)

        assert output == "test output"
