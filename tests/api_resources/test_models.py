# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import ReplicateClient, AsyncReplicateClient
from tests.utils import assert_matches_type
from replicate.types import Prediction

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ReplicateClient) -> None:
        model = client.models.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: ReplicateClient) -> None:
        model = client.models.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
            cover_image_url="cover_image_url",
            description="description",
            github_url="github_url",
            license_url="license_url",
            paper_url="paper_url",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ReplicateClient) -> None:
        response = client.models.with_raw_response.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ReplicateClient) -> None:
        with client.models.with_streaming_response.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ReplicateClient) -> None:
        model = client.models.retrieve(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ReplicateClient) -> None:
        response = client.models.with_raw_response.retrieve(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ReplicateClient) -> None:
        with client.models.with_streaming_response.retrieve(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.with_raw_response.retrieve(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.with_raw_response.retrieve(
                model_name="",
                model_owner="model_owner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ReplicateClient) -> None:
        model = client.models.list()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ReplicateClient) -> None:
        response = client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ReplicateClient) -> None:
        with client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ReplicateClient) -> None:
        model = client.models.delete(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ReplicateClient) -> None:
        response = client.models.with_raw_response.delete(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ReplicateClient) -> None:
        with client.models.with_streaming_response.delete(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.with_raw_response.delete(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.with_raw_response.delete(
                model_name="",
                model_owner="model_owner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_prediction(self, client: ReplicateClient) -> None:
        model = client.models.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )
        assert_matches_type(Prediction, model, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_prediction_with_all_params(self, client: ReplicateClient) -> None:
        model = client.models.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
            stream=True,
            webhook="webhook",
            webhook_events_filter=["start"],
            prefer="wait=5",
        )
        assert_matches_type(Prediction, model, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_prediction(self, client: ReplicateClient) -> None:
        response = client.models.with_raw_response.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = response.parse()
        assert_matches_type(Prediction, model, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_prediction(self, client: ReplicateClient) -> None:
        with client.models.with_streaming_response.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = response.parse()
            assert_matches_type(Prediction, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_prediction(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.with_raw_response.create_prediction(
                model_name="model_name",
                model_owner="",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.with_raw_response.create_prediction(
                model_name="",
                model_owner="model_owner",
                input={},
            )


class TestAsyncModels:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
            cover_image_url="cover_image_url",
            description="description",
            github_url="github_url",
            license_url="license_url",
            paper_url="paper_url",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.models.with_raw_response.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.models.with_streaming_response.create(
            hardware="hardware",
            name="name",
            owner="owner",
            visibility="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.retrieve(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.models.with_raw_response.retrieve(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.models.with_streaming_response.retrieve(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.with_raw_response.retrieve(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.with_raw_response.retrieve(
                model_name="",
                model_owner="model_owner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.list()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.models.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.models.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.delete(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.models.with_raw_response.delete(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert model is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.models.with_streaming_response.delete(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert model is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.with_raw_response.delete(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.with_raw_response.delete(
                model_name="",
                model_owner="model_owner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_prediction(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )
        assert_matches_type(Prediction, model, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_prediction_with_all_params(self, async_client: AsyncReplicateClient) -> None:
        model = await async_client.models.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
            stream=True,
            webhook="webhook",
            webhook_events_filter=["start"],
            prefer="wait=5",
        )
        assert_matches_type(Prediction, model, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_prediction(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.models.with_raw_response.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        model = await response.parse()
        assert_matches_type(Prediction, model, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_prediction(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.models.with_streaming_response.create_prediction(
            model_name="model_name",
            model_owner="model_owner",
            input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            model = await response.parse()
            assert_matches_type(Prediction, model, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_prediction(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.with_raw_response.create_prediction(
                model_name="model_name",
                model_owner="",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.with_raw_response.create_prediction(
                model_name="",
                model_owner="model_owner",
                input={},
            )
