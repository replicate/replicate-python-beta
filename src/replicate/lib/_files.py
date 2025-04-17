from __future__ import annotations

import io
import base64
import mimetypes
from typing import Any, Iterator, AsyncIterator
from typing_extensions import override

import httpx

from .._utils import is_mapping, is_sequence
from .._client import ReplicateClient, AsyncReplicateClient


def base64_encode_file(file: io.IOBase) -> str:
    """
    Base64 encode a file.

    Args:
        file: A file handle to upload.
    Returns:
        str: A base64-encoded data URI.
    """

    file.seek(0)
    body = file.read()

    # Ensure the file handle is in bytes
    body = body.encode("utf-8") if isinstance(body, str) else body
    encoded_body = base64.b64encode(body).decode("utf-8")

    mime_type = mimetypes.guess_type(getattr(file, "name", ""))[0] or "application/octet-stream"
    return f"data:{mime_type};base64,{encoded_body}"


class FileOutput(httpx.SyncByteStream):
    """
    An object that can be used to read the contents of an output file
    created by running a Replicate model.
    """

    url: str
    """
    The file URL.
    """

    _client: ReplicateClient

    def __init__(self, url: str, client: ReplicateClient) -> None:
        self.url = url
        self._client = client

    def read(self) -> bytes:
        if self.url.startswith("data:"):
            _, encoded = self.url.split(",", 1)
            return base64.b64decode(encoded)

        with self._client._client.stream("GET", self.url) as response:
            response.raise_for_status()
            return response.read()

    @override
    def __iter__(self) -> Iterator[bytes]:
        if self.url.startswith("data:"):
            yield self.read()
            return

        with self._client._client.stream("GET", self.url) as response:
            response.raise_for_status()
            yield from response.iter_bytes()

    @override
    def __str__(self) -> str:
        return self.url

    @override
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.url}")'


class AsyncFileOutput(httpx.AsyncByteStream):
    """
    An object that can be used to read the contents of an output file
    created by running a Replicate model.
    """

    url: str
    """
    The file URL.
    """

    _client: AsyncReplicateClient

    def __init__(self, url: str, client: AsyncReplicateClient) -> None:
        self.url = url
        self._client = client

    async def read(self) -> bytes:
        if self.url.startswith("data:"):
            _, encoded = self.url.split(",", 1)
            return base64.b64decode(encoded)

        async with self._client._client.stream("GET", self.url) as response:
            response.raise_for_status()
            return await response.aread()

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        if self.url.startswith("data:"):
            yield await self.read()
            return

        async with self._client._client.stream("GET", self.url) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes():
                yield chunk

    @override
    def __str__(self) -> str:
        return self.url

    @override
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.url}")'


def transform_output(value: Any, client: ReplicateClient | AsyncReplicateClient) -> Any:
    """
    Transform the output of a prediction to a `FileOutput` object if it's a URL.
    """

    def transform(obj: Any) -> Any:
        if is_mapping(obj):
            return {k: transform(v) for k, v in obj.items()}
        elif is_sequence(obj) and not isinstance(obj, str):
            return [transform(item) for item in obj]
        elif isinstance(obj, str) and (obj.startswith("https:") or obj.startswith("data:")):
            if isinstance(client, AsyncReplicateClient):
                return AsyncFileOutput(obj, client)
            return FileOutput(obj, client)
        return obj

    return transform(value)
