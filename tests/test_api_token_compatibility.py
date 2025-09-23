"""Tests for api_token legacy compatibility during client instantiation."""

from __future__ import annotations

import pytest

from replicate import Replicate, AsyncReplicate, ReplicateError
from replicate._client import Client


class TestApiTokenCompatibility:
    """Test that api_token parameter works as a legacy compatibility option."""

    def test_sync_client_with_api_token(self) -> None:
        """Test that Replicate accepts api_token parameter."""
        client = Replicate(api_token="test_token_123")
        assert client.bearer_token == "test_token_123"

    def test_async_client_with_api_token(self) -> None:
        """Test that AsyncReplicate accepts api_token parameter."""
        client = AsyncReplicate(api_token="test_token_123")
        assert client.bearer_token == "test_token_123"

    def test_sync_client_with_bearer_token(self) -> None:
        """Test that Replicate still accepts bearer_token parameter."""
        client = Replicate(bearer_token="test_token_123")
        assert client.bearer_token == "test_token_123"

    def test_async_client_with_bearer_token(self) -> None:
        """Test that AsyncReplicate still accepts bearer_token parameter."""
        client = AsyncReplicate(bearer_token="test_token_123")
        assert client.bearer_token == "test_token_123"

    def test_sync_client_both_tokens_error(self) -> None:
        """Test that providing both api_token and bearer_token raises an error."""
        with pytest.raises(ReplicateError, match="Cannot specify both 'bearer_token' and 'api_token'"):
            Replicate(api_token="test_api", bearer_token="test_bearer")

    def test_async_client_both_tokens_error(self) -> None:
        """Test that providing both api_token and bearer_token raises an error."""
        with pytest.raises(ReplicateError, match="Cannot specify both 'bearer_token' and 'api_token'"):
            AsyncReplicate(api_token="test_api", bearer_token="test_bearer")

    def test_sync_client_no_token_with_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that client reads from environment when no token is provided."""
        monkeypatch.setenv("REPLICATE_API_TOKEN", "env_token_123")
        client = Replicate()
        assert client.bearer_token == "env_token_123"

    def test_async_client_no_token_with_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that async client reads from environment when no token is provided."""
        monkeypatch.setenv("REPLICATE_API_TOKEN", "env_token_123")
        client = AsyncReplicate()
        assert client.bearer_token == "env_token_123"

    def test_sync_client_no_token_no_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that client raises error when no token is provided and env is not set."""
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        with pytest.raises(ReplicateError, match="The bearer_token client option must be set"):
            Replicate()

    def test_async_client_no_token_no_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that async client raises error when no token is provided and env is not set."""
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        with pytest.raises(ReplicateError, match="The bearer_token client option must be set"):
            AsyncReplicate()

    def test_legacy_client_alias(self) -> None:
        """Test that legacy Client import still works as an alias."""
        assert Client is Replicate

    def test_legacy_client_with_api_token(self) -> None:
        """Test that legacy Client alias works with api_token parameter."""
        client = Client(api_token="test_token_123")
        assert client.bearer_token == "test_token_123"
        assert isinstance(client, Replicate)

    def test_api_token_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that explicit api_token overrides environment variable."""
        monkeypatch.setenv("REPLICATE_API_TOKEN", "env_token")
        client = Replicate(api_token="explicit_token")
        assert client.bearer_token == "explicit_token"

    def test_bearer_token_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that explicit bearer_token overrides environment variable."""
        monkeypatch.setenv("REPLICATE_API_TOKEN", "env_token")
        client = Replicate(bearer_token="explicit_token")
        assert client.bearer_token == "explicit_token"
