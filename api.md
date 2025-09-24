# Replicate Python SDK API reference

## Installation

```bash
pip install replicate
```

## Initialize a client

Start by setting a `REPLICATE_API_TOKEN` environment variable in your environment. You can create a token at [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens).

Then use this code to initialize a client:

```py
import replicate
```

That's it! You can now use the client to make API calls.


If you want to explicitly pass the token when creating a client, you can do so like this:


```python
import os
import replicate

client = replicate.Replicate(
    bearer_token=os.environ["REPLICATE_API_TOKEN"]
)
```

## High-level operations

### `replicate.use()`

Create a reference to a model that can be used to make predictions.

```python
import replicate

claude = replicate.use("anthropic/claude-sonnet-4")

output = claude(prompt="Hello, world!")
print(output)

banana = replicate.use("google/nano-banana")
output = banana(prompt="Make me a sandwich")
print(output)
```

Note: The `replicate.use()` method only returns output. If you need access to more metadata like prediction ID, status, metrics, or input values, use `replicate.predictions.create()` instead.

### `replicate.run()`

Run a model and wait for the output. This is a convenience method that creates a prediction and waits for it to complete.

```python
import replicate

# Run a model and get the output directly
output = replicate.run(
    "anthropic/claude-sonnet-4",
    input={"prompt": "Hello, world!"}
)
print(output)
```

Note: The `replicate.run()` method only returns output. If you need access to more metadata like prediction ID, status, metrics, or input values, use `replicate.predictions.create()` instead.


## API operations

### `search`

Search models, collections, and docs (beta)

Search for public models, collections, and docs using a text query.

For models, the response includes all model data, plus a new `metadata` object with the following fields:

- `generated_description`: A longer and more detailed AI-generated description of the model
- `tags`: An array of tags for the model
- `score`: A score for the model's relevance to the search query

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  "https://api.replicate.com/v1/search?query=nano+banana"
```

Note: This search API is currently in beta and may change in future versions.


```python
response = replicate.search(
    query="nano banana",
)
print(response.collections)
```

Docs: https://replicate.com/docs/reference/http#search

### `predictions.cancel`

Cancel a prediction

Cancel a prediction that is currently running.

Example cURL request that creates a prediction and then cancels it:

```console
# First, create a prediction
PREDICTION_ID=$(curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "a video that may take a while to generate"
    }
  }' \
  https://api.replicate.com/v1/models/minimax/video-01/predictions | jq -r '.id')

# Echo the prediction ID
echo "Created prediction with ID: $PREDICTION_ID"

# Cancel the prediction
curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/predictions/$PREDICTION_ID/cancel
```


```python
prediction = replicate.predictions.cancel(
    prediction_id="prediction_id",
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#predictions.cancel

### `predictions.get`

Get a prediction

Get the current state of a prediction.

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/predictions/gm3qorzdhgbfurvjtvhg6dckhu
```

The response will be the prediction object:

```json
{
  "id": "gm3qorzdhgbfurvjtvhg6dckhu",
  "model": "replicate/hello-world",
  "version": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
  "input": {
    "text": "Alice"
  },
  "logs": "",
  "output": "hello Alice",
  "error": null,
  "status": "succeeded",
  "created_at": "2023-09-08T16:19:34.765994Z",
  "data_removed": false,
  "started_at": "2023-09-08T16:19:34.779176Z",
  "completed_at": "2023-09-08T16:19:34.791859Z",
  "metrics": {
    "predict_time": 0.012683
  },
  "urls": {
    "web": "https://replicate.com/p/gm3qorzdhgbfurvjtvhg6dckhu",
    "get": "https://api.replicate.com/v1/predictions/gm3qorzdhgbfurvjtvhg6dckhu",
    "cancel": "https://api.replicate.com/v1/predictions/gm3qorzdhgbfurvjtvhg6dckhu/cancel"
  }
}
```

`status` will be one of:

- `starting`: the prediction is starting up. If this status lasts longer than a few seconds, then it's typically because a new worker is being started to run the prediction.
- `processing`: the `predict()` method of the model is currently running.
- `succeeded`: the prediction completed successfully.
- `failed`: the prediction encountered an error during processing.
- `canceled`: the prediction was canceled by its creator.

In the case of success, `output` will be an object containing the output of the model. Any files will be represented as HTTPS URLs. You'll need to pass the `Authorization` header to request them.

In the case of failure, `error` will contain the error encountered during the prediction.

Terminated predictions (with a status of `succeeded`, `failed`, or `canceled`) will include a `metrics` object with a `predict_time` property showing the amount of CPU or GPU time, in seconds, that the prediction used while running. It won't include time waiting for the prediction to start.

All input parameters, output values, and logs are automatically removed after an hour, by default, for predictions created through the API.

You must save a copy of any data or files in the output if you'd like to continue using them. The `output` key will still be present, but it's value will be `null` after the output has been removed.

Output files are served by `replicate.delivery` and its subdomains. If you use an allow list of external domains for your assets, add `replicate.delivery` and `*.replicate.delivery` to it.


```python
prediction = replicate.predictions.get(
    prediction_id="prediction_id",
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#predictions.get

### `trainings.create`

Create a training

Start a new training of the model version you specify.

Example request body:

```json
{
  "destination": "{new_owner}/{new_name}",
  "input": {
    "train_data": "https://example.com/my-input-images.zip",
  },
  "webhook": "https://example.com/my-webhook",
}
```

Example cURL request:

```console
curl -s -X POST \
  -d '{"destination": "{new_owner}/{new_name}", "input": {"input_images": "https://example.com/my-input-images.zip"}}' \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H 'Content-Type: application/json' \
  https://api.replicate.com/v1/models/stability-ai/sdxl/versions/da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf/trainings
```

The response will be the training object:

```json
{
  "id": "zz4ibbonubfz7carwiefibzgga",
  "model": "stability-ai/sdxl",
  "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
  "input": {
    "input_images": "https://example.com/my-input-images.zip"
  },
  "logs": "",
  "error": null,
  "status": "starting",
  "created_at": "2023-09-08T16:32:56.990893084Z",
  "urls": {
    "web": "https://replicate.com/p/zz4ibbonubfz7carwiefibzgga",
     "get": "https://api.replicate.com/v1/predictions/zz4ibbonubfz7carwiefibzgga",
     "cancel": "https://api.replicate.com/v1/predictions/zz4ibbonubfz7carwiefibzgga/cancel"
  }
}
```

As models can take several minutes or more to train, the result will not be available immediately. To get the final result of the training you should either provide a `webhook` HTTPS URL for us to call when the results are ready, or poll the [get a training](#trainings.get) endpoint until it has finished.

When a training completes, it creates a new [version](https://replicate.com/docs/how-does-replicate-work#terminology) of the model at the specified destination.

To find some models to train on, check out the [trainable language models collection](https://replicate.com/collections/trainable-language-models).


```python
training = replicate.trainings.create(
    model_owner="model_owner",
    model_name="model_name",
    version_id="version_id",
    destination="destination",
    input={},
)
print(training.id)
```

Docs: https://replicate.com/docs/reference/http#trainings.create

### `models.versions.get`

Get a model version

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/models/replicate/hello-world/versions/5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa
```

The response will be the version object:

```json
{
  "id": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
  "created_at": "2022-04-26T19:29:04.418669Z",
  "cog_version": "0.3.0",
  "openapi_schema": {...}
}
```

Every model describes its inputs and outputs with [OpenAPI Schema Objects](https://spec.openapis.org/oas/latest.html#schemaObject) in the `openapi_schema` property.

The `openapi_schema.components.schemas.Input` property for the [replicate/hello-world](https://replicate.com/replicate/hello-world) model looks like this:

```json
{
  "type": "object",
  "title": "Input",
  "required": [
    "text"
  ],
  "properties": {
    "text": {
      "x-order": 0,
      "type": "string",
      "title": "Text",
      "description": "Text to prefix with 'hello '"
    }
  }
}
```

The `openapi_schema.components.schemas.Output` property for the [replicate/hello-world](https://replicate.com/replicate/hello-world) model looks like this:

```json
{
  "type": "string",
  "title": "Output"
}
```

For more details, see the docs on [Cog's supported input and output types](https://github.com/replicate/cog/blob/75b7802219e7cd4cee845e34c4c22139558615d4/docs/python.md#input-and-output-types)


```python
version = replicate.models.versions.get(
    model_owner="model_owner",
    model_name="model_name",
    version_id="version_id",
)
print(version.id)
```

Docs: https://replicate.com/docs/reference/http#models.versions.get

### `models.versions.delete`

Delete a model version

Delete a model version and all associated predictions, including all output files.

Model version deletion has some restrictions:

- You can only delete versions from models you own.
- You can only delete versions from private models.
- You cannot delete a version if someone other than you has run predictions with it.
- You cannot delete a version if it is being used as the base model for a fine tune/training.
- You cannot delete a version if it has an associated deployment.
- You cannot delete a version if another model version is overridden to use it.

Example cURL request:

```command
curl -s -X DELETE \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/models/replicate/hello-world/versions/5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa
```

The response will be an empty 202, indicating the deletion request has been accepted. It might take a few minutes to be processed.


```python
replicate.models.versions.delete(
    model_owner="model_owner",
    model_name="model_name",
    version_id="version_id",
)
```

Docs: https://replicate.com/docs/reference/http#models.versions.delete

### `collections.get`

Get a collection of models

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/collections/super-resolution
```

The response will be a collection object with a nested list of the models in that collection:

```json
{
  "name": "Super resolution",
  "slug": "super-resolution",
  "description": "Upscaling models that create high-quality images from low-quality images.",
  "models": [...]
}
```


```python
collection = replicate.collections.get(
    collection_slug="collection_slug",
)
print(collection.description)
```

Docs: https://replicate.com/docs/reference/http#collections.get

### `deployments.create`

Create a deployment

Create a new deployment:

Example cURL request:

```console
curl -s \
  -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "my-app-image-generator",
        "model": "stability-ai/sdxl",
        "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
        "hardware": "gpu-t4",
        "min_instances": 0,
        "max_instances": 3
      }' \
  https://api.replicate.com/v1/deployments
```

The response will be a JSON object describing the deployment:

```json
{
  "owner": "acme",
  "name": "my-app-image-generator",
  "current_release": {
    "number": 1,
    "model": "stability-ai/sdxl",
    "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
    "created_at": "2024-02-15T16:32:57.018467Z",
    "created_by": {
      "type": "organization",
      "username": "acme",
      "name": "Acme Corp, Inc.",
      "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
      "github_url": "https://github.com/acme"
    },
    "configuration": {
      "hardware": "gpu-t4",
      "min_instances": 1,
      "max_instances": 5
    }
  }
}
```


```python
deployment = replicate.deployments.create(
    hardware="hardware",
    max_instances=0,
    min_instances=0,
    model="model",
    name="name",
    version="version",
)
print(deployment.current_release)
```

Docs: https://replicate.com/docs/reference/http#deployments.create

### `deployments.get`

Get a deployment

Get information about a deployment by name including the current release.

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/deployments/replicate/my-app-image-generator
```

The response will be a JSON object describing the deployment:

```json
{
  "owner": "acme",
  "name": "my-app-image-generator",
  "current_release": {
    "number": 1,
    "model": "stability-ai/sdxl",
    "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
    "created_at": "2024-02-15T16:32:57.018467Z",
    "created_by": {
      "type": "organization",
      "username": "acme",
      "name": "Acme Corp, Inc.",
      "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
      "github_url": "https://github.com/acme"
    },
    "configuration": {
      "hardware": "gpu-t4",
      "min_instances": 1,
      "max_instances": 5
    }
  }
}
```


```python
deployment = replicate.deployments.get(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
)
print(deployment.current_release)
```

Docs: https://replicate.com/docs/reference/http#deployments.get

### `deployments.update`

Update a deployment

Update properties of an existing deployment, including hardware, min/max instances, and the deployment's underlying model [version](https://replicate.com/docs/how-does-replicate-work#versions).

Example cURL request:

```console
curl -s \
  -X PATCH \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"min_instances": 3, "max_instances": 10}' \
  https://api.replicate.com/v1/deployments/acme/my-app-image-generator
```

The response will be a JSON object describing the deployment:

```json
{
  "owner": "acme",
  "name": "my-app-image-generator",
  "current_release": {
    "number": 2,
    "model": "stability-ai/sdxl",
    "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
    "created_at": "2024-02-15T16:32:57.018467Z",
    "created_by": {
      "type": "organization",
      "username": "acme",
      "name": "Acme Corp, Inc.",
      "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
      "github_url": "https://github.com/acme"
    },
    "configuration": {
      "hardware": "gpu-t4",
      "min_instances": 3,
      "max_instances": 10
    }
  }
}
```

Updating any deployment properties will increment the `number` field of the `current_release`.


```python
deployment = replicate.deployments.update(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
)
print(deployment.current_release)
```

Docs: https://replicate.com/docs/reference/http#deployments.update

### `deployments.delete`

Delete a deployment

Delete a deployment

Deployment deletion has some restrictions:

- You can only delete deployments that have been offline and unused for at least 15 minutes.

Example cURL request:

```command
curl -s -X DELETE \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/deployments/acme/my-app-image-generator
```

The response will be an empty 204, indicating the deployment has been deleted.


```python
replicate.deployments.delete(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
)
```

Docs: https://replicate.com/docs/reference/http#deployments.delete

### `files.list`

List files

Get a paginated list of all files created by the user or organization associated with the provided API token.

Example cURL request:

```console
curl -s \
  -H "Authorization: Token $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/files
```

The response will be a paginated JSON array of file objects, sorted with the most recent file first.


```python
page = replicate.files.list()
page = page.results[0]
print(page.id)
```

Docs: https://replicate.com/docs/reference/http#files.list

### `files.create`

Create a file

Create a file by uploading its content and optional metadata.

Example cURL request:

```console
curl -X POST https://api.replicate.com/v1/files \
  -H "Authorization: Token $REPLICATE_API_TOKEN" \
  -H 'Content-Type: multipart/form-data' \
  -F 'content=@/path/to/archive.zip;type=application/zip;filename=example.zip' \
  -F 'metadata={"customer_reference_id": 123};type=application/json'
```

The request must include:
- `content`: The file content (required)
- `type`: The content / MIME type for the file (defaults to `application/octet-stream`)
- `filename`: The filename (required, ≤ 255 bytes, valid UTF-8)
- `metadata`: User-provided metadata associated with the file (defaults to `{}`, must be valid JSON)


```python
file = replicate.files.create(
    content=b"raw file contents",
)
print(file.id)
```

Docs: https://replicate.com/docs/reference/http#files.create

### `files.delete`

Delete a file

Delete a file. Once a file has been deleted, subsequent requests to the file resource return 404 Not found.

Example cURL request:

```console
curl -X DELETE \
  -H "Authorization: Token $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/files/cneqzikepnug6xezperrr4z55o
```


```python
replicate.files.delete(
    file_id="file_id",
)
```

Docs: https://replicate.com/docs/reference/http#files.delete

### `files.download`

Download a file

Download a file by providing the file owner, access expiry, and a valid signature.

Example cURL request:

```console
curl -X GET "https://api.replicate.com/v1/files/cneqzikepnug6xezperrr4z55o/download?expiry=1708515345&owner=mattt&signature=zuoghqlrcnw8YHywkpaXQlHsVhWen%2FDZ4aal76dLiOo%3D"
```


```python
response = replicate.files.download(
    file_id="file_id",
    expiry=0,
    owner="owner",
    signature="signature",
)
print(response)
content = response.read()
print(content)
```

Docs: https://replicate.com/docs/reference/http#files.download

### `trainings.cancel`

Cancel a training


```python
response = replicate.trainings.cancel(
    training_id="training_id",
)
print(response.id)
```

Docs: https://replicate.com/docs/reference/http#trainings.cancel

### `trainings.get`

Get a training

Get the current state of a training.

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga
```

The response will be the training object:

```json
{
  "completed_at": "2023-09-08T16:41:19.826523Z",
  "created_at": "2023-09-08T16:32:57.018467Z",
  "error": null,
  "id": "zz4ibbonubfz7carwiefibzgga",
  "input": {
    "input_images": "https://example.com/my-input-images.zip"
  },
  "logs": "...",
  "metrics": {
    "predict_time": 502.713876
  },
  "output": {
    "version": "...",
    "weights": "..."
  },
  "started_at": "2023-09-08T16:32:57.112647Z",
  "status": "succeeded",
  "urls": {
    "web": "https://replicate.com/p/zz4ibbonubfz7carwiefibzgga",
    "get": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga",
    "cancel": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga/cancel"
  },
  "model": "stability-ai/sdxl",
  "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
}
```

`status` will be one of:

- `starting`: the training is starting up. If this status lasts longer than a few seconds, then it's typically because a new worker is being started to run the training.
- `processing`: the `train()` method of the model is currently running.
- `succeeded`: the training completed successfully.
- `failed`: the training encountered an error during processing.
- `canceled`: the training was canceled by its creator.

In the case of success, `output` will be an object containing the output of the model. Any files will be represented as HTTPS URLs. You'll need to pass the `Authorization` header to request them.

In the case of failure, `error` will contain the error encountered during the training.

Terminated trainings (with a status of `succeeded`, `failed`, or `canceled`) will include a `metrics` object with a `predict_time` property showing the amount of CPU or GPU time, in seconds, that the training used while running. It won't include time waiting for the training to start.


```python
training = replicate.trainings.get(
    training_id="training_id",
)
print(training.id)
```

Docs: https://replicate.com/docs/reference/http#trainings.get

### `hardware.list`

List available hardware for models

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/hardware
```

The response will be a JSON array of hardware objects:

```json
[
    {"name": "CPU", "sku": "cpu"},
    {"name": "Nvidia T4 GPU", "sku": "gpu-t4"},
    {"name": "Nvidia A40 GPU", "sku": "gpu-a40-small"},
    {"name": "Nvidia A40 (Large) GPU", "sku": "gpu-a40-large"},
]
```


```python
hardware = replicate.hardware.list()
print(hardware)
```

Docs: https://replicate.com/docs/reference/http#hardware.list

### `account.get`

Get the authenticated account

Returns information about the user or organization associated with the provided API token.

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/account
```

The response will be a JSON object describing the account:

```json
{
  "type": "organization",
  "username": "acme",
  "name": "Acme Corp, Inc.",
  "github_url": "https://github.com/acme",
}
```


```python
account = replicate.account.get()
print(account.type)
```

Docs: https://replicate.com/docs/reference/http#account.get

### `webhooks.default.secret.get`

Get the signing secret for the default webhook

Get the signing secret for the default webhook endpoint. This is used to verify that webhook requests are coming from Replicate.

Example cURL request:

```console
curl -s \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/webhooks/default/secret
```

The response will be a JSON object with a `key` property:

```json
{
  "key": "..."
}
```


```python
secret = replicate.webhooks.default.secret.get()
print(secret.key)
```

Docs: https://replicate.com/docs/reference/http#webhooks.default.secret.get


## Low-level API

For cases where you need to make direct API calls not covered by the SDK methods, you can use the low-level request interface:

### Making custom requests

```python
import replicate

client = replicate.Replicate()

# Make a custom GET request
response = client.get("/custom/endpoint")

# Make a custom POST request with data
response = client.post(
    "/custom/endpoint",
    json={"key": "value"}
)

# Make a custom request with all options
response = client.request(
    method="PATCH",
    url="/custom/endpoint",
    json={"key": "value"},
    headers={"X-Custom-Header": "value"}
)
```

See the [README](https://github.com/replicate/replicate-python-stainless/blob/main/README.md) for more details about response handing, error handling, pagination, async support, and more.
