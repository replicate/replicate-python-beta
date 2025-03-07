# Collections

Methods:

- <code title="get /collections/{collection_slug}">client.collections.<a href="./src/replicate_client/resources/collections.py">retrieve</a>(collection_slug) -> None</code>
- <code title="get /collections">client.collections.<a href="./src/replicate_client/resources/collections.py">list</a>() -> None</code>

# Deployments

Types:

```python
from replicate_client.types import (
    PredictionRequest,
    PredictionResponse,
    DeploymentCreateResponse,
    DeploymentRetrieveResponse,
    DeploymentUpdateResponse,
    DeploymentListResponse,
)
```

Methods:

- <code title="post /deployments">client.deployments.<a href="./src/replicate_client/resources/deployments.py">create</a>(\*\*<a href="src/replicate_client/types/deployment_create_params.py">params</a>) -> <a href="./src/replicate_client/types/deployment_create_response.py">DeploymentCreateResponse</a></code>
- <code title="get /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/replicate_client/resources/deployments.py">retrieve</a>(deployment_name, \*, deployment_owner) -> <a href="./src/replicate_client/types/deployment_retrieve_response.py">DeploymentRetrieveResponse</a></code>
- <code title="patch /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/replicate_client/resources/deployments.py">update</a>(deployment_name, \*, deployment_owner, \*\*<a href="src/replicate_client/types/deployment_update_params.py">params</a>) -> <a href="./src/replicate_client/types/deployment_update_response.py">DeploymentUpdateResponse</a></code>
- <code title="get /deployments">client.deployments.<a href="./src/replicate_client/resources/deployments.py">list</a>() -> <a href="./src/replicate_client/types/deployment_list_response.py">DeploymentListResponse</a></code>
- <code title="delete /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/replicate_client/resources/deployments.py">delete</a>(deployment_name, \*, deployment_owner) -> None</code>
- <code title="post /deployments/{deployment_owner}/{deployment_name}/predictions">client.deployments.<a href="./src/replicate_client/resources/deployments.py">create_prediction</a>(deployment_name, \*, deployment_owner, \*\*<a href="src/replicate_client/types/deployment_create_prediction_params.py">params</a>) -> <a href="./src/replicate_client/types/prediction_response.py">PredictionResponse</a></code>

# Hardware

Types:

```python
from replicate_client.types import HardwareListResponse
```

Methods:

- <code title="get /hardware">client.hardware.<a href="./src/replicate_client/resources/hardware.py">list</a>() -> <a href="./src/replicate_client/types/hardware_list_response.py">HardwareListResponse</a></code>

# Accounts

Types:

```python
from replicate_client.types import AccountListResponse
```

Methods:

- <code title="get /account">client.accounts.<a href="./src/replicate_client/resources/accounts.py">list</a>() -> <a href="./src/replicate_client/types/account_list_response.py">AccountListResponse</a></code>

# Models

Methods:

- <code title="post /models">client.models.<a href="./src/replicate_client/resources/models/models.py">create</a>(\*\*<a href="src/replicate_client/types/model_create_params.py">params</a>) -> None</code>
- <code title="get /models/{model_owner}/{model_name}">client.models.<a href="./src/replicate_client/resources/models/models.py">retrieve</a>(model_name, \*, model_owner) -> None</code>
- <code title="get /models">client.models.<a href="./src/replicate_client/resources/models/models.py">list</a>() -> None</code>
- <code title="delete /models/{model_owner}/{model_name}">client.models.<a href="./src/replicate_client/resources/models/models.py">delete</a>(model_name, \*, model_owner) -> None</code>
- <code title="post /models/{model_owner}/{model_name}/predictions">client.models.<a href="./src/replicate_client/resources/models/models.py">create_prediction</a>(model_name, \*, model_owner, \*\*<a href="src/replicate_client/types/model_create_prediction_params.py">params</a>) -> <a href="./src/replicate_client/types/prediction_response.py">PredictionResponse</a></code>

## Versions

Methods:

- <code title="get /models/{model_owner}/{model_name}/versions/{version_id}">client.models.versions.<a href="./src/replicate_client/resources/models/versions.py">retrieve</a>(version_id, \*, model_owner, model_name) -> None</code>
- <code title="get /models/{model_owner}/{model_name}/versions">client.models.versions.<a href="./src/replicate_client/resources/models/versions.py">list</a>(model_name, \*, model_owner) -> None</code>
- <code title="delete /models/{model_owner}/{model_name}/versions/{version_id}">client.models.versions.<a href="./src/replicate_client/resources/models/versions.py">delete</a>(version_id, \*, model_owner, model_name) -> None</code>
- <code title="post /models/{model_owner}/{model_name}/versions/{version_id}/trainings">client.models.versions.<a href="./src/replicate_client/resources/models/versions.py">create_training</a>(version_id, \*, model_owner, model_name, \*\*<a href="src/replicate_client/types/models/version_create_training_params.py">params</a>) -> None</code>

# Predictions

Types:

```python
from replicate_client.types import PredictionListResponse
```

Methods:

- <code title="post /predictions">client.predictions.<a href="./src/replicate_client/resources/predictions.py">create</a>(\*\*<a href="src/replicate_client/types/prediction_create_params.py">params</a>) -> <a href="./src/replicate_client/types/prediction_response.py">PredictionResponse</a></code>
- <code title="get /predictions">client.predictions.<a href="./src/replicate_client/resources/predictions.py">list</a>(\*\*<a href="src/replicate_client/types/prediction_list_params.py">params</a>) -> <a href="./src/replicate_client/types/prediction_list_response.py">PredictionListResponse</a></code>
- <code title="post /predictions/{prediction_id}/cancel">client.predictions.<a href="./src/replicate_client/resources/predictions.py">cancel</a>(prediction_id) -> None</code>
- <code title="get /predictions/{prediction_id}">client.predictions.<a href="./src/replicate_client/resources/predictions.py">list_by_id</a>(prediction_id) -> <a href="./src/replicate_client/types/prediction_response.py">PredictionResponse</a></code>

# Trainings

Methods:

- <code title="get /trainings/{training_id}">client.trainings.<a href="./src/replicate_client/resources/trainings.py">retrieve</a>(training_id) -> None</code>
- <code title="get /trainings">client.trainings.<a href="./src/replicate_client/resources/trainings.py">list</a>() -> None</code>
- <code title="post /trainings/{training_id}/cancel">client.trainings.<a href="./src/replicate_client/resources/trainings.py">cancel</a>(training_id) -> None</code>

# Webhooks

## Default

Types:

```python
from replicate_client.types.webhooks import DefaultRetrieveSecretResponse
```

Methods:

- <code title="get /webhooks/default/secret">client.webhooks.default.<a href="./src/replicate_client/resources/webhooks/default.py">retrieve_secret</a>() -> <a href="./src/replicate_client/types/webhooks/default_retrieve_secret_response.py">DefaultRetrieveSecretResponse</a></code>
