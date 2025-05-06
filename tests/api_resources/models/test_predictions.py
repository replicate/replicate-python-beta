# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import Replicate, AsyncReplicate
from tests.utils import assert_matches_type
from replicate.types import Prediction

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPredictions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Replicate) -> None:
        prediction = client.models.predictions.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )
        assert_matches_type(Prediction, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Replicate) -> None:
        prediction = client.models.predictions.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
            stream=True,
            webhook="webhook",
            webhook_events_filter=["start"],
            prefer="wait=5",
        )
        assert_matches_type(Prediction, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Replicate) -> None:
        response = client.models.predictions.with_raw_response.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = response.parse()
        assert_matches_type(Prediction, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Replicate) -> None:
        with client.models.predictions.with_streaming_response.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = response.parse()
            assert_matches_type(Prediction, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: Replicate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.predictions.with_raw_response.create(
                model_name="model_name",
                model_owner="",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.predictions.with_raw_response.create(
                model_name="",
                model_owner="model_owner",
                input={},
            )


class TestAsyncPredictions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncReplicate) -> None:
        prediction = await async_client.models.predictions.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )
        assert_matches_type(Prediction, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncReplicate) -> None:
        prediction = await async_client.models.predictions.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
            stream=True,
            webhook="webhook",
            webhook_events_filter=["start"],
            prefer="wait=5",
        )
        assert_matches_type(Prediction, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncReplicate) -> None:
        response = await async_client.models.predictions.with_raw_response.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = await response.parse()
        assert_matches_type(Prediction, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncReplicate) -> None:
        async with async_client.models.predictions.with_streaming_response.create(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = await response.parse()
            assert_matches_type(Prediction, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncReplicate) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.predictions.with_raw_response.create(
                model_name="model_name",
                model_owner="",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.predictions.with_raw_response.create(
                model_name="",
                model_owner="model_owner",
                input={},
            )
