# Upgrading from v1 to v2

This guide will help you migrate an existing codebase from the v1 Replicate Python SDK to v2.

🍪 Feed this doc to your coding agent to assist with the upgrade process!

If you encounter any issues, please [share feedback on the GitHub Discussions page](https://github.com/replicate/replicate-python-beta/discussions/89).

## Docs

- v2 beta release notes: https://github.com/replicate/replicate-python-beta/releases/tag/v2.0.0-beta.1
- v2 beta SDK reference: https://sdks.replicate.com/python
- v2 beta GitHub discussion: https://github.com/replicate/replicate-python-beta/discussions/89
- HTTP API reference: https://replicate.com/docs/reference/http

## Installing the v2 SDK

Install the latest pre-release version of the v2 SDK from PyPI using pip:

```sh
pip install --pre replicate
```

## Pinning to the legacy v1 SDK

You are not required to upgrade to the new 2.x version. If you're already using the 1.x version and want to continue using it, pin the version number in your dependency files.

Here's an example `requirements.txt`:

```
replicate>=1.0.0,<2.0.0
```

Here's an example `pyproject.toml`:

```toml
[project]
dependencies = [
    "replicate>=1.0.0,<2.0.0",
]
```

## Quick migration checklist

- Update client initialization to use `Replicate()` instead of `Client()` and `bearer_token` instead of `api_token` - [details](#client-initialization-and-authentication)
- Replace prediction instance methods with client methods (e.g., `replicate.predictions.wait(id)` instead of `prediction.wait()`) - [details](#predictions)
- Update async code to use `AsyncReplicate` client or context-aware module-level functions - [details](#async-support)
- Add keyword arguments to all API calls - [details](#models-and-versions)
- Update exception handling to use new exception types - [details](#error-handling)

## Client initialization and authentication

In both the v1 and v2 SDKs, the simplest way to import and use the library is to import the `replicate` module and use the module-level functions like `replicate.run()`, without explicitly instantiating a client:

```python
import replicate

output = replicate.run(...)
```

☝️ This approach expects a `REPLICATE_API_TOKEN` variable to be present in the environment.

---

For cases where you need to instantiate a client (e.g., for custom configuration or async support), the client class name and parameter names have changed in v2:

### Before (v1)

```python
import os
import replicate
from replicate import Client

client = Client(api_token=os.environ["REPLICATE_API_TOKEN"])
```

### After (v2)

```python
import os
import replicate
from replicate import Replicate

client = Replicate(bearer_token=os.environ["REPLICATE_API_TOKEN"])
```

The `api_token` parameter is still accepted for backward compatibility, but `bearer_token` is preferred.

## Streaming output

Streaming works differently in v2. Prediction objects no longer have a `stream()` method and the `replicate.stream()` method is deprecated.

You should use `replicate.use()` with `streaming=True` for streaming output in the v2 SDK.

### Before (v1)

```python
# Top-level streaming
for event in replicate.stream(
    "anthropic/claude-4.5-sonnet",
    input={"prompt": "Write a haiku"}
):
    print(str(event), end="")

# Streaming from prediction object
prediction = replicate.predictions.create(..., stream=True)
for event in prediction.stream():
    print(str(event), end="")
```

### After (v2)

```python
# Use replicate.use() with streaming=True
model = replicate.use("anthropic/claude-4.5-sonnet", streaming=True)
for event in model(prompt="Write a haiku"):
    print(str(event), end="")

# Streaming from prediction object is not available
prediction = replicate.predictions.create(...)
# prediction.stream() is not available in v2
```

Note: `replicate.stream()` still works in v2 but is deprecated and will be removed in a future version.

## Predictions

Prediction objects in the v2 client no longer have instance methods like `wait()`, `cancel()`, and `reload()`. These have been removed in favor of client methods (e.g., use `replicate.predictions.wait(prediction.id)` instead of `prediction.wait()`).

### Creating predictions

#### Before (v1)

```python
# Create via model shorthand
prediction = replicate.predictions.create(
    model="owner/model",
    input={"prompt": "..."}
)
```

#### After (v2)

```python
# Create with keyword arguments model_owner and model_name
prediction = replicate.models.predictions.create(
    model_owner="owner",
    model_name="model",
    input={"prompt": "..."}
)
```

### Getting predictions

#### Before (v1)

```python
prediction = replicate.predictions.get("prediction_id")
```

#### After (v2)

```python
# Note: keyword argument required
prediction = replicate.predictions.get(prediction_id="prediction_id")
```

### Waiting for predictions

#### Before (v1)

```python
prediction = replicate.predictions.create(...)
prediction.wait()
```

#### After (v2)

```python
prediction = replicate.predictions.create(...)
# prediction.wait() is not available

# Use resource method instead
prediction = replicate.predictions.wait(prediction.id)
```

### Canceling predictions

#### Before (v1)

```python
prediction = replicate.predictions.get("prediction_id")
prediction.cancel()
```

#### After (v2)

```python
prediction = replicate.predictions.get(prediction_id="prediction_id")
# prediction.cancel() is not available

# Use resource method instead
prediction = replicate.predictions.cancel(prediction.id)
```

### Reloading predictions

#### Before (v1)

```python
prediction = replicate.predictions.get("prediction_id")
prediction.reload()
print(prediction.status)
```

#### After (v2)

```python
prediction = replicate.predictions.get(prediction_id="prediction_id")
# prediction.reload() is not available

# Fetch fresh data instead
prediction = replicate.predictions.get(prediction_id=prediction.id)
print(prediction.status)
```

## Async support

Async functionality has been redesigned. Instead of separate `async_*` methods, v2 uses a dedicated `AsyncReplicate` client.

### Before (v1)

```python
import replicate

# Async methods with async_ prefix
output = await replicate.async_run(...)

for event in replicate.async_stream(...):
    print(event)

prediction = await replicate.predictions.async_create(...)
prediction = await replicate.predictions.async_get("id")
await prediction.async_wait()
```

### After (v2)

```python
from replicate import AsyncReplicate

# Use AsyncReplicate client
client = AsyncReplicate()

# Same method names, no async_ prefix
output = await client.run(...)

async for event in client.stream(...):
    print(event)

prediction = await client.predictions.create(...)
prediction = await client.predictions.get(prediction_id="id")
prediction = await client.predictions.wait(prediction.id)

# Or use module-level functions (context-aware)
output = await replicate.run(...)
async for event in replicate.stream(...):
    print(event)
```

## Error handling

Error handling is more granular in v2, with specific exception types for each HTTP status code.

### Before (v1)

```python
from replicate.exceptions import ReplicateError, ModelError

try:
    output = replicate.run(...)
except ModelError as e:
    print(f"Model failed: {e.prediction.error}")
except ReplicateError as e:
    print(f"API error: {e}")
```

### After (v2)

```python
from replicate.exceptions import (
    ModelError,
    NotFoundError,
    AuthenticationError,
    RateLimitError,
    APIStatusError
)

try:
    output = replicate.run(...)
except ModelError as e:
    print(f"Model failed: {e.prediction.error}")
except NotFoundError as e:
    print(f"Not found: {e.message}")
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
except APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
```

Available exception types in v2:

- `APIError` - Base exception for all API errors
- `APIConnectionError` - Network connection errors
- `APITimeoutError` - Request timeout errors
- `APIStatusError` - Base for HTTP status errors
- `BadRequestError` - 400 errors
- `AuthenticationError` - 401 errors
- `PermissionDeniedError` - 403 errors
- `NotFoundError` - 404 errors
- `ConflictError` - 409 errors
- `UnprocessableEntityError` - 422 errors
- `RateLimitError` - 429 errors
- `InternalServerError` - 500+ errors
- `ModelError` - Model execution failures

## Pagination

Pagination is more streamlined in v2 with auto-pagination support.

### Before (v1)

```python
# Manual pagination
page = replicate.predictions.list()
for prediction in page.results:
    print(prediction.id)

if page.next:
    next_page = replicate.predictions.list(cursor=page.next)

# Auto-pagination
for page in replicate.paginate(replicate.predictions.list):
    for prediction in page.results:
        print(prediction.id)
```

### After (v2)

```python
# Auto-pagination: iterate through all pages automatically
for prediction in replicate.predictions.list():
    print(prediction.id)
    # Automatically fetches more pages as needed

# Manual pagination (if needed)
page = replicate.predictions.list()
if page.has_next_page():
    next_page = page.get_next_page()

# Access results from a single page
page = replicate.predictions.list()
for prediction in page.results:
    print(prediction.id)
```

## Models and versions

Model and version access uses keyword arguments throughout, instead of shorthand positional arguments.

The new keyword argument syntax in v2 is more verbose but clearer and more consistent with Replicate's HTTP API, and consistent across all SDKs in different programming languages.

### Before (v1)

```python
# Get model
model = replicate.models.get("owner/name")

# Get version from model
version = model.versions.get("version_id")

# List versions
versions = model.versions.list()
```

### After (v2)

```python
# Get model (keyword arguments required)
model = replicate.models.get(
    model_owner="owner",
    model_name="name"
)

# Get version (no shorthand via model object)
version = replicate.models.versions.get(
    model_owner="owner",
    model_name="name",
    version_id="version_id"
)

# List versions
versions = replicate.models.versions.list(
    model_owner="owner",
    model_name="name"
)
```

The `model.versions` shorthand is not available in v2.

## Trainings

Training objects do not have the `.wait()` and `.cancel()` instance methods in v2.

### Before (v1)

```python
training = replicate.trainings.create(
    version="version_id",
    input={"train_data": "https://..."},
    destination="owner/model"
)

# Wait and cancel
training.wait()
training.cancel()
```

### After (v2)

```python
training = replicate.trainings.create(
    model_owner="owner",
    model_name="model",
    version_id="version_id",
    input={"train_data": "https://..."},
    destination="owner/new-model"
)

# No instance methods available
# Use client methods instead

# Wait for training (no trainings.wait() available)
# Poll with get() instead
while True:
    training = replicate.trainings.get(training_id=training.id)
    if training.status in ["succeeded", "failed", "canceled"]:
        break
    time.sleep(1)

# Cancel training
training = replicate.trainings.cancel(training_id=training.id)
```

## File uploads

File upload handling has changed slightly.

### Before (v1)

```python
# Upload file
file = replicate.files.create(
    file=open("image.jpg", "rb"),
    filename="image.jpg"
)

# Access URL
url = file.urls["get"]
```

### After (v2)

```python
# Upload file (supports file handle, bytes, or PathLike)
with open("image.jpg", "rb") as f:
    file = replicate.files.create(
        content=f,  # Can pass file handle directly
        filename="image.jpg"
    )

# Or read into memory if needed
with open("image.jpg", "rb") as f:
    file = replicate.files.create(
        content=f.read(),
        filename="image.jpg"
    )

# Access URL (property instead of dict)
url = file.urls.get
```

File inputs to predictions work the same way in both versions.

## Collections

Collections API uses keyword arguments in v2.

### Before (v1)

```python
collection = replicate.collections.get("collection_slug")
models = collection.models
```

### After (v2)

```python
collection = replicate.collections.get(collection_slug="collection_slug")

# Models accessed via nested resource
models = replicate.collections.models.list(collection_slug="collection_slug")
```

## Webhooks

Webhook validation is compatible between v1 and v2.

### Before (v1)

```python
from replicate.webhook import Webhooks

secret = replicate.webhooks.default.secret()
Webhooks.validate(request, secret)
```

### After (v2)

```python
from replicate.resources.webhooks import Webhooks

secret = replicate.webhooks.default.secret()
Webhooks.validate(request, secret)
```

The validation logic is identical; only the import paths differ.

## Experimental use() interface

The experimental `use()` interface is available in both versions with similar functionality.

### Before (v1)

```python
flux = replicate.use("black-forest-labs/flux-schnell")
outputs = flux(prompt="astronaut on a horse")

# Async support
async_flux = replicate.use("black-forest-labs/flux-schnell")
outputs = await async_flux(prompt="astronaut on a horse")
```

### After (v2)

```python
# Same interface
flux = replicate.use("black-forest-labs/flux-schnell")
outputs = flux(prompt="astronaut on a horse")

# Async support (uses use_async parameter)
async_flux = replicate.use("black-forest-labs/flux-schnell", use_async=True)
outputs = await async_flux(prompt="astronaut on a horse")
```

## New features in v2

### Models listing

```python
# List all models (not available in v1)
for model in replicate.models.list():
    print(model.name)
```

### Better type safety

V2 includes comprehensive type hints generated from the OpenAPI spec, providing better IDE autocomplete and type checking.

```python
from replicate import Replicate
from replicate.types import Prediction

client: Replicate = Replicate()
prediction: Prediction = client.predictions.get(prediction_id="...")
```

### HTTP client customization

```python
from replicate import Replicate, DefaultHttpxClient
import httpx

client = Replicate(
    http_client=DefaultHttpxClient(
        proxy="http://proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0")
    ),
    timeout=30.0,
    max_retries=3
)
```

### Raw response access

```python
# Access raw HTTP responses
response = client.with_raw_response.predictions.get(prediction_id="...")
print(response.headers)
print(response.http_response.status_code)

prediction = response.parse()
```

The response object is an [`APIResponse`](https://github.com/replicate/replicate-python-beta/tree/main/src/replicate/_response.py) instance. See the [README](https://github.com/replicate/replicate-python-beta#accessing-raw-response-data-eg-headers) for full documentation.

### Streaming response wrapper

```python
# Stream response body
with client.with_streaming_response.predictions.get(
    prediction_id="..."
) as response:
    for chunk in response.iter_bytes():
        process(chunk)
```

## Removed features

The following features are not available in v2:

- Prediction instance methods: `wait()`, `cancel()`, `reload()`, `stream()`, `output_iterator()`
- Training instance methods: `cancel()`, `reload()`
- Model instance methods: `predict()`
- `model.versions` shorthand (use `replicate.models.versions` instead)
- Separate `async_*` methods (use `AsyncReplicate` client)
- Positional arguments (all methods that map to HTTP API operations like `models.get` and `collections.get` now require keyword arguments)

## Getting help

If you encounter issues during the migration process, share your feedback on the [GitHub Discussions page](https://github.com/replicate/replicate-python-beta/discussions/89).