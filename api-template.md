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

<!-- API_OPERATIONS -->

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
