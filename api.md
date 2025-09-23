# Replicate Python SDK API Reference

## Installation

```bash
pip install replicate
```

## Quick Start

```python
import replicate

# Create a model function for image generation
banana = replicate.use("google/nano-banana")

# Call it - returns an image URL
image_url = banana(prompt="astronaut on a horse")
print(image_url)  # https://replicate.delivery/...

# Or for text generation
claude = replicate.use("anthropic/claude-4-sonnet")
text = claude(prompt="Write a haiku about Python")
print(text)  # "Code flows like water..."
```

## Client Initialization

By default, the SDK uses the `REPLICATE_API_TOKEN` environment variable:

```python
import replicate

# Uses REPLICATE_API_TOKEN from environment
image_url = replicate.run("google/nano-banana", input={"prompt": "hello"})
```

### Custom Client Configuration

For advanced use cases, you can create an explicit client instance:

```python
from replicate import Replicate
import os

# Explicitly specify which environment variable to use
replicate = Replicate(
    bearer_token=os.environ.get("MY_REPLICATE_TOKEN"),
    base_url="https://api.replicate.com/v1",  # Optional custom base URL
    timeout=120.0,  # Request timeout in seconds
    max_retries=5  # Maximum number of retries
)

# Now use this configured client
image_url = replicate.run("google/nano-banana", input={"prompt": "hello"})
```

### Asynchronous Client

```python
from replicate import AsyncReplicate
import asyncio
import os

async def main():
    # Can specify token explicitly if needed
    replicate = AsyncReplicate(bearer_token=os.environ.get("MY_REPLICATE_TOKEN"))
    image_url = await replicate.run(
        "google/nano-banana",
        input={"prompt": "a watercolor painting"}
    )
    print(image_url)  # https://replicate.delivery/...

asyncio.run(main())
```

## High-Level Methods

### use() - Create a Reusable Model Function (Recommended)

The most Pythonic way to interact with models. Creates a callable function for any model.

```python
# Image generation - returns file URLs
banana = replicate.use("google/nano-banana")

# Simple call with just prompt (only required input)
image_url = banana(prompt="a 19th century portrait of a wombat gentleman")
print(image_url)  # Returns: https://replicate.delivery/...

# Use it multiple times
image1 = banana(prompt="a cat in a hat")
image2 = banana(prompt="a dog in sunglasses")

# Text generation - returns text string
claude = replicate.use("anthropic/claude-4-sonnet")

# Simple call with just prompt (only required input)
text = claude(prompt="Write a haiku about Python programming")
print(text)  # Returns: "Code flows like water..."

# Enable streaming for text models
claude_stream = replicate.use("anthropic/claude-4-sonnet", streaming=True)
for chunk in claude_stream(prompt="Explain quantum computing"):
    print(chunk, end="")  # Streams text chunks

# Can accept model references in various formats
model = replicate.use("owner/name:version")  # Specific version
model = replicate.use("owner/name")  # Latest version
model = replicate.use("5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa")  # Version ID
```

### run() - Run a Model Once

Direct method to run a model and get output. Good for one-off predictions.

```python
# Image generation - returns a file URL
image_url = replicate.run(
    "google/nano-banana",
    input={"prompt": "a 19th century portrait of a wombat gentleman"}
)
print(image_url)  # https://replicate.delivery/...

# Text generation - returns text string
text = replicate.run(
    "anthropic/claude-4-sonnet",
    input={"prompt": "Write a poem about machine learning"}
)
print(text)  # "In silicon valleys deep and wide..."

# Model reference formats
replicate.run("owner/name:version", input={})  # Specific version
replicate.run("owner/name", input={})  # Latest version
replicate.run("5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa", input={})  # Version ID
```

### stream() - Stream Model Output

For models that support streaming (like language models). Returns an iterator of output chunks.

```python
# Stream text output (only for text models like Claude)
for chunk in replicate.stream(
    "anthropic/claude-4-sonnet",
    input={"prompt": "Tell me a story about a robot"}
):
    print(chunk, end="")  # Prints each text chunk as it arrives

# Async streaming
async for chunk in async_replicate.stream(
    "anthropic/claude-4-sonnet", 
    input={"prompt": "Hello"}
):
    print(chunk, end="")
```

### search() - Search Models

Find models by keyword or description.

```python
# Search for models
results = replicate.search(query="image generation", limit=10)

for model in results:
    print(f"{model.owner}/{model.name}: {model.description}")
```

## Core Resources

### Predictions

Create and manage model predictions.

```python
from replicate.types import Prediction

# Create a prediction
prediction = replicate.predictions.create(
    model="owner/model:version",
    input={"prompt": "hello world"},
    webhook="https://example.com/webhook",  # Optional webhook URL
    webhook_events_filter=["start", "completed"]  # Optional webhook events
)

# Get prediction status
prediction = replicate.predictions.get(prediction_id="abc123")
print(f"Status: {prediction.status}")
print(f"Output: {prediction.output}")

# Cancel a prediction
cancelled = replicate.predictions.cancel(prediction_id="abc123")

# List predictions
for prediction in replicate.predictions.list():
    print(f"{prediction.id}: {prediction.status}")

# Wait for a prediction to complete
completed = replicate.predictions.wait(
    prediction_id="abc123",
    timeout=60  # Optional timeout in seconds
)
```

### Models

Interact with models and their versions.

```python
# Get a specific model
model = replicate.models.get(model_owner="google", model_name="nano-banana")
print(f"Model: {model.owner}/{model.name}")
print(f"Description: {model.description}")
print(f"Latest version: {model.latest_version.id}")

# List all models (with pagination)
for model in replicate.models.list():
    print(f"{model.owner}/{model.name}")

# Search models
for model in replicate.models.search(query="text generation"):
    print(f"{model.owner}/{model.name}: {model.description}")

# Create a new model
model = replicate.models.create(
    owner="your-username",
    name="my-model",
    visibility="public",  # or "private"
    hardware="gpu-t4",  # Specify hardware requirements
    description="My custom model",
    github_url="https://github.com/user/repo"
)

# Delete a model
replicate.models.delete(model_owner="your-username", model_name="my-model")
```

#### Model Versions

```python
# List model versions
for version in replicate.models.versions.list(
    model_owner="google",
    model_name="nano-banana"
):
    print(f"Version {version.id}: created at {version.created_at}")

# Get a specific version
version = replicate.models.versions.get(
    model_owner="google",
    model_name="nano-banana",
    version_id="db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"
)

# Delete a version
replicate.models.versions.delete(
    model_owner="your-username",
    model_name="my-model",
    version_id="version-id"
)
```

#### Model Predictions

Run predictions directly through a model.

```python
# Create a prediction for a specific model
prediction = replicate.models.predictions.create(
    model_owner="google",
    model_name="nano-banana",
    input={"prompt": "a beautiful landscape"}
)
# prediction.output will be an image URL when complete
```

#### Model Examples

```python
# Get example predictions for a model
for example in replicate.models.examples.list(
    model_owner="google",
    model_name="nano-banana"
):
    print(f"Example input: {example.input}")
    print(f"Example output: {example.output}")
```

### Deployments

Manage model deployments for production use.

```python
# Create a deployment
deployment = replicate.deployments.create(
    name="my-deployment",
    model="owner/model:version",
    hardware="gpu-a100-large",
    min_instances=1,
    max_instances=10
)

# List deployments
for deployment in replicate.deployments.list():
    print(f"{deployment.owner}/{deployment.name}")

# Get deployment details
deployment = replicate.deployments.get(
    deployment_owner="your-username",
    deployment_name="my-deployment"
)

# Update deployment
updated = replicate.deployments.update(
    deployment_owner="your-username",
    deployment_name="my-deployment",
    min_instances=2,
    max_instances=20
)

# Delete deployment
replicate.deployments.delete(
    deployment_owner="your-username",
    deployment_name="my-deployment"
)

# Run a prediction on a deployment
prediction = replicate.deployments.predictions.create(
    deployment_owner="your-username",
    deployment_name="my-deployment",
    input={"prompt": "hello world"}
)
```

### Trainings

Create and manage model training jobs.

```python
# Start a training job
training = replicate.trainings.create(
    model_owner="your-username",
    model_name="my-model",
    version_id="base-version-id",
    input={
        "train_data": "https://example.com/training-data.zip",
        "epochs": 100,
        "batch_size": 32
    },
    webhook="https://example.com/training-webhook"
)

# Get training status
training = replicate.trainings.get(training_id="training-abc123")
print(f"Status: {training.status}")

# List trainings
for training in replicate.trainings.list():
    print(f"{training.id}: {training.status}")

# Cancel a training
cancelled = replicate.trainings.cancel(training_id="training-abc123")
```

### Collections

Browse curated model collections.

```python
# List collections
for collection in replicate.collections.list():
    print(f"{collection.name}: {collection.description}")

# Get a specific collection
collection = replicate.collections.get(collection_slug="awesome-banana-models")
for model in collection.models:
    print(f"- {model.owner}/{model.name}")
```

### Files

Upload and manage files for model inputs.

```python
# Create/upload a file
with open("image.jpg", "rb") as f:
    file_response = replicate.files.create(file=f)
    file_url = file_response.urls.get

# List files
for file in replicate.files.list():
    print(f"{file.id}: {file.name}")

# Get file details
file = replicate.files.get(file_id="file-abc123")
print(f"File URL: {file.urls.get}")

# Delete a file
replicate.files.delete(file_id="file-abc123")
```

### Hardware

Get information about available hardware.

```python
# List available hardware SKUs
hardware_list = replicate.hardware.list()
for sku in hardware_list:
    print(f"{sku.name}: {sku.specs}")
```

### Account

Manage account information.

```python
# Get account details
account = replicate.account.get()
print(f"Username: {account.username}")
print(f"Email: {account.email}")
```

### Webhooks

Configure webhooks for predictions.

```python
# Get the default webhook secret
webhook_secret = replicate.webhooks.default.secret.get()
print(f"Webhook signing secret: {webhook_secret.key}")
```

## File Handling

### Input Files

The SDK supports multiple ways to provide file inputs:

```python
# For models that accept image inputs (like Claude with vision)
with open("input.jpg", "rb") as f:
    text = replicate.run("anthropic/claude-4-sonnet", input={
        "prompt": "What's in this image?",
        "image": f
    })

# File path (automatically opened)
text = replicate.run("anthropic/claude-4-sonnet", input={
    "prompt": "Describe this",
    "image": "path/to/image.jpg"
})

# URL
text = replicate.run("anthropic/claude-4-sonnet", input={
    "prompt": "Analyze this image",
    "image": "https://example.com/image.jpg"
})
```

### Output Files

File outputs are automatically converted to `FileOutput` objects:

```python
from replicate.helpers import FileOutput

# Image generation returns a file URL
image_url = replicate.run("google/nano-banana", input={"prompt": "sunset over mountains"})
print(f"Generated image: {image_url}")

# Text generation returns a string
text = replicate.run("anthropic/claude-4-sonnet", input={"prompt": "Tell me a joke"})
print(f"Response: {text}")

# When using FileOutput wrapper
from replicate.helpers import FileOutput
if isinstance(image_url, FileOutput):
    # Get the URL
    print(f"File URL: {image_url.url}")
    
    # Save to disk
    with open("output.jpg", "wb") as f:
        for chunk in image_url:
            f.write(chunk)
```

## Error Handling

The SDK provides detailed exception types for error handling:

```python
from replicate.exceptions import (
    ReplicateError,
    ModelError,
    RateLimitError,
    AuthenticationError,
    NotFoundError
)

try:
    image_url = replicate.run("google/nano-banana", input={"prompt": "test"})
except ModelError as e:
    # Model execution failed
    print(f"Model error: {e}")
    print(f"Prediction ID: {e.prediction.id}")
    print(f"Prediction status: {e.prediction.status}")
except RateLimitError as e:
    # Rate limited
    print("Rate limit exceeded, retry after:", e.response.headers.get("retry-after"))
except AuthenticationError:
    # Invalid API token
    print("Invalid API token")
except NotFoundError:
    # Model not found
    print("Model not found")
except ReplicateError as e:
    # Other Replicate API errors
    print(f"API error: {e}")
```

## Pagination

The SDK automatically handles pagination for list operations:

```python
# Automatic pagination (iterates through all pages)
for model in replicate.models.list():
    print(model.name)

# Manual pagination
first_page = replicate.models.list()
print(f"Items in first page: {len(first_page.items)}")

if first_page.has_next_page():
    next_page = first_page.get_next_page()
    print(f"Items in second page: {len(next_page.items)}")

# Get all items at once
all_models = list(replicate.models.list())
```

## Advanced Features

### Raw Response Access

Access the underlying HTTP response:

```python
# Get raw response
response = replicate.predictions.with_raw_response.create(
    model="model:version",
    input={"prompt": "test"}
)

# Access response data
print(f"Status code: {response.status_code}")
print(f"Headers: {response.headers}")

# Parse the response
prediction = response.parse()
```

### Custom HTTP Client

Configure a custom HTTP client for Replicate:

```python
import httpx
from replicate import DefaultHttpxClient

# With proxy
replicate = Replicate(
    http_client=DefaultHttpxClient(
        proxy="http://proxy.example.com:8080"
    )
)

# With custom timeout
replicate = Replicate(
    http_client=DefaultHttpxClient(
        timeout=httpx.Timeout(60.0)
    )
)
```

### Retries and Timeouts

Configure retry behavior and timeouts:

```python
replicate = Replicate(
    max_retries=5,  # Maximum number of retries
    timeout=120.0  # Request timeout in seconds
)

# Per-request timeout
image_url = replicate.run(
    "google/nano-banana",
    input={"prompt": "test"},
    wait=60  # Wait up to 60 seconds for completion
)
```

### Client Copying

Create a new Replicate instance with modified settings:

```python
# Create a copy with different settings
new_replicate = replicate.copy(
    bearer_token="different_token",
    timeout=60.0,
    max_retries=3
)
```

## Async/Await Support

All methods have async equivalents when using `AsyncReplicate`:

```python
import asyncio
from replicate import AsyncReplicate

async def main():
    replicate = AsyncReplicate()
    
    # Image generation
    image_url = await replicate.run(
        "google/nano-banana",
        input={"prompt": "a futuristic city"}
    )
    print(f"Image: {image_url}")
    
    # Stream text generation
    async for chunk in replicate.stream(
        "anthropic/claude-4-sonnet",
        input={"prompt": "Tell me a joke"}
    ):
        print(chunk, end="")
    
    # Pagination
    async for model in replicate.models.list():
        print(model.name)
    
    # Concurrent requests
    tasks = [
        replicate.run("google/nano-banana", input={"prompt": "cat"}),
        replicate.run("google/nano-banana", input={"prompt": "dog"}),
        replicate.run("anthropic/claude-4-sonnet", input={"prompt": "Hello"})
    ]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

## Environment Variables

The SDK respects these environment variables:

- `REPLICATE_API_TOKEN` - API authentication token
- `REPLICATE_BASE_URL` - Override the API base URL (default: `https://api.replicate.com/v1`)

## Type Hints

The SDK is fully typed with comprehensive type hints:

```python
import replicate
from replicate.types import Prediction, PredictionStatus
from replicate.pagination import SyncCursorURLPage

# Type hints for responses
prediction: Prediction = replicate.predictions.get(prediction_id="abc123")
status: PredictionStatus = prediction.status

# Type hints for pagination
page: SyncCursorURLPage[Prediction] = replicate.predictions.list()
```

## Common Patterns

### Wait for Completion with Polling

```python
import time

def wait_for_prediction(replicate, prediction_id, timeout=300):
    """Poll a prediction until it completes or times out."""
    start = time.time()
    while time.time() - start < timeout:
        prediction = replicate.predictions.get(prediction_id)
        if prediction.status in ["succeeded", "failed", "canceled"]:
            return prediction
        time.sleep(2)  # Poll every 2 seconds
    raise TimeoutError(f"Prediction {prediction_id} timed out")

# Usage
prediction = replicate.predictions.create(model="model:version", input={})
result = wait_for_prediction(replicate, prediction.id)
```

### Batch Processing

```python
import asyncio
from replicate import AsyncReplicate

async def batch_process(prompts):
    """Process multiple prompts in parallel."""
    from replicate import AsyncReplicate
    replicate = AsyncReplicate()
    tasks = [
        replicate.run("model:version", input={"prompt": prompt})
        for prompt in prompts
    ]
    return await asyncio.gather(*tasks)

# Usage
prompts = ["prompt 1", "prompt 2", "prompt 3"]
results = asyncio.run(batch_process(prompts))
```

### Webhook Handling

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

def verify_webhook(payload, signature, secret):
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Get webhook secret
    secret = "your_webhook_secret"  # From replicate.webhooks.default.secret.get()
    
    # Verify signature
    signature = request.headers.get("X-Replicate-Signature")
    if not verify_webhook(request.data, signature, secret):
        return "Unauthorized", 401
    
    # Process prediction
    data = request.json
    print(f"Prediction {data['id']} status: {data['status']}")
    
    if data["status"] == "succeeded":
        print(f"Output: {data['output']}")
    
    return "OK", 200
```

## Migration Guide

### From v0.x to v1.0+

The new SDK uses a different API structure. Here's how to migrate:

**Old (v0.x):**
```python
import replicate

# Run a model - image generation returns URL
image_url = replicate.run(
    "google/nano-banana",
    input={"prompt": "a cat"}
)

# Get a model
model = replicate.models.get("google/nano-banana")
```

**New (v1.0+):**
```python
import replicate

# Run a model - image generation returns URL
image_url = replicate.run(
    "google/nano-banana",
    input={"prompt": "a cat"}
)

# Get a model
model = replicate.models.get(
    model_owner="google",
    model_name="nano-banana"
)
```

### Using Legacy Authentication

For compatibility with older code:

```python
from replicate import Replicate

# Old style (still supported)
replicate = Replicate(api_token="your_token")

# New style (recommended)
replicate = Replicate(bearer_token="your_token")
```

## Support

- **Documentation**: https://replicate.com/docs
- **GitHub**: https://github.com/replicate/replicate-python
- **Discord**: https://discord.gg/replicate
- **API Reference**: https://replicate.com/docs/api

## License

Apache License 2.0