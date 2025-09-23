# Replicate Python SDK API Reference

## Installation

```bash
pip install replicate
```

## Quick Start

```python
import replicate

# Initialize the client (uses REPLICATE_API_TOKEN env var by default)
client = replicate.Replicate()

# Run a model
output = client.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "astronaut on a horse"}
)
print(output)
```

## Client Initialization

### Synchronous Client

```python
from replicate import Replicate

# Using environment variable (REPLICATE_API_TOKEN)
client = Replicate()

# With explicit token
client = Replicate(bearer_token="your_api_token")

# Legacy token parameter (for compatibility)
client = Replicate(api_token="your_api_token")

# With custom configuration
client = Replicate(
    bearer_token="your_api_token",
    base_url="https://api.replicate.com/v1",  # Optional custom base URL
    timeout=120.0,  # Request timeout in seconds
    max_retries=5  # Maximum number of retries
)
```

### Asynchronous Client

```python
from replicate import AsyncReplicate
import asyncio

async def main():
    client = AsyncReplicate(bearer_token="your_api_token")
    output = await client.run(
        "stability-ai/stable-diffusion",
        input={"prompt": "a watercolor painting"}
    )
    print(output)

asyncio.run(main())
```

## High-Level Methods

### run() - Run a Model

The simplest way to run a model and get output.

```python
# Basic usage - returns output when complete
output = client.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={"prompt": "a 19th century portrait of a wombat gentleman"}
)

# With options
output = client.run(
    "meta/llama-2-70b-chat",
    input={
        "prompt": "Write a poem about machine learning",
        "max_new_tokens": 500,
        "temperature": 0.7
    },
    wait=30,  # Wait up to 30 seconds for completion (or True for unlimited)
    use_file_output=True,  # Return files as FileOutput objects
    file_encoding_strategy="base64"  # Encode input files as base64 (or "url")
)

# Model reference formats
client.run("owner/name:version", input={})  # Specific version
client.run("owner/name", input={})  # Latest version
client.run("5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa", input={})  # Version ID
```

### stream() - Stream Model Output

For models that support streaming (like language models).

```python
# Stream text output
for event in client.stream(
    "meta/llama-2-70b-chat",
    input={
        "prompt": "Tell me a story about a robot",
        "max_new_tokens": 1000
    }
):
    print(str(event), end="")

# Async streaming
async for event in async_client.stream("meta/llama-2-70b-chat", input={"prompt": "Hello"}):
    print(str(event), end="")
```

### use() - Create a Reusable Model Function

Experimental feature for creating reusable model functions.

```python
# Create a model function
stable_diffusion = client.use("stability-ai/stable-diffusion")

# Use it multiple times
image1 = stable_diffusion(prompt="a cat in a hat")
image2 = stable_diffusion(prompt="a dog in sunglasses")

# With streaming models
llama = client.use("meta/llama-2-70b-chat", streaming=True)
for chunk in llama(prompt="Explain quantum computing"):
    print(chunk, end="")
```

### search() - Search Models

```python
# Search for models
results = client.search(query="image generation", limit=10)

for model in results:
    print(f"{model.owner}/{model.name}: {model.description}")
```

## Core Resources

### Predictions

Create and manage model predictions.

```python
from replicate.types import Prediction

# Create a prediction
prediction = client.predictions.create(
    model="owner/model:version",
    input={"prompt": "hello world"},
    webhook="https://example.com/webhook",  # Optional webhook URL
    webhook_events_filter=["start", "completed"]  # Optional webhook events
)

# Get prediction status
prediction = client.predictions.get(prediction_id="abc123")
print(f"Status: {prediction.status}")
print(f"Output: {prediction.output}")

# Cancel a prediction
cancelled = client.predictions.cancel(prediction_id="abc123")

# List predictions
for prediction in client.predictions.list():
    print(f"{prediction.id}: {prediction.status}")

# Wait for a prediction to complete
completed = client.predictions.wait(
    prediction_id="abc123",
    timeout=60  # Optional timeout in seconds
)
```

### Models

Interact with models and their versions.

```python
# Get a specific model
model = client.models.get(model_owner="stability-ai", model_name="stable-diffusion")
print(f"Model: {model.owner}/{model.name}")
print(f"Description: {model.description}")
print(f"Latest version: {model.latest_version.id}")

# List all models (with pagination)
for model in client.models.list():
    print(f"{model.owner}/{model.name}")

# Search models
for model in client.models.search(query="text generation"):
    print(f"{model.owner}/{model.name}: {model.description}")

# Create a new model
model = client.models.create(
    owner="your-username",
    name="my-model",
    visibility="public",  # or "private"
    hardware="gpu-t4",  # Specify hardware requirements
    description="My custom model",
    github_url="https://github.com/user/repo"
)

# Delete a model
client.models.delete(model_owner="your-username", model_name="my-model")
```

#### Model Versions

```python
# List model versions
for version in client.models.versions.list(
    model_owner="stability-ai",
    model_name="stable-diffusion"
):
    print(f"Version {version.id}: created at {version.created_at}")

# Get a specific version
version = client.models.versions.get(
    model_owner="stability-ai",
    model_name="stable-diffusion",
    version_id="db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"
)

# Delete a version
client.models.versions.delete(
    model_owner="your-username",
    model_name="my-model",
    version_id="version-id"
)
```

#### Model Predictions

Run predictions directly through a model.

```python
# Create a prediction for a specific model
prediction = client.models.predictions.create(
    model_owner="stability-ai",
    model_name="stable-diffusion",
    input={"prompt": "a beautiful landscape"}
)
```

#### Model Examples

```python
# Get example predictions for a model
for example in client.models.examples.list(
    model_owner="stability-ai",
    model_name="stable-diffusion"
):
    print(f"Example input: {example.input}")
    print(f"Example output: {example.output}")
```

### Deployments

Manage model deployments for production use.

```python
# Create a deployment
deployment = client.deployments.create(
    name="my-deployment",
    model="owner/model:version",
    hardware="gpu-a100-large",
    min_instances=1,
    max_instances=10
)

# List deployments
for deployment in client.deployments.list():
    print(f"{deployment.owner}/{deployment.name}")

# Get deployment details
deployment = client.deployments.get(
    deployment_owner="your-username",
    deployment_name="my-deployment"
)

# Update deployment
updated = client.deployments.update(
    deployment_owner="your-username",
    deployment_name="my-deployment",
    min_instances=2,
    max_instances=20
)

# Delete deployment
client.deployments.delete(
    deployment_owner="your-username",
    deployment_name="my-deployment"
)

# Run a prediction on a deployment
prediction = client.deployments.predictions.create(
    deployment_owner="your-username",
    deployment_name="my-deployment",
    input={"prompt": "hello world"}
)
```

### Trainings

Create and manage model training jobs.

```python
# Start a training job
training = client.trainings.create(
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
training = client.trainings.get(training_id="training-abc123")
print(f"Status: {training.status}")

# List trainings
for training in client.trainings.list():
    print(f"{training.id}: {training.status}")

# Cancel a training
cancelled = client.trainings.cancel(training_id="training-abc123")
```

### Collections

Browse curated model collections.

```python
# List collections
for collection in client.collections.list():
    print(f"{collection.name}: {collection.description}")

# Get a specific collection
collection = client.collections.get(collection_slug="awesome-sdxl-models")
for model in collection.models:
    print(f"- {model.owner}/{model.name}")
```

### Files

Upload and manage files for model inputs.

```python
# Create/upload a file
with open("image.jpg", "rb") as f:
    file_response = client.files.create(file=f)
    file_url = file_response.urls.get

# List files
for file in client.files.list():
    print(f"{file.id}: {file.name}")

# Get file details
file = client.files.get(file_id="file-abc123")
print(f"File URL: {file.urls.get}")

# Delete a file
client.files.delete(file_id="file-abc123")
```

### Hardware

Get information about available hardware.

```python
# List available hardware SKUs
hardware_list = client.hardware.list()
for sku in hardware_list:
    print(f"{sku.name}: {sku.specs}")
```

### Account

Manage account information.

```python
# Get account details
account = client.account.get()
print(f"Username: {account.username}")
print(f"Email: {account.email}")
```

### Webhooks

Configure webhooks for predictions.

```python
# Get the default webhook secret
webhook_secret = client.webhooks.default.secret.get()
print(f"Webhook signing secret: {webhook_secret.key}")
```

## File Handling

### Input Files

The SDK supports multiple ways to provide file inputs:

```python
# File object
with open("input.jpg", "rb") as f:
    output = client.run("model:version", input={"image": f})

# File path (automatically opened)
output = client.run("model:version", input={"image": "path/to/image.jpg"})

# URL
output = client.run("model:version", input={"image": "https://example.com/image.jpg"})

# Base64 data URI
output = client.run("model:version", input={"image": "data:image/jpeg;base64,..."})

# Control encoding strategy
output = client.run(
    "model:version",
    input={"image": file_obj},
    file_encoding_strategy="base64"  # or "url" (uploads to Replicate)
)
```

### Output Files

File outputs are automatically converted to `FileOutput` objects:

```python
from replicate.helpers import FileOutput

output = client.run("model:version", input={"prompt": "generate an image"})

# If output is a FileOutput
if isinstance(output, FileOutput):
    # Get the URL
    print(f"File URL: {output.url}")
    
    # Read the file content
    content = output.read()
    
    # Save to disk
    with open("output.jpg", "wb") as f:
        for chunk in output:
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
    output = client.run("model:version", input={"prompt": "test"})
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
for model in client.models.list():
    print(model.name)

# Manual pagination
first_page = client.models.list()
print(f"Items in first page: {len(first_page.items)}")

if first_page.has_next_page():
    next_page = first_page.get_next_page()
    print(f"Items in second page: {len(next_page.items)}")

# Get all items at once
all_models = list(client.models.list())
```

## Advanced Features

### Raw Response Access

Access the underlying HTTP response:

```python
# Get raw response
response = client.predictions.with_raw_response.create(
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

Configure a custom HTTP client:

```python
import httpx
from replicate import DefaultHttpxClient

# With proxy
client = Replicate(
    http_client=DefaultHttpxClient(
        proxy="http://proxy.example.com:8080"
    )
)

# With custom timeout
client = Replicate(
    http_client=DefaultHttpxClient(
        timeout=httpx.Timeout(60.0)
    )
)
```

### Retries and Timeouts

Configure retry behavior and timeouts:

```python
client = Replicate(
    max_retries=5,  # Maximum number of retries
    timeout=120.0  # Request timeout in seconds
)

# Per-request timeout
output = client.run(
    "model:version",
    input={"prompt": "test"},
    wait=60  # Wait up to 60 seconds for completion
)
```

### Client Copying

Create a new client with modified settings:

```python
# Create a copy with different settings
new_client = client.copy(
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
    client = AsyncReplicate()
    
    # Run a model
    output = await client.run(
        "stability-ai/stable-diffusion",
        input={"prompt": "a futuristic city"}
    )
    
    # Stream output
    async for event in client.stream(
        "meta/llama-2-70b-chat",
        input={"prompt": "Tell me a joke"}
    ):
        print(event, end="")
    
    # Pagination
    async for model in client.models.list():
        print(model.name)
    
    # Concurrent requests
    tasks = [
        client.run("model1", input={"prompt": "test1"}),
        client.run("model2", input={"prompt": "test2"}),
        client.run("model3", input={"prompt": "test3"})
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
from replicate import Replicate
from replicate.types import Prediction, PredictionStatus
from replicate.pagination import SyncCursorURLPage

client: Replicate = Replicate()

# Type hints for responses
prediction: Prediction = client.predictions.get(prediction_id="abc123")
status: PredictionStatus = prediction.status

# Type hints for pagination
page: SyncCursorURLPage[Prediction] = client.predictions.list()
```

## Common Patterns

### Wait for Completion with Polling

```python
import time

def wait_for_prediction(client, prediction_id, timeout=300):
    """Poll a prediction until it completes or times out."""
    start = time.time()
    while time.time() - start < timeout:
        prediction = client.predictions.get(prediction_id)
        if prediction.status in ["succeeded", "failed", "canceled"]:
            return prediction
        time.sleep(2)  # Poll every 2 seconds
    raise TimeoutError(f"Prediction {prediction_id} timed out")

# Usage
prediction = client.predictions.create(model="model:version", input={})
result = wait_for_prediction(client, prediction.id)
```

### Batch Processing

```python
import asyncio
from replicate import AsyncReplicate

async def batch_process(prompts):
    """Process multiple prompts in parallel."""
    client = AsyncReplicate()
    tasks = [
        client.run("model:version", input={"prompt": prompt})
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
    secret = "your_webhook_secret"  # Get from client.webhooks.default.secret.get()
    
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

# Run a model
output = replicate.run(
    "stability-ai/stable-diffusion:version",
    input={"prompt": "a cat"}
)

# Get a model
model = replicate.models.get("stability-ai/stable-diffusion")
```

**New (v1.0+):**
```python
from replicate import Replicate

client = Replicate()

# Run a model
output = client.run(
    "stability-ai/stable-diffusion:version",
    input={"prompt": "a cat"}
)

# Get a model
model = client.models.get(
    model_owner="stability-ai",
    model_name="stable-diffusion"
)
```

### Using Legacy Authentication

For compatibility with older code:

```python
# Old style (still supported)
client = Replicate(api_token="your_token")

# New style (recommended)
client = Replicate(bearer_token="your_token")
```

## Support

- **Documentation**: https://replicate.com/docs
- **GitHub**: https://github.com/replicate/replicate-python
- **Discord**: https://discord.gg/replicate
- **API Reference**: https://replicate.com/docs/api

## License

Apache License 2.0