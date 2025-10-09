"""Tests for models.get() backward compatibility with legacy owner/name format."""

import os

import httpx
import pytest
from respx import MockRouter

from replicate import Replicate, AsyncReplicate

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"


def mock_model_response():
    """Mock model response data."""
    return {
        "url": "https://replicate.com/stability-ai/stable-diffusion",
        "owner": "stability-ai",
        "name": "stable-diffusion",
        "description": "A model for generating images from text prompts",
        "visibility": "public",
        "github_url": None,
        "paper_url": None,
        "license_url": None,
        "run_count": 12345,
        "cover_image_url": "https://example.com/cover.jpg",
        "default_example": None,
        "latest_version": None,
    }


class TestModelsGetLegacyFormat:
    """Test legacy format: models.get('owner/name')."""

    client = Replicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    @pytest.mark.respx(base_url=base_url)
    def test_legacy_format_basic(self, respx_mock: MockRouter):
        """Test basic legacy format with owner/name."""
        respx_mock.get("/models/stability-ai/stable-diffusion").mock(
            return_value=httpx.Response(200, json=mock_model_response())
        )

        model = self.client.models.get("stability-ai/stable-diffusion")

        assert model.owner == "stability-ai"
        assert model.name == "stable-diffusion"

    @pytest.mark.respx(base_url=base_url)
    def test_legacy_format_with_hyphens_and_dots(self, respx_mock: MockRouter):
        """Test legacy format with hyphenated names and dots."""
        response_data = {**mock_model_response(), "owner": "black-forest-labs", "name": "flux-1.1-pro"}
        respx_mock.get("/models/black-forest-labs/flux-1.1-pro").mock(
            return_value=httpx.Response(200, json=response_data)
        )

        model = self.client.models.get("black-forest-labs/flux-1.1-pro")

        assert model.owner == "black-forest-labs"
        assert model.name == "flux-1.1-pro"

    @pytest.mark.respx(base_url=base_url)
    def test_legacy_format_splits_on_first_slash_only(self, respx_mock: MockRouter):
        """Test legacy format splits on first slash only."""
        response_data = {**mock_model_response(), "owner": "owner", "name": "name/with/slashes"}
        respx_mock.get("/models/owner/name/with/slashes").mock(return_value=httpx.Response(200, json=response_data))

        model = self.client.models.get("owner/name/with/slashes")

        assert model.owner == "owner"
        assert model.name == "name/with/slashes"

    def test_legacy_format_error_no_slash(self):
        """Test error when legacy format has no slash."""
        with pytest.raises(ValueError, match="Invalid model reference 'invalid-format'.*Expected format: 'owner/name'"):
            self.client.models.get("invalid-format")

    def test_legacy_format_error_mixed_with_kwargs(self):
        """Test error when mixing positional and keyword arguments."""
        with pytest.raises(ValueError, match="Cannot specify both positional and keyword arguments"):
            self.client.models.get("owner/name", model_owner="other-owner")  # type: ignore[call-overload]


class TestModelsGetNewFormat:
    """Test new format: models.get(model_owner='owner', model_name='name')."""

    client = Replicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    @pytest.mark.respx(base_url=base_url)
    def test_new_format_basic(self, respx_mock: MockRouter):
        """Test basic new format with keyword arguments."""
        respx_mock.get("/models/stability-ai/stable-diffusion").mock(
            return_value=httpx.Response(200, json=mock_model_response())
        )

        model = self.client.models.get(model_owner="stability-ai", model_name="stable-diffusion")

        assert model.owner == "stability-ai"
        assert model.name == "stable-diffusion"

    def test_new_format_error_missing_params(self):
        """Test error when required parameters are missing."""
        with pytest.raises(ValueError, match="model_owner and model_name are required"):
            self.client.models.get()  # type: ignore[call-overload]


class TestAsyncModelsGetLegacyFormat:
    """Test async legacy format."""

    client = AsyncReplicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.asyncio
    async def test_async_legacy_format_basic(self, respx_mock: MockRouter):
        """Test async basic legacy format."""
        respx_mock.get("/models/stability-ai/stable-diffusion").mock(
            return_value=httpx.Response(200, json=mock_model_response())
        )

        model = await self.client.models.get("stability-ai/stable-diffusion")

        assert model.owner == "stability-ai"
        assert model.name == "stable-diffusion"

    @pytest.mark.asyncio
    async def test_async_legacy_format_error_no_slash(self):
        """Test async error when legacy format has no slash."""
        with pytest.raises(ValueError, match="Invalid model reference 'invalid-format'.*Expected format: 'owner/name'"):
            await self.client.models.get("invalid-format")

    @pytest.mark.asyncio
    async def test_async_legacy_format_error_mixed(self):
        """Test async error when mixing formats."""
        with pytest.raises(ValueError, match="Cannot specify both positional and keyword arguments"):
            await self.client.models.get("owner/name", model_owner="other")  # type: ignore[call-overload]


class TestAsyncModelsGetNewFormat:
    """Test async new format."""

    client = AsyncReplicate(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.asyncio
    async def test_async_new_format_basic(self, respx_mock: MockRouter):
        """Test async new format."""
        respx_mock.get("/models/stability-ai/stable-diffusion").mock(
            return_value=httpx.Response(200, json=mock_model_response())
        )

        model = await self.client.models.get(model_owner="stability-ai", model_name="stable-diffusion")

        assert model.owner == "stability-ai"
        assert model.name == "stable-diffusion"

    @pytest.mark.asyncio
    async def test_async_new_format_error_missing_params(self):
        """Test async error when required parameters are missing."""
        with pytest.raises(ValueError, match="model_owner and model_name are required"):
            await self.client.models.get()  # type: ignore[call-overload]
