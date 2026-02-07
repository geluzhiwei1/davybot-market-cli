"""Utility functions for CLI."""

import os
from typing import Tuple, Optional
from .client import DavybotMarketClient


def get_api_client() -> DavybotMarketClient:
    """Get configured API client.

    Returns:
        Configured DavybotMarketClient instance
    """
    base_url = os.environ.get("DAVYBOT_API_URL", "http://localhost:8000/api/v1")
    return DavybotMarketClient(base_url=base_url)


def parse_resource_uri(uri: str) -> Tuple[Optional[str], str]:
    """Parse a resource URI.

    Supported formats:
    - type://name (e.g., skill://web-scraper)
    - type:name (e.g., skill:web-scraper)
    - id (e.g., abc123-def456)

    Args:
        uri: Resource URI

    Returns:
        Tuple of (resource_type, resource_id_or_name)
    """
    if "://" in uri:
        # Format: type://name
        resource_type, resource_id = uri.split("://", 1)
        return resource_type, resource_id
    elif ":" in uri and len(uri.split(":")[0]) in ["skill", "agent", "mcp", "knowledge"]:
        # Format: type:name
        resource_type, resource_id = uri.split(":", 1)
        return resource_type, resource_id
    else:
        # Assume it's an ID or name without type
        return None, uri


def format_resource(resource: dict) -> str:
    """Format a resource for display.

    Args:
        resource: Resource dictionary

    Returns:
        Formatted string
    """
    lines = [
        f"Name: {resource['name']}",
        f"Type: {resource['type']}",
        f"Version: {resource['version']}",
    ]

    if resource.get("description"):
        lines.append(f"Description: {resource['description'][:100]}...")

    lines.append(f"Rating: {resource['rating']:.1f} | Downloads: {resource['downloads']}")

    if resource.get("tags"):
        lines.append(f"Tags: {', '.join(resource['tags'][:5])}")

    return "\n".join(lines)
