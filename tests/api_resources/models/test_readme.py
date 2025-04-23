# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import ReplicateClient, AsyncReplicateClient
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReadme:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get(self, client: ReplicateClient) -> None:
        readme = client.models.readme.get(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert_matches_type(str, readme, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get(self, client: ReplicateClient) -> None:
        response = client.models.readme.with_raw_response.get(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        readme = response.parse()
        assert_matches_type(str, readme, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get(self, client: ReplicateClient) -> None:
        with client.models.readme.with_streaming_response.get(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            readme = response.parse()
            assert_matches_type(str, readme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.readme.with_raw_response.get(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.readme.with_raw_response.get(
                model_name="",
                model_owner="model_owner",
            )


class TestAsyncReadme:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get(self, async_client: AsyncReplicateClient) -> None:
        readme = await async_client.models.readme.get(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert_matches_type(str, readme, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.models.readme.with_raw_response.get(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        readme = await response.parse()
        assert_matches_type(str, readme, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.models.readme.with_streaming_response.get(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            readme = await response.parse()
            assert_matches_type(str, readme, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.readme.with_raw_response.get(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.readme.with_raw_response.get(
                model_name="",
                model_owner="model_owner",
            )
