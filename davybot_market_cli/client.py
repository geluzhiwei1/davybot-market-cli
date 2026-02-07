"""DavyBot Market SDK Client."""

import os
import urllib.parse
import httpx
from typing import Any
from pathlib import Path

from .exceptions import (
    DavybotMarketError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    APIError,
)


class DavybotMarketClient:
    """Client for DavyBot Market API.

    Example usage:

        with DavybotMarketClient() as client:
            # Search resources
            results = client.search("web scraping")

            # List skills
            skills = client.list_skills()

            # Get resource details
            skill = client.get_skill("abc123")

            # Download resource
            client.download("skill", "abc123", "./downloads")
    """

    def _encode_resource_id(self, resource_id: str) -> str:
        """URL-encode resource ID to handle slashes and special characters.

        Args:
            resource_id: Resource ID that may contain slashes

        Returns:
            URL-encoded resource ID
        """
        return urllib.parse.quote(resource_id, safe="")

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ):
        """Initialize the client.

        Args:
            base_url: API base URL (defaults to http://localhost:8000/api/v1)
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = (
            base_url or os.environ.get("DAVYBOT_API_URL", "http://localhost:8000/api/v1")
        ).rstrip("/")
        self.api_key = api_key or os.environ.get("DAVYBOT_API_KEY")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    def __enter__(self):
        """Enter context manager."""
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_headers(),
            verify=self.verify_ssl,
        )
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        if self._client:
            self._client.close()

    async def __aenter__(self):
        """Enter async context manager."""
        self._async_client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_headers(),
            verify=self.verify_ssl,
        )
        return self

    async def __aexit__(self, *args):
        """Exit async context manager."""
        if self._async_client:
            await self._async_client.aclose()

    def _get_client(self) -> httpx.Client:
        """Get or create sync client."""
        if not self._client:
            raise RuntimeError(
                "Client not initialized. Use 'with DavybotMarketClient() as client:'"
            )
        return self._client

    async def _get_async_client(self) -> httpx.AsyncClient:
        """Get or create async client."""
        if not self._async_client:
            raise RuntimeError(
                "Async client not initialized. Use 'async with DavybotMarketClient() as client:'"
            )
        return self._async_client

    def _get_headers(self) -> dict[str, str]:
        """Get request headers."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    # Health check
    def health(self) -> dict[str, Any]:
        """Check API health.

        Returns:
            Health status
        """
        client = self._get_client()
        url = self.base_url.replace("/api/v1", "") + "/health"
        response = client.get(url)
        response.raise_for_status()
        return response.json()

    # Search
    def search(
        self,
        query: str,
        resource_type: str | None = None,
        tags: list[str] | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search for resources.

        Args:
            query: Search query
            resource_type: Optional resource type filter
            tags: Optional list of tags to filter
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Search results with 'results' and 'total' keys
        """
        client = self._get_client()
        payload = {"query": query, "limit": limit, "offset": offset}
        if resource_type:
            payload["type"] = resource_type
        if tags:
            payload["tags"] = tags

        response = client.post("/search", json=payload)
        self._handle_error(response)
        return response.json()

    # List resources
    def list_skills(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """List all skills.

        Args:
            skip: Number of results to skip
            limit: Maximum number of results

        Returns:
            List of skills with metadata
        """
        return self._list_resources("skill", skip, limit)

    def list_agents(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """List all agents.

        Args:
            skip: Number of results to skip
            limit: Maximum number of results

        Returns:
            List of agents with metadata
        """
        return self._list_resources("agent", skip, limit)

    def list_mcp_servers(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """List all MCP servers.

        Args:
            skip: Number of results to skip
            limit: Maximum number of results

        Returns:
            List of MCP servers with metadata
        """
        return self._list_resources("mcp", skip, limit)

    def list_knowledge_bases(self, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """List all knowledge bases.

        Args:
            skip: Number of results to skip
            limit: Maximum number of results

        Returns:
            List of knowledge bases with metadata
        """
        return self._list_resources("knowledge", skip, limit)

    def _list_resources(self, resource_type: str, skip: int, limit: int) -> dict[str, Any]:
        """Internal method to list resources by type."""
        client = self._get_client()
        response = client.get(f"/{resource_type}s", params={"skip": skip, "limit": limit})
        self._handle_error(response)
        return response.json()

    def _get_resource(self, resource_type: str, resource_id: str) -> dict[str, Any]:
        """Internal method to get resource by type."""
        client = self._get_client()
        encoded_id = self._encode_resource_id(resource_id)
        response = client.get(f"/{resource_type}s/{encoded_id}")
        self._handle_error(response)
        return response.json()

    # Get resource details
    def get_skill(self, resource_id: str) -> dict[str, Any]:
        """Get skill details.

        Args:
            resource_id: Skill ID

        Returns:
            Skill details
        """
        return self._get_resource("skill", resource_id)

    def get_agent(self, resource_id: str) -> dict[str, Any]:
        """Get agent details.

        Args:
            resource_id: Agent ID

        Returns:
            Agent details
        """
        return self._get_resource("agent", resource_id)

    def get_mcp_server(self, resource_id: str) -> dict[str, Any]:
        """Get MCP server details.

        Args:
            resource_id: MCP server ID

        Returns:
            MCP server details
        """
        return self._get_resource("mcp", resource_id)

    def get_knowledge_base(self, resource_id: str) -> dict[str, Any]:
        """Get knowledge base details.

        Args:
            resource_id: Knowledge base ID

        Returns:
            Knowledge base details
        """
        return self._get_resource("knowledge", resource_id)

    # Create resources
    def create_skill(
        self,
        name: str,
        files: dict[str, str],
        description: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new skill.

        Args:
            name: Skill name
            files: Dictionary of filename to content
            description: Optional description
            author: Optional author
            tags: Optional list of tags
            metadata: Optional metadata

        Returns:
            Created skill
        """
        return self._create_resource("skill", name, files, description, author, tags, metadata)

    def create_agent(
        self,
        name: str,
        files: dict[str, str],
        description: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new agent.

        Args:
            name: Agent name
            files: Dictionary of filename to content
            description: Optional description
            author: Optional author
            tags: Optional list of tags
            metadata: Optional metadata

        Returns:
            Created agent
        """
        return self._create_resource("agent", name, files, description, author, tags, metadata)

    def create_mcp_server(
        self,
        name: str,
        files: dict[str, str],
        description: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new MCP server.

        Args:
            name: MCP server name
            files: Dictionary of filename to content
            description: Optional description
            author: Optional author
            tags: Optional list of tags
            metadata: Optional metadata

        Returns:
            Created MCP server
        """
        return self._create_resource("mcp", name, files, description, author, tags, metadata)

    def create_knowledge_base(
        self,
        name: str,
        files: dict[str, str],
        description: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new knowledge base.

        Args:
            name: Knowledge base name
            files: Dictionary of filename to content
            description: Optional description
            author: Optional author
            tags: Optional list of tags
            metadata: Optional metadata

        Returns:
            Created knowledge base
        """
        return self._create_resource("knowledge", name, files, description, author, tags, metadata)

    def _create_resource(
        self,
        resource_type: str,
        name: str,
        files: dict[str, str],
        description: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Internal method to create resource."""
        client = self._get_client()
        payload = {"name": name, "files": files}
        if description:
            payload["description"] = description
        if author:
            payload["author"] = author
        if tags:
            payload["tags"] = tags
        if metadata:
            payload["metadata"] = metadata

        response = client.post(f"/{resource_type}s", json=payload)
        self._handle_error(response)
        return response.json()

    # Download
    def download(
        self,
        resource_type: str,
        resource_id: str,
        output_path: str | Path,
        format: str = "zip",
        version: str | None = None,
    ) -> Path:
        """Download a resource.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            output_path: Output file or directory path
            format: Download format (zip, python)
            version: Optional version to download

        Returns:
            Path to downloaded file
        """
        client = self._get_client()
        params = {"format": format}
        if version:
            params["version"] = version

        encoded_id = self._encode_resource_id(resource_id)
        response = client.get(
            f"/{resource_type}s/{encoded_id}/download",
            params=params,
            follow_redirects=True,
        )
        self._handle_error(response)

        output = Path(output_path)
        if output.is_dir():
            # Get filename from resource
            resource = self._get_resource(resource_type, resource_id)
            name = resource.get("name", "resource")
            ver = resource.get("version", "1.0.0")
            if format == "zip":
                filename = f"{name}-{ver}.zip"
            else:
                filename = f"{name}-{ver}.tar.gz"
            output = output / filename

        output.write_bytes(response.content)
        return output

    # Ratings
    def rate_resource(
        self,
        resource_id: str,
        score: int,
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Rate a resource.

        Args:
            resource_id: Resource ID
            score: Rating score (1-5)
            comment: Optional review comment

        Returns:
            Created rating
        """
        client = self._get_client()
        payload = {"score": score}
        if comment:
            payload["comment"] = comment

        encoded_id = self._encode_resource_id(resource_id)
        response = client.post(f"/resources/{encoded_id}/ratings", json=payload)
        self._handle_error(response)
        return response.json()

    def get_resource_ratings(
        self, resource_id: str, skip: int = 0, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get ratings for a resource.

        Args:
            resource_id: Resource ID
            skip: Number of results to skip
            limit: Maximum number of results

        Returns:
            List of ratings
        """
        client = self._get_client()
        encoded_id = self._encode_resource_id(resource_id)
        response = client.get(
            f"/resources/{encoded_id}/ratings", params={"skip": skip, "limit": limit}
        )
        self._handle_error(response)
        return response.json()

    def get_average_rating(self, resource_id: str) -> dict[str, Any]:
        """Get average rating for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Average rating info
        """
        client = self._get_client()
        encoded_id = self._encode_resource_id(resource_id)
        response = client.get(f"/resources/{encoded_id}/ratings/avg")
        self._handle_error(response)
        return response.json()

    # Similar resources
    def find_similar(self, resource_id: str, limit: int = 10) -> dict[str, Any]:
        """Find similar resources.

        Args:
            resource_id: Resource ID
            limit: Maximum number of results

        Returns:
            Similar resources
        """
        client = self._get_client()
        encoded_id = self._encode_resource_id(resource_id)
        response = client.get(f"/search/similar/{encoded_id}", params={"limit": limit})
        self._handle_error(response)
        return response.json()

    # Update and delete
    def update_resource(
        self,
        resource_type: str,
        resource_id: str,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a resource.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            name: New name
            description: New description
            tags: New tags
            metadata: New metadata

        Returns:
            Updated resource
        """
        client = self._get_client()
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags
        if metadata is not None:
            payload["metadata"] = metadata

        encoded_id = self._encode_resource_id(resource_id)
        response = client.put(f"/{resource_type}s/{encoded_id}", json=payload)
        self._handle_error(response)
        return response.json()

    def delete_resource(self, resource_type: str, resource_id: str) -> None:
        """Delete a resource.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID
        """
        client = self._get_client()
        encoded_id = self._encode_resource_id(resource_id)
        response = client.delete(f"/{resource_type}s/{encoded_id}")
        self._handle_error(response)

    # Compatibility aliases for CLI
    def get_resource(self, resource_type: str, resource_id: str) -> dict[str, Any]:
        """Get a specific resource (alias for backward compatibility)."""
        return self._get_resource(resource_type, resource_id)

    def create_resource(
        self,
        resource_type: str,
        name: str,
        files: dict[str, str],
        description: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create/publish a new resource (alias for backward compatibility)."""
        return self._create_resource(
            resource_type, name, files, description, author, tags, metadata
        )

    def download_resource(
        self,
        resource_type: str,
        resource_id: str,
        format: str = "zip",
        version: str | None = None,
        output_dir: Path = Path("."),
    ) -> Path:
        """Download a resource (alias for backward compatibility)."""
        return self.download(resource_type, resource_id, output_dir, format, version)

    def get_similar(self, resource_id: str, limit: int = 10) -> dict[str, Any]:
        """Find similar resources (alias for backward compatibility)."""
        return self.find_similar(resource_id, limit)

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle API errors."""
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed")
        elif response.status_code == 404:
            raise NotFoundError("Resource not found")
        elif response.status_code == 422:
            raise ValidationError("Validation error")
        elif response.status_code >= 400:
            raise APIError(f"API error: {response.status_code}")
        response.raise_for_status()
