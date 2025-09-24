"""
Tests for backward compatibility in models.get() method.
"""

from unittest.mock import Mock, patch

import pytest

from replicate import Replicate, AsyncReplicate
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
        return Replicate(bearer_token="test-token")

    def test_legacy_format_owner_name(self, client, mock_model_response):
        """Test legacy format: models.get('owner/name')."""
        # Mock the underlying _get method
        with patch.object(client.models, "_get", return_value=mock_model_response) as mock_get:
            # Call with legacy format
            result = client.models.get("stability-ai/stable-diffusion")

            # Verify underlying method was called with correct parameters
            mock_get.assert_called_once_with("/models/stability-ai/stable-diffusion", options=Mock())
            assert result == mock_model_response

    def test_new_format_keyword_args(self, client, mock_model_response):
        """Test new format: models.get(model_owner='owner', model_name='name')."""
        # Mock the underlying _get method
        with patch.object(client.models, "_get", return_value=mock_model_response) as mock_get:
            # Call with new format
            result = client.models.get(model_owner="stability-ai", model_name="stable-diffusion")

            # Verify underlying method was called with correct parameters
            mock_get.assert_called_once_with("/models/stability-ai/stable-diffusion", options=Mock())
            assert result == mock_model_response

    def test_legacy_format_with_extra_params(self, client, mock_model_response):
        """Test legacy format with extra parameters."""
        # Mock the underlying _get method
        with patch.object(client.models, "_get", return_value=mock_model_response) as mock_get:
            # Call with legacy format and extra parameters
            result = client.models.get(
                "stability-ai/stable-diffusion", extra_headers={"X-Custom": "test"}, timeout=30.0
            )

            # Verify underlying method was called
            mock_get.assert_called_once()
            assert result == mock_model_response

    def test_error_mixed_formats(self, client):
        """Test error when mixing legacy and new formats."""
        with pytest.raises(ValueError) as exc_info:
            client.models.get("stability-ai/stable-diffusion", model_owner="other-owner")

        assert "Cannot specify both positional and keyword arguments" in str(exc_info.value)

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
        # Mock the underlying _get method
        with patch.object(client.models, "_get", return_value=mock_model_response) as mock_get:
            # Test with hyphenated names and numbers
            result = client.models.get("black-forest-labs/flux-1.1-pro")

            # Verify parsing
            mock_get.assert_called_once_with("/models/black-forest-labs/flux-1.1-pro", options=Mock())

    def test_legacy_format_multiple_slashes(self, client):
        """Test legacy format with multiple slashes (should split on first slash only)."""
        # Mock the underlying _get method
        with patch.object(client.models, "_get", return_value=Mock()) as mock_get:
            # This should work - split on first slash only
            client.models.get("owner/name/with/slashes")

            # Verify it was parsed correctly
            mock_get.assert_called_once_with("/models/owner/name/with/slashes", options=Mock())


class TestAsyncModelGetBackwardCompatibility:
    """Test backward compatibility for async models.get() method."""

    @pytest.fixture
    async def async_client(self):
        """Create an async Replicate client with mocked token."""
        return AsyncReplicate(bearer_token="test-token")

    @pytest.mark.asyncio
    async def test_async_legacy_format_owner_name(self, async_client, mock_model_response):
        """Test async legacy format: models.get('owner/name')."""
        # Mock the underlying _get method
        with patch.object(async_client.models, "_get", return_value=mock_model_response) as mock_get:
            # Call with legacy format
            result = await async_client.models.get("stability-ai/stable-diffusion")

            # Verify underlying method was called with correct parameters
            mock_get.assert_called_once_with("/models/stability-ai/stable-diffusion", options=Mock())
            assert result == mock_model_response

    @pytest.mark.asyncio
    async def test_async_new_format_keyword_args(self, async_client, mock_model_response):
        """Test async new format: models.get(model_owner='owner', model_name='name')."""
        # Mock the underlying _get method
        with patch.object(async_client.models, "_get", return_value=mock_model_response) as mock_get:
            # Call with new format
            result = await async_client.models.get(model_owner="stability-ai", model_name="stable-diffusion")

            # Verify underlying method was called with correct parameters
            mock_get.assert_called_once_with("/models/stability-ai/stable-diffusion", options=Mock())
            assert result == mock_model_response

    @pytest.mark.asyncio
    async def test_async_error_mixed_formats(self, async_client):
        """Test async error when mixing legacy and new formats."""
        with pytest.raises(ValueError) as exc_info:
            await async_client.models.get("stability-ai/stable-diffusion", model_owner="other-owner")

        assert "Cannot specify both positional and keyword arguments" in str(exc_info.value)
