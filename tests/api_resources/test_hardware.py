# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import ReplicateClient, AsyncReplicateClient
from tests.utils import assert_matches_type
from replicate.types import HardwareListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHardware:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ReplicateClient) -> None:
        hardware = client.hardware.list()
        assert_matches_type(HardwareListResponse, hardware, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ReplicateClient) -> None:
        response = client.hardware.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hardware = response.parse()
        assert_matches_type(HardwareListResponse, hardware, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ReplicateClient) -> None:
        with client.hardware.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hardware = response.parse()
            assert_matches_type(HardwareListResponse, hardware, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_collections(self, client: ReplicateClient) -> None:
        hardware = client.hardware.retrieve_collections(
            "collection_slug",
        )
        assert hardware is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_collections(self, client: ReplicateClient) -> None:
        response = client.hardware.with_raw_response.retrieve_collections(
            "collection_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hardware = response.parse()
        assert hardware is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_collections(self, client: ReplicateClient) -> None:
        with client.hardware.with_streaming_response.retrieve_collections(
            "collection_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hardware = response.parse()
            assert hardware is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_collections(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_slug` but received ''"):
            client.hardware.with_raw_response.retrieve_collections(
                "",
            )


class TestAsyncHardware:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncReplicateClient) -> None:
        hardware = await async_client.hardware.list()
        assert_matches_type(HardwareListResponse, hardware, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.hardware.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hardware = await response.parse()
        assert_matches_type(HardwareListResponse, hardware, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.hardware.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hardware = await response.parse()
            assert_matches_type(HardwareListResponse, hardware, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_collections(self, async_client: AsyncReplicateClient) -> None:
        hardware = await async_client.hardware.retrieve_collections(
            "collection_slug",
        )
        assert hardware is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_collections(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.hardware.with_raw_response.retrieve_collections(
            "collection_slug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hardware = await response.parse()
        assert hardware is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_collections(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.hardware.with_streaming_response.retrieve_collections(
            "collection_slug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hardware = await response.parse()
            assert hardware is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_collections(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_slug` but received ''"):
            await async_client.hardware.with_raw_response.retrieve_collections(
                "",
            )
