from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union, Iterable, Optional
from typing_extensions import Unpack

from replicate.lib._files import FileEncodingStrategy
from replicate.types.prediction_create_params import PredictionCreateParamsWithoutVersion

from ..types import PredictionOutput, PredictionCreateParams
from .._types import NOT_GIVEN, NotGiven
from .._utils import is_given
from ._models import Model, Version, ModelVersionIdentifier, resolve_reference
from .._exceptions import ModelError

if TYPE_CHECKING:
    from ._files import FileOutput
    from .._client import ReplicateClient, AsyncReplicateClient


def run(
    client: "ReplicateClient",
    ref: Union[Model, Version, ModelVersionIdentifier, str],
    *,
    wait: Union[int, bool, NotGiven] = NOT_GIVEN,
    use_file_output: Optional[bool] = True,
    file_encoding_strategy: Optional["FileEncodingStrategy"] = None,
    **params: Unpack[PredictionCreateParamsWithoutVersion],
) -> PredictionOutput | FileOutput | Iterable[FileOutput] | Dict[str, FileOutput]:
    """
    Run a model prediction.

    Args:
        client: The ReplicateClient instance to use for API calls
        ref: Reference to the model or version to run. Can be:
            - A string containing a version ID (e.g. "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa")
            - A string with owner/name format (e.g. "replicate/hello-world")
            - A string with owner/name/version format (e.g. "replicate/hello-world/5c7d5dc6...")
            - A Model instance with owner and name attributes
            - A Version instance with id attribute
            - A ModelVersionIdentifier dictionary with owner, name, and/or version keys
        input: Dictionary of input parameters for the model
        wait: If True (default), wait for the prediction to complete. If False, return immediately.
              If an integer, wait up to that many seconds.
        use_file_output: If True (default), convert output URLs to FileOutput objects
        **params: Additional parameters to pass to the prediction creation endpoint

    Returns:
        The prediction output, which could be a basic type (str, int, etc.), a FileOutput object,
        a list of FileOutput objects, or a dictionary of FileOutput objects, depending on what
        the model returns.

    Raises:
        ModelError: If the model run fails
        ValueError: If the reference format is invalid
        TypeError: If both wait and prefer parameters are provided
    """
    from ._files import transform_output

    if is_given(wait) and "prefer" in params:
        raise TypeError("cannot mix and match prefer and wait")

    if not is_given(wait):
        wait = True

    is_blocking = wait != False

    if wait:
        if wait is True:
            params.setdefault("prefer", "wait")
        else:
            params.setdefault("prefer", f"wait={wait}")

    # Resolve ref to its components
    _version, owner, name, version_id = resolve_reference(ref)

    prediction = None
    if version_id is not None:
        # Create prediction with the specific version ID
        params_with_version: PredictionCreateParams = {**params, "version": version_id}
        prediction = client.predictions.create(file_encoding_strategy=file_encoding_strategy, **params_with_version)
    elif owner and name:
        # Create prediction via models resource with owner/name
        prediction = client.models.predictions.create(
            file_encoding_strategy=file_encoding_strategy, model_owner=owner, model_name=name, **params
        )
    else:
        # If ref is a string but doesn't match expected patterns
        if isinstance(ref, str):
            params_with_version = {**params, "version": ref}
            prediction = client.predictions.create(file_encoding_strategy=file_encoding_strategy, **params_with_version)
        else:
            raise ValueError(
                f"Invalid reference format: {ref}. Expected a model name ('owner/name'), "
                "a version ID, a Model object, a Version object, or a ModelVersionIdentifier."
            )

    # Currently the "Prefer: wait" interface will return a prediction with a status
    # of "processing" rather than a terminal state because it returns before the
    # prediction has been fully processed. If request exceeds the wait time, even if
    # it is actually processing, the prediction will be in a "starting" state.
    #
    # We should fix this in the blocking API itself. Predictions that are done should
    # be in a terminal state and predictions that are processing should be in state
    # "processing".
    in_terminal_state = is_blocking and prediction.status != "starting"
    if not in_terminal_state:
        # TODO: Return a "polling" iterator if the model has an output iterator array type.

        prediction = client.predictions.wait(prediction.id)

    if prediction.status == "failed":
        raise ModelError(prediction)

    # TODO: Return an iterator for completed output if the model has an output iterator array type.

    if use_file_output:
        return transform_output(prediction.output, client)  # type: ignore[no-any-return]

    return prediction.output


async def async_run(
    client: "AsyncReplicateClient",
    ref: Union[Model, Version, ModelVersionIdentifier, str],
    *,
    file_encoding_strategy: Optional["FileEncodingStrategy"] = None,
    wait: Union[int, bool, NotGiven] = NOT_GIVEN,
    use_file_output: Optional[bool] = True,
    **params: Unpack[PredictionCreateParamsWithoutVersion],
) -> PredictionOutput | FileOutput | Iterable[FileOutput] | Dict[str, FileOutput]:
    """
    Run a model prediction asynchronously.

    Args:
        client: The AsyncReplicateClient instance to use for API calls
        ref: Reference to the model or version to run. Can be:
            - A string containing a version ID (e.g. "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa")
            - A string with owner/name format (e.g. "replicate/hello-world")
            - A string with owner/name/version format (e.g. "replicate/hello-world/5c7d5dc6...")
            - A Model instance with owner and name attributes
            - A Version instance with id attribute
            - A ModelVersionIdentifier dictionary with owner, name, and/or version keys
        input: Dictionary of input parameters for the model
        wait: If True (default), wait for the prediction to complete. If False, return immediately.
              If an integer, wait up to that many seconds.
        use_file_output: If True (default), convert output URLs to AsyncFileOutput objects
        **params: Additional parameters to pass to the prediction creation endpoint

    Returns:
        The prediction output, which could be a basic type (str, int, etc.), an AsyncFileOutput object,
        a list of AsyncFileOutput objects, or a dictionary of AsyncFileOutput objects, depending on what
        the model returns.

    Raises:
        ModelError: If the model run fails
        ValueError: If the reference format is invalid
        TypeError: If both wait and prefer parameters are provided
    """
    from ._files import transform_output

    if is_given(wait) and "prefer" in params:
        raise TypeError("cannot mix and match prefer and wait")

    if not is_given(wait):
        wait = True

    is_blocking = wait != False

    if wait:
        if wait is True:
            params.setdefault("prefer", "wait")
        else:
            params.setdefault("prefer", f"wait={wait}")

    # Resolve ref to its components
    _version, owner, name, version_id = resolve_reference(ref)

    prediction = None
    if version_id is not None:
        # Create prediction with the specific version ID
        params_with_version: PredictionCreateParams = {**params, "version": version_id}
        prediction = await client.predictions.create(
            file_encoding_strategy=file_encoding_strategy, **params_with_version
        )
    elif owner and name:
        # Create prediction via models resource with owner/name
        prediction = await client.models.predictions.create(
            model_owner=owner, model_name=name, file_encoding_strategy=file_encoding_strategy, **params
        )
    else:
        # If ref is a string but doesn't match expected patterns
        if isinstance(ref, str):
            params_with_version = {**params, "version": ref}
            prediction = await client.predictions.create(
                file_encoding_strategy=file_encoding_strategy, **params_with_version
            )
        else:
            raise ValueError(
                f"Invalid reference format: {ref}. Expected a model name ('owner/name'), "
                "a version ID, a Model object, a Version object, or a ModelVersionIdentifier."
            )

    # Currently the "Prefer: wait" interface will return a prediction with a status
    # of "processing" rather than a terminal state because it returns before the
    # prediction has been fully processed. If request exceeds the wait time, even if
    # it is actually processing, the prediction will be in a "starting" state.
    #
    # We should fix this in the blocking API itself. Predictions that are done should
    # be in a terminal state and predictions that are processing should be in state
    # "processing".
    in_terminal_state = is_blocking and prediction.status != "starting"
    if not in_terminal_state:
        # TODO: Return a "polling" iterator if the model has an output iterator array type.

        prediction = await client.predictions.wait(prediction.id)

    if prediction.status == "failed":
        raise ModelError(prediction)

    # TODO: Return an iterator for completed output if the model has an output iterator array type.

    if use_file_output:
        return transform_output(prediction.output, client)  # type: ignore[no-any-return]

    return prediction.output
