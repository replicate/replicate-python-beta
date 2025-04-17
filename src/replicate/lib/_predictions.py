from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union, Iterable
from typing_extensions import Unpack

from replicate.types.prediction_create_params import PredictionCreateParamsWithoutVersion

from ..types import PredictionOutput, PredictionCreateParams
from .._types import NOT_GIVEN, NotGiven
from .._utils import is_given
from .._client import ReplicateClient, AsyncReplicateClient
from .._exceptions import ModelError

if TYPE_CHECKING:
    from ._files import FileOutput


def run(
    client: ReplicateClient,
    ref: str,
    # TODO: support these types
    # ref: Union["Model", "Version", "ModelVersionIdentifier", str],
    *,
    wait: Union[int, bool, NotGiven] = NOT_GIVEN,
    # use_file_output: Optional[bool] = True,
    **params: Unpack[PredictionCreateParamsWithoutVersion],
) -> PredictionOutput | FileOutput | Iterable[FileOutput] | Dict[str, FileOutput]:
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

    # TODO: support more ref types
    params_with_version: PredictionCreateParams = {**params, "version": ref}
    prediction = client.predictions.create(**params_with_version)

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

    return transform_output(prediction.output, client)  # type: ignore[no-any-return]


async def async_run(
    client: AsyncReplicateClient,
    ref: str,
    # TODO: support these types
    # ref: Union["Model", "Version", "ModelVersionIdentifier", str],
    *,
    wait: Union[int, bool, NotGiven] = NOT_GIVEN,
    # use_file_output: Optional[bool] = True,
    **params: Unpack[PredictionCreateParams],
) -> PredictionOutput | FileOutput | Iterable[FileOutput] | Dict[str, FileOutput]:
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

    # TODO: support more ref types
    params_with_version: PredictionCreateParams = {**params, "version": ref}
    prediction = await client.predictions.create(**params_with_version)

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

    return transform_output(prediction.output, client)  # type: ignore[no-any-return]
