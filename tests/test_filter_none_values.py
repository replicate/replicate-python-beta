from replicate import Replicate
from replicate.lib._files import encode_json, async_encode_json, filter_none_values


def test_filter_none_values_simple_dict():
    """Test that None values are filtered from a simple dictionary."""
    input_dict = {"prompt": "banana", "seed": None, "width": 512}
    result = filter_none_values(input_dict)
    assert result == {"prompt": "banana", "width": 512}
    assert "seed" not in result


def test_filter_none_values_nested_dict():
    """Test that None values are filtered from nested dictionaries."""
    input_dict = {
        "prompt": "banana",
        "config": {"seed": None, "temperature": 0.8, "iterations": None},
        "width": 512,
    }
    result = filter_none_values(input_dict)
    assert result == {
        "prompt": "banana",
        "config": {"temperature": 0.8},
        "width": 512,
    }
    assert "seed" not in result["config"]
    assert "iterations" not in result["config"]


def test_filter_none_values_all_none():
    """Test that a dict with all None values returns an empty dict."""
    input_dict = {"seed": None, "temperature": None}
    result = filter_none_values(input_dict)
    assert result == {}


def test_filter_none_values_empty_dict():
    """Test that an empty dict returns an empty dict."""
    input_dict = {}
    result = filter_none_values(input_dict)
    assert result == {}


def test_filter_none_values_with_list():
    """Test that lists are preserved and None values in dicts within lists are filtered."""
    input_dict = {
        "prompts": ["banana", "apple"],
        "seeds": [None, 42, None],
        "config": {"value": None},
    }
    result = filter_none_values(input_dict)
    # None values in lists are preserved
    assert result == {
        "prompts": ["banana", "apple"],
        "seeds": [None, 42, None],
        "config": {},
    }


def test_filter_none_values_with_tuple():
    """Test that tuples are preserved."""
    input_dict = {"coords": (1, None, 3)}
    result = filter_none_values(input_dict)
    # Tuples are preserved as-is
    assert result == {"coords": (1, None, 3)}


def test_filter_none_values_non_dict():
    """Test that non-dict values are returned as-is."""
    assert filter_none_values("string") == "string"
    assert filter_none_values(42) == 42
    assert filter_none_values(None) is None
    assert filter_none_values([1, 2, 3]) == [1, 2, 3]


def test_encode_json_filters_none(client: Replicate):
    """Test that encode_json filters None values from dicts."""
    input_dict = {"prompt": "banana", "seed": None, "width": 512}
    result = encode_json(input_dict, client)
    assert result == {"prompt": "banana", "width": 512}
    assert "seed" not in result


def test_encode_json_nested_none_filtering(client: Replicate):
    """Test that encode_json recursively filters None values."""
    input_dict = {
        "prompt": "banana",
        "config": {"seed": None, "temperature": 0.8},
        "metadata": {"user": "test", "session": None},
    }
    result = encode_json(input_dict, client)
    assert result == {
        "prompt": "banana",
        "config": {"temperature": 0.8},
        "metadata": {"user": "test"},
    }


async def test_async_encode_json_filters_none(async_client):
    """Test that async_encode_json filters None values from dicts."""
    input_dict = {"prompt": "banana", "seed": None, "width": 512}
    result = await async_encode_json(input_dict, async_client)
    assert result == {"prompt": "banana", "width": 512}
    assert "seed" not in result


async def test_async_encode_json_nested_none_filtering(async_client):
    """Test that async_encode_json recursively filters None values."""
    input_dict = {
        "prompt": "banana",
        "config": {"seed": None, "temperature": 0.8},
        "metadata": {"user": "test", "session": None},
    }
    result = await async_encode_json(input_dict, async_client)
    assert result == {
        "prompt": "banana",
        "config": {"temperature": 0.8},
        "metadata": {"user": "test"},
    }


def test_encode_json_preserves_false_and_zero(client: Replicate):
    """Test that False and 0 are not filtered out."""
    input_dict = {
        "prompt": "banana",
        "seed": 0,
        "enable_feature": False,
        "iterations": None,
    }
    result = encode_json(input_dict, client)
    assert result == {
        "prompt": "banana",
        "seed": 0,
        "enable_feature": False,
    }
    assert "iterations" not in result
