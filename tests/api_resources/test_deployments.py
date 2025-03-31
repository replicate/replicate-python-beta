# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import ReplicateClient, AsyncReplicateClient
from tests.utils import assert_matches_type
from replicate.types import (
    DeploymentListResponse,
    DeploymentCreateResponse,
    DeploymentUpdateResponse,
    DeploymentRetrieveResponse,
)
from replicate.pagination import SyncCursorURLPage, AsyncCursorURLPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ReplicateClient) -> None:
        deployment = client.deployments.create(
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            model="model",
            name="name",
            version="version",
        )
        assert_matches_type(DeploymentCreateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ReplicateClient) -> None:
        response = client.deployments.with_raw_response.create(
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            model="model",
            name="name",
            version="version",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentCreateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ReplicateClient) -> None:
        with client.deployments.with_streaming_response.create(
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            model="model",
            name="name",
            version="version",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentCreateResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ReplicateClient) -> None:
        deployment = client.deployments.retrieve(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ReplicateClient) -> None:
        response = client.deployments.with_raw_response.retrieve(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ReplicateClient) -> None:
        with client.deployments.with_streaming_response.retrieve(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_owner` but received ''"):
            client.deployments.with_raw_response.retrieve(
                deployment_name="deployment_name",
                deployment_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_name` but received ''"):
            client.deployments.with_raw_response.retrieve(
                deployment_name="",
                deployment_owner="deployment_owner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ReplicateClient) -> None:
        deployment = client.deployments.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )
        assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ReplicateClient) -> None:
        deployment = client.deployments.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            version="version",
        )
        assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ReplicateClient) -> None:
        response = client.deployments.with_raw_response.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ReplicateClient) -> None:
        with client.deployments.with_streaming_response.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_owner` but received ''"):
            client.deployments.with_raw_response.update(
                deployment_name="deployment_name",
                deployment_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_name` but received ''"):
            client.deployments.with_raw_response.update(
                deployment_name="",
                deployment_owner="deployment_owner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ReplicateClient) -> None:
        deployment = client.deployments.list()
        assert_matches_type(SyncCursorURLPage[DeploymentListResponse], deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ReplicateClient) -> None:
        response = client.deployments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(SyncCursorURLPage[DeploymentListResponse], deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ReplicateClient) -> None:
        with client.deployments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(SyncCursorURLPage[DeploymentListResponse], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ReplicateClient) -> None:
        deployment = client.deployments.delete(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ReplicateClient) -> None:
        response = client.deployments.with_raw_response.delete(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ReplicateClient) -> None:
        with client.deployments.with_streaming_response.delete(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert deployment is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: ReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_owner` but received ''"):
            client.deployments.with_raw_response.delete(
                deployment_name="deployment_name",
                deployment_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_name` but received ''"):
            client.deployments.with_raw_response.delete(
                deployment_name="",
                deployment_owner="deployment_owner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list_em_all(self, client: ReplicateClient) -> None:
        deployment = client.deployments.list_em_all()
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_em_all(self, client: ReplicateClient) -> None:
        response = client.deployments.with_raw_response.list_em_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_em_all(self, client: ReplicateClient) -> None:
        with client.deployments.with_streaming_response.list_em_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert deployment is None

        assert cast(Any, response.is_closed) is True


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.create(
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            model="model",
            name="name",
            version="version",
        )
        assert_matches_type(DeploymentCreateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.deployments.with_raw_response.create(
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            model="model",
            name="name",
            version="version",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentCreateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.deployments.with_streaming_response.create(
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            model="model",
            name="name",
            version="version",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentCreateResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.retrieve(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.deployments.with_raw_response.retrieve(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.deployments.with_streaming_response.retrieve(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentRetrieveResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_owner` but received ''"):
            await async_client.deployments.with_raw_response.retrieve(
                deployment_name="deployment_name",
                deployment_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_name` but received ''"):
            await async_client.deployments.with_raw_response.retrieve(
                deployment_name="",
                deployment_owner="deployment_owner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )
        assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
            hardware="hardware",
            max_instances=0,
            min_instances=0,
            version="version",
        )
        assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.deployments.with_raw_response.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.deployments.with_streaming_response.update(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentUpdateResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_owner` but received ''"):
            await async_client.deployments.with_raw_response.update(
                deployment_name="deployment_name",
                deployment_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_name` but received ''"):
            await async_client.deployments.with_raw_response.update(
                deployment_name="",
                deployment_owner="deployment_owner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.list()
        assert_matches_type(AsyncCursorURLPage[DeploymentListResponse], deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.deployments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(AsyncCursorURLPage[DeploymentListResponse], deployment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.deployments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(AsyncCursorURLPage[DeploymentListResponse], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.delete(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.deployments.with_raw_response.delete(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.deployments.with_streaming_response.delete(
            deployment_name="deployment_name",
            deployment_owner="deployment_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert deployment is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncReplicateClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_owner` but received ''"):
            await async_client.deployments.with_raw_response.delete(
                deployment_name="deployment_name",
                deployment_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_name` but received ''"):
            await async_client.deployments.with_raw_response.delete(
                deployment_name="",
                deployment_owner="deployment_owner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_em_all(self, async_client: AsyncReplicateClient) -> None:
        deployment = await async_client.deployments.list_em_all()
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_em_all(self, async_client: AsyncReplicateClient) -> None:
        response = await async_client.deployments.with_raw_response.list_em_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert deployment is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_em_all(self, async_client: AsyncReplicateClient) -> None:
        async with async_client.deployments.with_streaming_response.list_em_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert deployment is None

        assert cast(Any, response.is_closed) is True
