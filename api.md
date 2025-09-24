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

Available operations:

- [`search`](#search)
- [`predictions.create`](#predictionscreate)
- [`predictions.get`](#predictionsget)
- [`predictions.list`](#predictionslist)
- [`predictions.cancel`](#predictionscancel)
- [`models.create`](#modelscreate)
- [`models.get`](#modelsget)
- [`models.list`](#modelslist)
- [`models.delete`](#modelsdelete)
- [`models.examples.list`](#modelsexampleslist)
- [`models.predictions.create`](#modelspredictionscreate)
- [`models.readme.get`](#modelsreadmeget)
- [`models.versions.get`](#modelsversionsget)
- [`models.versions.list`](#modelsversionslist)
- [`models.versions.delete`](#modelsversionsdelete)
- [`collections.get`](#collectionsget)
- [`collections.list`](#collectionslist)
- [`deployments.create`](#deploymentscreate)
- [`deployments.get`](#deploymentsget)
- [`deployments.list`](#deploymentslist)
- [`deployments.update`](#deploymentsupdate)
- [`deployments.delete`](#deploymentsdelete)
- [`deployments.predictions.create`](#deploymentspredictionscreate)
- [`files.list`](#fileslist)
- [`files.create`](#filescreate)
- [`files.delete`](#filesdelete)
- [`files.get`](#filesget)
- [`files.download`](#filesdownload)
- [`trainings.create`](#trainingscreate)
- [`trainings.get`](#trainingsget)
- [`trainings.list`](#trainingslist)
- [`trainings.cancel`](#trainingscancel)
- [`hardware.list`](#hardwarelist)
- [`account.get`](#accountget)
- [`webhooks.default.secret.get`](#webhooksdefaultsecretget)

### `search`

Search models, collections, and docs (beta)


```python
response = replicate.search(
    query="nano banana",
)
print(response.collections)
```

Docs: https://replicate.com/docs/reference/http#search

---

### `predictions.create`

Create a prediction


```python
prediction = replicate.predictions.create(
    input={
        "text": "Alice"
    },
    version="replicate/hello-world:9dcd6d78e7c6560c340d916fe32e9f24aabfa331e5cce95fe31f77fb03121426",
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#predictions.create

---

### `predictions.get`

Get a prediction


```python
prediction = replicate.predictions.get(
    prediction_id="prediction_id",
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#predictions.get

---

### `predictions.list`

List predictions


```python
page = replicate.predictions.list()
page = page.results[0]
print(page.id)
```

Docs: https://replicate.com/docs/reference/http#predictions.list

---

### `predictions.cancel`

Cancel a prediction


```python
prediction = replicate.predictions.cancel(
    prediction_id="prediction_id",
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#predictions.cancel

---

### `models.create`

Create a model


```python
model = replicate.models.create(
    hardware="cpu",
    name="hot-dog-detector",
    owner="alice",
    visibility="public",
)
print(model.cover_image_url)
```

Docs: https://replicate.com/docs/reference/http#models.create

---

### `models.get`

Get a model


```python
model = replicate.models.get(
    model_owner="model_owner",
    model_name="model_name",
)
print(model.cover_image_url)
```

Docs: https://replicate.com/docs/reference/http#models.get

---

### `models.list`

List public models


```python
page = replicate.models.list()
page = page.results[0]
print(page.cover_image_url)
```

Docs: https://replicate.com/docs/reference/http#models.list

---

### `models.delete`

Delete a model


```python
replicate.models.delete(
    model_owner="model_owner",
    model_name="model_name",
)
```

Docs: https://replicate.com/docs/reference/http#models.delete

---

### `models.examples.list`

List examples for a model


```python
page = replicate.models.examples.list(
    model_owner="model_owner",
    model_name="model_name",
)
page = page.results[0]
print(page.id)
```

Docs: https://replicate.com/docs/reference/http#models.examples.list

---

### `models.predictions.create`

Create a prediction using an official model


```python
prediction = replicate.models.predictions.create(
    model_owner="model_owner",
    model_name="model_name",
    input={
        "prompt": "Tell me a joke",
        "system_prompt": "You are a helpful assistant",
    },
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#models.predictions.create

---

### `models.readme.get`

Get a model's README


```python
readme = replicate.models.readme.get(
    model_owner="model_owner",
    model_name="model_name",
)
print(readme)
```

Docs: https://replicate.com/docs/reference/http#models.readme.get

---

### `models.versions.get`

Get a model version


```python
version = replicate.models.versions.get(
    model_owner="model_owner",
    model_name="model_name",
    version_id="version_id",
)
print(version.id)
```

Docs: https://replicate.com/docs/reference/http#models.versions.get

---

### `models.versions.list`

List model versions


```python
page = replicate.models.versions.list(
    model_owner="model_owner",
    model_name="model_name",
)
page = page.results[0]
print(page.id)
```

Docs: https://replicate.com/docs/reference/http#models.versions.list

---

### `models.versions.delete`

Delete a model version


```python
replicate.models.versions.delete(
    model_owner="model_owner",
    model_name="model_name",
    version_id="version_id",
)
```

Docs: https://replicate.com/docs/reference/http#models.versions.delete

---

### `collections.get`

Get a collection of models


```python
collection = replicate.collections.get(
    collection_slug="collection_slug",
)
print(collection.description)
```

Docs: https://replicate.com/docs/reference/http#collections.get

---

### `collections.list`

List collections of models


```python
page = replicate.collections.list()
page = page.results[0]
print(page.description)
```

Docs: https://replicate.com/docs/reference/http#collections.list

---

### `deployments.create`

Create a deployment


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

---

### `deployments.get`

Get a deployment


```python
deployment = replicate.deployments.get(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
)
print(deployment.current_release)
```

Docs: https://replicate.com/docs/reference/http#deployments.get

---

### `deployments.list`

List deployments


```python
page = replicate.deployments.list()
page = page.results[0]
print(page.current_release)
```

Docs: https://replicate.com/docs/reference/http#deployments.list

---

### `deployments.update`

Update a deployment


```python
deployment = replicate.deployments.update(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
)
print(deployment.current_release)
```

Docs: https://replicate.com/docs/reference/http#deployments.update

---

### `deployments.delete`

Delete a deployment


```python
replicate.deployments.delete(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
)
```

Docs: https://replicate.com/docs/reference/http#deployments.delete

---

### `deployments.predictions.create`

Create a prediction using a deployment


```python
prediction = replicate.deployments.predictions.create(
    deployment_owner="deployment_owner",
    deployment_name="deployment_name",
    input={
        "prompt": "Tell me a joke",
        "system_prompt": "You are a helpful assistant",
    },
)
print(prediction.id)
```

Docs: https://replicate.com/docs/reference/http#deployments.predictions.create

---

### `files.list`

List files


```python
page = replicate.files.list()
page = page.results[0]
print(page.id)
```

Docs: https://replicate.com/docs/reference/http#files.list

---

### `files.create`

Create a file


```python
file = replicate.files.create(
    content=b"raw file contents",
)
print(file.id)
```

Docs: https://replicate.com/docs/reference/http#files.create

---

### `files.delete`

Delete a file


```python
replicate.files.delete(
    file_id="file_id",
)
```

Docs: https://replicate.com/docs/reference/http#files.delete

---

### `files.get`

Get a file


```python
file = replicate.files.get(
    file_id="file_id",
)
print(file.id)
```

Docs: https://replicate.com/docs/reference/http#files.get

---

### `files.download`

Download a file


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

---

### `trainings.create`

Create a training


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

---

### `trainings.get`

Get a training


```python
training = replicate.trainings.get(
    training_id="training_id",
)
print(training.id)
```

Docs: https://replicate.com/docs/reference/http#trainings.get

---

### `trainings.list`

List trainings


```python
page = replicate.trainings.list()
page = page.results[0]
print(page.id)
```

Docs: https://replicate.com/docs/reference/http#trainings.list

---

### `trainings.cancel`

Cancel a training


```python
response = replicate.trainings.cancel(
    training_id="training_id",
)
print(response.id)
```

Docs: https://replicate.com/docs/reference/http#trainings.cancel

---

### `hardware.list`

List available hardware for models


```python
hardware = replicate.hardware.list()
print(hardware)
```

Docs: https://replicate.com/docs/reference/http#hardware.list

---

### `account.get`

Get the authenticated account


```python
account = replicate.account.get()
print(account.type)
```

Docs: https://replicate.com/docs/reference/http#account.get

---

### `webhooks.default.secret.get`

Get the signing secret for the default webhook


```python
secret = replicate.webhooks.default.secret.get()
print(secret.key)
```

Docs: https://replicate.com/docs/reference/http#webhooks.default.secret.get

---


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
