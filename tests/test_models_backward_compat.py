"""
Tests for backward compatibility in models.get() method.
"""

from unittest.mock import Mock, AsyncMock, patch

import pytest

from replicate import Replicate, AsyncReplicate
from replicate._types import NOT_GIVEN
from replicate.types.model_get_response import ModelGetResponse


@pytest.fixture
def mock_model_response():
    """Mock response for model.get requests."""
    return ModelGetResponse(
        url="https://replicate.com/stability-ai/stable-diffusion",
        owner="stability-ai",
        name="stable-diffusion",
        description="A model for generating images from text prompts",
        visibility="public",
        github_url=None,
        paper_url=None,
        license_url=None,
        run_count=0,
        cover_image_url=None,
        default_example=None,
        latest_version=None,
    )


class TestModelGetBackwardCompatibility:
    """Test backward compatibility for models.get() method."""

    @pytest.fixture
    def client(self):
        """Create a Replicate client with mocked token."""
        with patch("replicate.lib.cog._get_api_token_from_environment", return_value="test-token"):
            return Replicate()

    def test_legacy_format_owner_name(self, client, mock_model_response):
        """Test legacy format: models.get('owner/name')."""
        # Mock the original get method
        client.models._original_get = Mock(return_value=mock_model_response)

        # Call with legacy format
        result = client.models.get("stability-ai/stable-diffusion")

        # Verify original method was called with correct parameters
        client.models._original_get.assert_called_once_with(
            model_owner="stability-ai",
            model_name="stable-diffusion",
            extra_headers=None,
            extra_query=None,
            extra_body=None,
            timeout=NOT_GIVEN,
        )
        assert result == mock_model_response

    def test_new_format_keyword_args(self, client, mock_model_response):
        """Test new format: models.get(model_owner='owner', model_name='name')."""
        # Mock the original get method
        client.models._original_get = Mock(return_value=mock_model_response)

        # Call with new format
        result = client.models.get(model_owner="stability-ai", model_name="stable-diffusion")

        # Verify original method was called with correct parameters
        client.models._original_get.assert_called_once_with(
            model_owner="stability-ai",
            model_name="stable-diffusion",
            extra_headers=None,
            extra_query=None,
            extra_body=None,
            timeout=NOT_GIVEN,
        )
        assert result == mock_model_response

    def test_legacy_format_with_extra_params(self, client, mock_model_response):
        """Test legacy format with extra parameters."""
        # Mock the original get method
        client.models._original_get = Mock(return_value=mock_model_response)

        # Call with legacy format and extra parameters
        result = client.models.get("stability-ai/stable-diffusion", extra_headers={"X-Custom": "test"}, timeout=30.0)

        # Verify original method was called with correct parameters
        client.models._original_get.assert_called_once_with(
            model_owner="stability-ai",
            model_name="stable-diffusion",
            extra_headers={"X-Custom": "test"},
            extra_query=None,
            extra_body=None,
            timeout=30.0,
        )
        assert result == mock_model_response

    def test_error_mixed_formats(self, client):
        """Test error when mixing legacy and new formats."""
        with pytest.raises(ValueError) as exc_info:
            client.models.get("stability-ai/stable-diffusion", model_owner="other-owner")

        assert "Cannot specify both positional 'model_or_owner' and keyword arguments" in str(exc_info.value)

    def test_error_invalid_legacy_format(self, client):
        """Test error for invalid legacy format (no slash)."""
        with pytest.raises(ValueError) as exc_info:
            client.models.get("invalid-format")

        assert "Invalid model reference 'invalid-format'" in str(exc_info.value)
        assert "Expected format: 'owner/name'" in str(exc_info.value)

    def test_error_missing_parameters(self, client):
        """Test error when no parameters are provided."""
        with pytest.raises(ValueError) as exc_info:
            client.models.get()

        assert "model_owner and model_name are required" in str(exc_info.value)

    def test_legacy_format_with_complex_names(self, client, mock_model_response):
        """Test legacy format with complex owner/model names."""
        # Mock the original get method
        client.models._original_get = Mock(return_value=mock_model_response)

        # Test with hyphenated names and numbers
        result = client.models.get("black-forest-labs/flux-1.1-pro")

        # Verify parsing
        client.models._original_get.assert_called_once_with(
            model_owner="black-forest-labs",
            model_name="flux-1.1-pro",
            extra_headers=None,
            extra_query=None,
            extra_body=None,
            timeout=NOT_GIVEN,
        )

    def test_legacy_format_multiple_slashes_error(self, client):
        """Test error for legacy format with multiple slashes."""
        with pytest.raises(ValueError) as exc_info:
            client.models.get("owner/name/version")

        assert "Invalid model reference" in str(exc_info.value)


class TestAsyncModelGetBackwardCompatibility:
    """Test backward compatibility for async models.get() method."""

    @pytest.fixture
    async def async_client(self):
        """Create an async Replicate client with mocked token."""
        with patch("replicate.lib.cog._get_api_token_from_environment", return_value="test-token"):
            return AsyncReplicate()

    @pytest.mark.asyncio
    async def test_async_legacy_format_owner_name(self, async_client, mock_model_response):
        """Test async legacy format: models.get('owner/name')."""
        # Mock the original async get method
        async_client.models._original_get = AsyncMock(return_value=mock_model_response)

        # Call with legacy format
        result = await async_client.models.get("stability-ai/stable-diffusion")

        # Verify original method was called with correct parameters
        async_client.models._original_get.assert_called_once_with(
            model_owner="stability-ai",
            model_name="stable-diffusion",
            extra_headers=None,
            extra_query=None,
            extra_body=None,
            timeout=NOT_GIVEN,
        )
        assert result == mock_model_response

    @pytest.mark.asyncio
    async def test_async_new_format_keyword_args(self, async_client, mock_model_response):
        """Test async new format: models.get(model_owner='owner', model_name='name')."""
        # Mock the original async get method
        async_client.models._original_get = AsyncMock(return_value=mock_model_response)

        # Call with new format
        result = await async_client.models.get(model_owner="stability-ai", model_name="stable-diffusion")

        # Verify original method was called with correct parameters
        async_client.models._original_get.assert_called_once_with(
            model_owner="stability-ai",
            model_name="stable-diffusion",
            extra_headers=None,
            extra_query=None,
            extra_body=None,
            timeout=NOT_GIVEN,
        )
        assert result == mock_model_response

    @pytest.mark.asyncio
    async def test_async_error_mixed_formats(self, async_client):
        """Test async error when mixing legacy and new formats."""
        with pytest.raises(ValueError) as exc_info:
            await async_client.models.get("stability-ai/stable-diffusion", model_owner="other-owner")

        assert "Cannot specify both positional 'model_or_owner' and keyword arguments" in str(exc_info.value)


class TestModelVersionIdentifierIntegration:
    """Test integration with ModelVersionIdentifier parsing."""

    @pytest.fixture
    def client(self):
        """Create a Replicate client with mocked token."""
        with patch("replicate.lib.cog._get_api_token_from_environment", return_value="test-token"):
            return Replicate()

    def test_legacy_format_parsing_edge_cases(self, client, mock_model_response):
        """Test edge cases in legacy format parsing."""
        # Mock the original get method
        client.models._original_get = Mock(return_value=mock_model_response)

        # Test various valid formats
        test_cases = [
            ("owner/name", "owner", "name"),
            ("owner-with-hyphens/name-with-hyphens", "owner-with-hyphens", "name-with-hyphens"),
            ("owner123/name456", "owner123", "name456"),
            ("owner/name.with.dots", "owner", "name.with.dots"),
        ]

        for model_ref, expected_owner, expected_name in test_cases:
            client.models._original_get.reset_mock()
            client.models.get(model_ref)

            client.models._original_get.assert_called_once_with(
                model_owner=expected_owner,
                model_name=expected_name,
                extra_headers=None,
                extra_query=None,
                extra_body=None,
                timeout=NOT_GIVEN,
            )
