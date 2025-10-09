#!/usr/bin/env python3
"""
Script to generate API.md documentation from OpenAPI spec with code samples.
"""

from __future__ import annotations

import re
import sys
import json
import tempfile
import subprocess
from typing import Any
from pathlib import Path


def download_openapi_spec() -> dict[str, Any]:
    """Download and parse the OpenAPI spec from Stainless."""
    import urllib.request

    spec_url = "https://app.stainless.com/api/spec/documented/replicate-client/openapi.documented.yml"

    print(f"Downloading OpenAPI spec from {spec_url}...")

    with urllib.request.urlopen(spec_url) as response:
        yaml_content = response.read().decode("utf-8")

    # Save to temp file to dereference it
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        # Try to use swagger-cli if available to dereference
        result = subprocess.run(
            ["npx", "@apidevtools/swagger-cli", "bundle", temp_path, "--dereference", "--type", "json"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            spec = json.loads(result.stdout)
            print("Successfully dereferenced OpenAPI spec using swagger-cli")
        else:
            # Fallback to PyYAML
            import yaml

            with open(temp_path, "r") as f:
                spec = yaml.safe_load(f)
            print("Loaded OpenAPI spec using PyYAML (not dereferenced)")
    finally:
        Path(temp_path).unlink(missing_ok=True)

    return spec


def extract_operation_id(path: str, method: str, operation: dict[str, Any]) -> str:
    """Extract operation ID from operation object."""
    if "operationId" in operation:
        return operation["operationId"]

    # Fallback: generate from path and method
    # Convert path like /models/{model_owner}/{model_name} to models_get
    clean_path = path.strip("/").replace("{", "").replace("}", "").replace("/", "_")
    return f"{clean_path}_{method}"


def remove_client_instantiation(code: str) -> str:
    """Remove client instantiation code from examples."""
    # Pattern to match Replicate client instantiation
    patterns = [
        # Multi-line instantiation
        r"replicate\s*=\s*Replicate\s*\([^)]*\)\s*\n",
        # Single-line instantiation
        r"replicate\s*=\s*Replicate\s*\([^)]*\)",
        # Import and instantiation in one
        r"from replicate import Replicate\s*\n",
        r"import replicate\s*\n\s*replicate\s*=\s*Replicate\s*\([^)]*\)\s*\n?",
        # Client with bearer_token
        r'client\s*=\s*replicate\.Replicate\s*\(\s*bearer_token\s*=\s*"[^"]*"\s*\)\s*\n?',
        r'replicate\s*=\s*replicate\.Replicate\s*\(\s*bearer_token\s*=\s*"[^"]*"\s*\)\s*\n?',
    ]

    cleaned = code
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.MULTILINE)

    # Clean up extra blank lines at the start
    lines = cleaned.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)

    return "\n".join(lines)


def format_operation(operation_id: str, operation: dict[str, Any]) -> str:
    """Format a single operation as markdown."""
    summary = operation.get("summary", "").strip()

    # Extract code sample
    code_sample = ""
    if "x-readme" in operation and "code-samples" in operation["x-readme"]:
        samples = operation["x-readme"]["code-samples"]
        # Look for Python sample
        for sample in samples:
            if sample.get("language") == "python" or sample.get("lang") == "python":
                code = sample.get("code", "")
                code = remove_client_instantiation(code)
                if code:
                    code_sample = f"\n```python\n{code}\n```"
                break

    # Generate docs link
    docs_link = f"https://replicate.com/docs/reference/http#{operation_id}"

    # Build the markdown section
    lines = [f"### `{operation_id}`", ""]

    if summary:
        lines.append(summary)
        lines.append("")

    if code_sample:
        lines.append(code_sample)
        lines.append("")

    lines.append(f"Docs: {docs_link}")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def get_ordered_operations(spec: dict[str, Any]) -> list[tuple[str, str, str, dict[str, Any]]]:
    """Get operations in the specified order."""
    # Specified order from the Linear issue
    operation_order = [
        "search",
        "predictions.create",
        "predictions.get",
        "predictions.list",
        "predictions.cancel",
        "models.create",
        "models.get",
        "models.list",
        "models.search",
        "models.delete",
        "models.examples.list",
        "models.predictions.create",
        "models.readme.get",
        "models.versions.get",
        "models.versions.list",
        "models.versions.delete",
        "collections.get",
        "collections.list",
        "deployments.create",
        "deployments.get",
        "deployments.list",
        "deployments.update",
        "deployments.delete",
        "deployments.predictions.create",
        "files.list",
        "files.create",
        "files.delete",
        "files.get",
        "files.download",
        "trainings.create",
        "trainings.get",
        "trainings.list",
        "trainings.cancel",
        "hardware.list",
        "account.get",
        "webhooks.default.secret.get",
    ]

    operations: dict[str, tuple[str, str, str, dict[str, Any]]] = {}

    # Extract all operations from paths
    for path, path_obj in spec.get("paths", {}).items():
        for method in ["get", "post", "put", "patch", "delete"]:
            if method in path_obj:
                operation = path_obj[method]
                op_id = extract_operation_id(path, method, operation)

                # Try to match with our ordered list using multiple strategies
                matched_name = None

                # Strategy 1: Direct operationId match
                if op_id in operation_order:
                    matched_name = op_id

                # Strategy 2: Case-insensitive exact match
                if not matched_name:
                    for ordered_name in operation_order:
                        if op_id.lower() == ordered_name.lower():
                            matched_name = ordered_name
                            break

                # Strategy 3: Convert ordered name to possible operation IDs
                if not matched_name:
                    for ordered_name in operation_order:
                        # e.g., "predictions.create" might be "predictionsCreate" or "predictions_create"
                        variants = [
                            ordered_name.replace(".", "_"),
                            ordered_name.replace(".", ""),
                            "".join(word.capitalize() if i > 0 else word for i, word in enumerate(ordered_name.split("."))),
                        ]

                        if op_id in variants or any(v.lower() == op_id.lower() for v in variants):
                            matched_name = ordered_name
                            break

                # Strategy 4: Match by path structure and method
                if not matched_name:
                    for ordered_name in operation_order:
                        ordered_parts = ordered_name.split(".")
                        if len(ordered_parts) >= 2:
                            resource = ordered_parts[0]
                            action = ordered_parts[-1]

                            # Check various path patterns
                            path_lower = path.lower()
                            if (resource in path_lower and
                                ((action == "create" and method == "post") or
                                 (action == "get" and method == "get" and "{" in path) or
                                 (action == "list" and method == "get" and "{" not in path) or
                                 (action == "update" and method in ["put", "patch"]) or
                                 (action == "delete" and method == "delete") or
                                 (action == "cancel" and method == "post" and "cancel" in path) or
                                 (action == "search" and method == "get" and "search" in path))):
                                matched_name = ordered_name
                                break

                key = matched_name or op_id
                operations[key] = (op_id, path, method, operation)

    # Order operations according to the specified list
    ordered = []
    added_keys = set()

    for name in operation_order:
        if name in operations:
            ordered.append(operations[name])
            added_keys.add(name)

    # Add any remaining operations not in the ordered list
    for key, value in operations.items():
        if key not in added_keys:
            ordered.append(value)

    return ordered


def generate_api_docs(spec: dict[str, Any]) -> str:
    """Generate the API operations documentation."""
    lines = []
    operations = get_ordered_operations(spec)

    # Generate sorted list of operations at the top
    lines.append("Available operations:")
    lines.append("")
    for op_id, _path, _method, _operation in operations:
        # Create anchor link from operation_id
        anchor = op_id.lower().replace('.', '').replace('_', '')
        lines.append(f"- [`{op_id}`](#{anchor})")
    lines.append("")

    # Generate detailed documentation for each operation
    for op_id, _path, _method, operation in operations:
        lines.append(format_operation(op_id, operation))

    return "\n".join(lines)


def update_api_md():
    """Main function to update api.md file."""
    # Paths
    project_root = Path(__file__).parent.parent.parent
    template_path = project_root / "api-template.md"
    output_path = project_root / "api.md"

    # Download and parse OpenAPI spec
    try:
        spec = download_openapi_spec()
    except Exception as e:
        print(f"Error downloading OpenAPI spec: {e}", file=sys.stderr)
        sys.exit(1)

    # Read template
    if not template_path.exists():
        print(f"Template file not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    with open(template_path, "r") as f:
        template_content = f.read()

    # Generate API operations documentation
    api_docs = generate_api_docs(spec)

    # Replace placeholder in template
    if "<!-- API_OPERATIONS -->" not in template_content:
        print("Warning: <!-- API_OPERATIONS --> placeholder not found in template", file=sys.stderr)
        final_content = template_content + "\n\n" + api_docs
    else:
        final_content = template_content.replace("<!-- API_OPERATIONS -->", api_docs)

    # Write output
    with open(output_path, "w") as f:
        f.write(final_content)

    print(f"Successfully updated {output_path}")


if __name__ == "__main__":
    update_api_md()
