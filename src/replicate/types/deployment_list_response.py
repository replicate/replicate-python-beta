# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "DeploymentListResponse",
    "Result",
    "ResultCurrentRelease",
    "ResultCurrentReleaseConfiguration",
    "ResultCurrentReleaseCreatedBy",
]


class ResultCurrentReleaseConfiguration(BaseModel):
    hardware: Optional[str] = None
    """The SKU for the hardware used to run the model."""

    max_instances: Optional[int] = None
    """The maximum number of instances for scaling."""

    min_instances: Optional[int] = None
    """The minimum number of instances for scaling."""


class ResultCurrentReleaseCreatedBy(BaseModel):
    type: Literal["organization", "user"]
    """The account type of the creator. Can be a user or an organization."""

    username: str
    """The username of the account that created the release."""

    avatar_url: Optional[str] = None
    """The avatar URL for the account that created the release."""

    github_url: Optional[str] = None
    """The GitHub URL of the account that created the release."""

    name: Optional[str] = None
    """The name of the account that created the release."""


class ResultCurrentRelease(BaseModel):
    configuration: Optional[ResultCurrentReleaseConfiguration] = None

    created_at: Optional[datetime] = None
    """The time the release was created."""

    created_by: Optional[ResultCurrentReleaseCreatedBy] = None

    model: Optional[str] = None
    """The model identifier string in the format of `{model_owner}/{model_name}`."""

    number: Optional[int] = None
    """The release number.

    This is an auto-incrementing integer that starts at 1, and is set automatically
    when a deployment is created.
    """

    version: Optional[str] = None
    """The ID of the model version used in the release."""


class Result(BaseModel):
    current_release: Optional[ResultCurrentRelease] = None

    name: Optional[str] = None
    """The name of the deployment."""

    owner: Optional[str] = None
    """The owner of the deployment."""


class DeploymentListResponse(BaseModel):
    next: Optional[str] = None
    """A URL pointing to the next page of deployment objects if any"""

    previous: Optional[str] = None
    """A URL pointing to the previous page of deployment objects if any"""

    results: Optional[List[Result]] = None
    """An array containing a page of deployment objects"""
