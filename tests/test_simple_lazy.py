"""Simple test showing the lazy client fix works."""

import os
from unittest.mock import MagicMock, patch
import sys


def test_use_does_not_create_client_immediately():
    """Test that replicate.use() does not create a client until the model is called."""
    sys.path.insert(0, 'src')
    
    # Clear any existing token to simulate the original error condition
    with patch.dict(os.environ, {}, clear=True):
        with patch.dict(sys.modules, {"cog": None}):
            try:
                import replicate
                # This should work now - no client is created yet
                model = replicate.use("test/model")
                
                # Verify we got a Function object back
                from replicate.lib._predictions_use import Function
                assert isinstance(model, Function)
                print("✓ replicate.use() works without immediate client creation")
                
                # Verify the client is stored as a callable (factory function)
                assert callable(model._client)
                print("✓ Client is stored as factory function")
                
            except Exception as e:
                print(f"✗ Test failed: {e}")
                raise


def test_client_created_when_model_called():
    """Test that the client is created when the model is called."""
    sys.path.insert(0, 'src')
    
    # Mock the client creation to track when it happens
    created_clients = []
    
    def track_client_creation(*args, **kwargs):
        client = MagicMock()
        client.bearer_token = kwargs.get('bearer_token', 'no-token')
        created_clients.append(client)
        return client
    
    # Mock cog to provide a token
    mock_scope = MagicMock()
    mock_scope.context.items.return_value = [("REPLICATE_API_TOKEN", "cog-token")]
    mock_cog = MagicMock()
    mock_cog.current_scope.return_value = mock_scope
    
    with patch.dict(os.environ, {}, clear=True):
        with patch.dict(sys.modules, {"cog": mock_cog}):
            with patch('replicate._module_client._ModuleClient', side_effect=track_client_creation):
                import replicate
                
                # Create model function - should not create client yet
                model = replicate.use("test/model")
                assert len(created_clients) == 0
                print("✓ No client created when use() is called")
                
                # Try to call the model - this should create a client
                try:
                    model(prompt="test")
                except Exception:
                    # Expected to fail due to mocking, but client should be created
                    pass
                
                # Verify client was created with the cog token
                assert len(created_clients) == 1
                assert created_clients[0].bearer_token == "cog-token"
                print("✓ Client created with correct token when model is called")


if __name__ == "__main__":
    test_use_does_not_create_client_immediately()
    test_client_created_when_model_called()
    print("\n✓ All tests passed! The lazy client fix works correctly.")