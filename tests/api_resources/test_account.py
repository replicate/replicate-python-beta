# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from replicate import Replicate, AsyncReplicate
from tests.utils import assert_matches_type
from replicate.types import AccountGetResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccount:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get(self, client: Replicate) -> None:
        account = client.account.get()
        assert_matches_type(AccountGetResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get(self, client: Replicate) -> None:
        response = client.account.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountGetResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get(self, client: Replicate) -> None:
        with client.account.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountGetResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAccount:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get(self, async_client: AsyncReplicate) -> None:
        account = await async_client.account.get()
        assert_matches_type(AccountGetResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncReplicate) -> None:
        response = await async_client.account.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountGetResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncReplicate) -> None:
        async with async_client.account.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountGetResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True
