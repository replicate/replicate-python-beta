from __future__ import annotations

import io
import os
from typing import Any, Dict, Optional

import httpx
import pytest
from respx import MockRouter

from replicate import ReplicateClient, AsyncReplicateClient
from replicate.lib._files import FileOutput, AsyncFileOutput
from replicate._exceptions import ModelError, NotFoundError, BadRequestError

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
bearer_token = "My Bearer Token"


# Mock prediction data for testing
def create_mock_prediction(
    status: str = "succeeded",
    output: Any = "test output",
    error: Optional[str] = None,
    logs: Optional[str] = None,
    urls: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    if urls is None:
        urls = {
            "get": "https://api.replicate.com/v1/predictions/test_prediction_id",
            "cancel": "https://api.replicate.com/v1/predictions/test_prediction_id/cancel",
        }

    return {
        "id": "test_prediction_id",
        "version": "test_version",
        "status": status,
        "input": {"prompt": "test prompt"},
        "output": output,
        "error": error,
        "logs": logs,
        "created_at": "2023-01-01T00:00:00Z",
        "started_at": "2023-01-01T00:00:01Z",
        "completed_at": "2023-01-01T00:00:02Z" if status in ["succeeded", "failed"] else None,
        "urls": urls,
        "model": "test-model",
        "data_removed": False,
    }


class TestRun:
    client = ReplicateClient(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    @pytest.mark.respx(base_url=base_url)
    def test_run_basic(self, respx_mock: MockRouter) -> None:
        """Test basic model run functionality."""
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = self.client.run("some-model-ref", input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_wait_true(self, respx_mock: MockRouter) -> None:
        """Test run with wait=True parameter."""
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = self.client.run("some-model-ref", wait=True, input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_wait_int(self, respx_mock: MockRouter) -> None:
        """Test run with wait as an integer value."""
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = self.client.run("some-model-ref", wait=10, input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    def test_run_without_wait(self, respx_mock: MockRouter) -> None:
        """Test run with wait=False parameter."""
        # Initial prediction state is "processing"
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(status="processing"))
        )

        # When we wait for it, it becomes "succeeded"
        respx_mock.get("/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction(status="succeeded"))
        )

        output: Any = self.client.run("some-model-ref", wait=False, input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url, assert_all_mocked=False)
    def test_run_with_file_output(self, respx_mock: MockRouter) -> None:
        """Test run with file output."""
        # Mock prediction with file URL output
        file_url = "https://replicate.delivery/output.png"
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(output=file_url))
        )

        output: Any = self.client.run("some-model-ref", input={"prompt": "generate image"})

        assert isinstance(output, FileOutput)
        assert output.url == file_url

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_file_list_output(self, respx_mock: MockRouter) -> None:
        """Test run with list of file outputs."""
        # Create a mock prediction response with a list of file URLs
        file_urls = ["https://replicate.delivery/output1.png", "https://replicate.delivery/output2.png"]
        mock_prediction = create_mock_prediction()
        mock_prediction["output"] = file_urls

        # Mock the endpoint
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=mock_prediction))

        output: list[FileOutput] = self.client.run("some-model-ref", input={"prompt": "generate multiple images"})

        assert isinstance(output, list)
        assert len(output) == 2
        assert all(isinstance(item, FileOutput) for item in output)

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_dict_file_output(self, respx_mock: MockRouter) -> None:
        """Test run with dictionary of file outputs."""
        # Mock prediction with dict of file URLs
        file_urls = {
            "image1": "https://replicate.delivery/output1.png",
            "image2": "https://replicate.delivery/output2.png",
        }
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(output=file_urls))
        )

        output: Dict[str, FileOutput] = self.client.run("some-model-ref", input={"prompt": "structured output"})

        assert isinstance(output, dict)
        assert len(output) == 2
        assert all(isinstance(item, FileOutput) for item in output.values())

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_error(self, respx_mock: MockRouter) -> None:
        """Test run with model error."""
        # Mock prediction with error
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(status="failed", error="Model error occurred"))
        )

        with pytest.raises(ModelError):
            self.client.run("error-model-ref", input={"prompt": "trigger error"})

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_base64_file(self, respx_mock: MockRouter) -> None:
        """Test run with base64 encoded file input."""
        # Create a simple file-like object
        file_obj = io.BytesIO(b"test content")

        # Mock the prediction response
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = self.client.run("some-model-ref", input={"file": file_obj})

        assert output == "test output"

    def test_run_with_prefer_conflict(self) -> None:
        """Test run with conflicting wait and prefer parameters."""
        with pytest.raises(TypeError, match="cannot mix and match prefer and wait"):
            self.client.run("some-model-ref", wait=True, prefer="nowait", input={"prompt": "test"})

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_iterator(self, respx_mock: MockRouter) -> None:
        """Test run with an iterator output."""
        # Create a mock prediction with an iterator output
        output_iterator = ["chunk1", "chunk2", "chunk3"]
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(output=output_iterator))
        )

        output: list[str] = self.client.run("some-model-ref", input={"prompt": "generate iterator"})

        assert isinstance(output, list)
        assert len(output) == 3
        assert output == output_iterator

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_invalid_identifier(self, respx_mock: MockRouter) -> None:
        """Test run with an invalid model identifier."""
        # Mock a 404 response for an invalid model identifier
        respx_mock.post("/predictions").mock(return_value=httpx.Response(404, json={"detail": "Model not found"}))

        with pytest.raises(NotFoundError):
            self.client.run("invalid-model-ref", input={"prompt": "test prompt"})

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_invalid_cog_version(self, respx_mock: MockRouter) -> None:
        """Test run with an invalid Cog version."""
        # Mock an error response for an invalid Cog version
        respx_mock.post("/predictions").mock(return_value=httpx.Response(400, json={"detail": "Invalid Cog version"}))

        with pytest.raises(BadRequestError):
            self.client.run("model-with-invalid-cog", input={"prompt": "test prompt"})

    @pytest.mark.respx(base_url=base_url)
    def test_run_with_file_output_iterator(self, respx_mock: MockRouter) -> None:
        """Test run with file output iterator."""
        # Mock URLs for file outputs
        file_urls = [
            "https://replicate.delivery/output1.png",
            "https://replicate.delivery/output2.png",
            "https://replicate.delivery/output3.png",
        ]

        # Initial response with processing status and no output
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(status="processing", output=None))
        )

        # First poll returns still processing
        respx_mock.get("/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction(status="processing", output=None))
        )

        # Second poll returns success with file URLs
        respx_mock.get("/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction(output=file_urls))
        )

        output: list[FileOutput] = self.client.run("some-model-ref", input={"prompt": "generate file iterator"})

        assert isinstance(output, list)
        assert len(output) == 3
        assert all(isinstance(item, FileOutput) for item in output)
        assert [item.url for item in output] == file_urls


class TestAsyncRun:
    client = AsyncReplicateClient(base_url=base_url, bearer_token=bearer_token, _strict_response_validation=True)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_basic(self, respx_mock: MockRouter) -> None:
        """Test basic async model run functionality."""
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = await self.client.run("some-model-ref", input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_wait_true(self, respx_mock: MockRouter) -> None:
        """Test async run with wait=True parameter."""
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = await self.client.run("some-model-ref", wait=True, input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_wait_int(self, respx_mock: MockRouter) -> None:
        """Test async run with wait as an integer value."""
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = await self.client.run("some-model-ref", wait=10, input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_without_wait(self, respx_mock: MockRouter) -> None:
        """Test async run with wait=False parameter."""
        # Initial prediction state is "processing"
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(status="processing"))
        )

        # When we wait for it, it becomes "succeeded"
        respx_mock.get("/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction(status="succeeded"))
        )

        output: Any = await self.client.run("some-model-ref", wait=False, input={"prompt": "test prompt"})

        assert output == "test output"

    @pytest.mark.respx(base_url=base_url, assert_all_mocked=False)
    async def test_async_run_with_file_output(self, respx_mock: MockRouter) -> None:
        """Test async run with file output."""
        # Mock prediction with file URL output
        file_url = "https://replicate.delivery/output.png"
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(output=file_url))
        )

        output: Any = await self.client.run("some-model-ref", input={"prompt": "generate image"})

        assert isinstance(output, AsyncFileOutput)
        assert output.url == file_url

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_file_list_output(self, respx_mock: MockRouter) -> None:
        """Test async run with list of file outputs."""
        # Create a mock prediction response with a list of file URLs
        file_urls = ["https://replicate.delivery/output1.png", "https://replicate.delivery/output2.png"]
        mock_prediction = create_mock_prediction()
        mock_prediction["output"] = file_urls

        # Mock the endpoint
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=mock_prediction))

        output: list[AsyncFileOutput] = await self.client.run(
            "some-model-ref", input={"prompt": "generate multiple images"}
        )

        assert isinstance(output, list)
        assert len(output) == 2
        assert all(isinstance(item, AsyncFileOutput) for item in output)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_dict_file_output(self, respx_mock: MockRouter) -> None:
        """Test async run with dictionary of file outputs."""
        # Mock prediction with dict of file URLs
        file_urls = {
            "image1": "https://replicate.delivery/output1.png",
            "image2": "https://replicate.delivery/output2.png",
        }
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(output=file_urls))
        )

        output: Dict[str, AsyncFileOutput] = await self.client.run(
            "some-model-ref", input={"prompt": "structured output"}
        )

        assert isinstance(output, dict)
        assert len(output) == 2
        assert all(isinstance(item, AsyncFileOutput) for item in output.values())

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_error(self, respx_mock: MockRouter) -> None:
        """Test async run with model error."""
        # Mock prediction with error
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(status="failed", error="Model error occurred"))
        )

        with pytest.raises(ModelError):
            await self.client.run("error-model-ref", input={"prompt": "trigger error"})

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_base64_file(self, respx_mock: MockRouter) -> None:
        """Test async run with base64 encoded file input."""
        # Create a simple file-like object
        file_obj = io.BytesIO(b"test content")

        # Mock the prediction response
        respx_mock.post("/predictions").mock(return_value=httpx.Response(201, json=create_mock_prediction()))

        output: Any = await self.client.run("some-model-ref", input={"file": file_obj})

        assert output == "test output"

    async def test_async_run_with_prefer_conflict(self) -> None:
        """Test async run with conflicting wait and prefer parameters."""
        with pytest.raises(TypeError, match="cannot mix and match prefer and wait"):
            await self.client.run("some-model-ref", wait=True, prefer="nowait", input={"prompt": "test"})

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_iterator(self, respx_mock: MockRouter) -> None:
        """Test async run with an iterator output."""
        # Create a mock prediction with an iterator output
        output_iterator = ["chunk1", "chunk2", "chunk3"]
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(output=output_iterator))
        )

        output: list[str] = await self.client.run("some-model-ref", input={"prompt": "generate iterator"})

        assert isinstance(output, list)
        assert len(output) == 3
        assert output == output_iterator

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_invalid_identifier(self, respx_mock: MockRouter) -> None:
        """Test async run with an invalid model identifier."""
        # Mock a 404 response for an invalid model identifier
        respx_mock.post("/predictions").mock(return_value=httpx.Response(404, json={"detail": "Model not found"}))

        with pytest.raises(NotFoundError):
            await self.client.run("invalid-model-ref", input={"prompt": "test prompt"})

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_invalid_cog_version(self, respx_mock: MockRouter) -> None:
        """Test async run with an invalid Cog version."""
        # Mock an error response for an invalid Cog version
        respx_mock.post("/predictions").mock(return_value=httpx.Response(400, json={"detail": "Invalid Cog version"}))

        with pytest.raises(BadRequestError):
            await self.client.run("model-with-invalid-cog", input={"prompt": "test prompt"})

    @pytest.mark.respx(base_url=base_url)
    async def test_async_run_with_file_output_iterator(self, respx_mock: MockRouter) -> None:
        """Test async run with file output iterator."""
        # Mock URLs for file outputs
        file_urls = [
            "https://replicate.delivery/output1.png",
            "https://replicate.delivery/output2.png",
            "https://replicate.delivery/output3.png",
        ]

        # Initial response with processing status and no output
        respx_mock.post("/predictions").mock(
            return_value=httpx.Response(201, json=create_mock_prediction(status="processing", output=None))
        )

        # First poll returns still processing
        respx_mock.get("/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction(status="processing", output=None))
        )

        # Second poll returns success with file URLs
        respx_mock.get("/predictions/test_prediction_id").mock(
            return_value=httpx.Response(200, json=create_mock_prediction(output=file_urls))
        )

        output: list[AsyncFileOutput] = await self.client.run(
            "some-model-ref", input={"prompt": "generate file iterator"}
        )

        assert isinstance(output, list)
        assert len(output) == 3
        assert all(isinstance(item, AsyncFileOutput) for item in output)
        assert [item.url for item in output] == file_urls
