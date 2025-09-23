"""Tests for legacy v1.x type compatibility."""

from __future__ import annotations

from typing import TYPE_CHECKING

from replicate.types import Prediction, ModelGetResponse
from replicate.types.models.version_get_response import VersionGetResponse


def test_legacy_model_imports():
    """Test that legacy import paths work."""
    # Test importing Model from legacy path
    from replicate.model import Model
    from replicate.lib._models import Model as LibModel

    # Verify they are the same class
    assert Model is LibModel


def test_legacy_version_imports():
    """Test that legacy Version import paths work."""
    # Test importing Version from legacy path
    from replicate.model import Version
    from replicate.lib._models import Version as LibVersion

    # Verify they are the same class
    assert Version is LibVersion


def test_legacy_prediction_imports():
    """Test that legacy Prediction import paths work."""
    # Test importing Prediction from legacy path
    from replicate.model import Prediction as LegacyPrediction
    from replicate.types import Prediction as TypesPrediction

    # Verify they are the same class
    assert LegacyPrediction is TypesPrediction


def test_legacy_response_type_imports():
    """Test that legacy response type aliases work."""
    # Test importing response types from legacy path
    from replicate.model import ModelResponse, VersionResponse

    # Verify they are the correct types
    assert ModelResponse is ModelGetResponse
    assert VersionResponse is VersionGetResponse


def test_legacy_isinstance_checks_with_model():
    """Test that isinstance checks work with legacy Model type."""
    from replicate.model import Model

    # Create an instance
    model = Model(owner="test", name="model")

    # Test isinstance check
    assert isinstance(model, Model)


def test_legacy_isinstance_checks_with_version():
    """Test that isinstance checks work with legacy Version type."""
    import datetime

    from replicate.model import Version

    # Create a Version instance
    version = Version(id="test-version-id", created_at=datetime.datetime.now(), cog_version="0.8.0", openapi_schema={})

    # Test isinstance check
    assert isinstance(version, Version)


def test_legacy_isinstance_checks_with_prediction():
    """Test that isinstance checks work with legacy Prediction type."""
    import datetime

    from replicate.model import Prediction

    # Create a Prediction instance using construct to bypass validation
    prediction = Prediction.construct(
        id="test-prediction-id",
        created_at=datetime.datetime.now(),
        data_removed=False,
        input={},
        model="test/model",
        output=None,
        status="succeeded",
        urls={
            "cancel": "https://example.com/cancel",
            "get": "https://example.com/get",
            "web": "https://example.com/web",
        },
        version="test-version",
    )

    # Test isinstance check
    assert isinstance(prediction, Prediction)


def test_legacy_isinstance_checks_with_model_response():
    """Test that isinstance checks work with ModelResponse alias."""
    from replicate.model import ModelResponse

    # Create a ModelGetResponse instance
    model = ModelGetResponse.construct(name="test-model", owner="test-owner")

    # Test isinstance check with both the alias and the actual type
    assert isinstance(model, ModelResponse)
    assert isinstance(model, ModelGetResponse)


def test_legacy_isinstance_checks_with_version_response():
    """Test that isinstance checks work with VersionResponse alias."""
    import datetime

    from replicate.model import VersionResponse

    # Create a VersionGetResponse instance
    version = VersionGetResponse.construct(
        id="test-version-id", created_at=datetime.datetime.now(), cog_version="0.8.0", openapi_schema={}
    )

    # Test isinstance check with both the alias and the actual type
    assert isinstance(version, VersionResponse)
    assert isinstance(version, VersionGetResponse)


def test_all_exports():
    """Test that __all__ exports the expected items."""
    from replicate import model

    expected_exports = {
        "Model",
        "Version",
        "Prediction",
        "ModelResponse",
        "VersionResponse",
    }

    assert set(model.__all__) == expected_exports

    # Verify all exported items are importable
    for name in model.__all__:
        assert hasattr(model, name)


if TYPE_CHECKING:
    # Type checking test - ensure type annotations work correctly
    def type_annotation_test():
        from replicate.model import Model, Version, ModelResponse, VersionResponse

        model: Model = Model("owner", "name")  # pyright: ignore[reportUnusedVariable]
        version: Version  # pyright: ignore[reportUnusedVariable]
        prediction: Prediction  # pyright: ignore[reportUnusedVariable]
        model_response: ModelResponse  # pyright: ignore[reportUnusedVariable]
        version_response: VersionResponse  # pyright: ignore[reportUnusedVariable]

