"""Data models for DavyBot Market SDK."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Resource:
    """Base resource model."""

    id: str
    name: str
    type: str = ""  # Default value, overridden by subclasses
    description: str | None = None
    author: str | None = None
    version: str = "1.0.0"
    tags: list[str] = field(default_factory=list)
    extra_metadata: dict[str, object] = field(default_factory=dict)
    downloads: int = 0
    rating: float = 0.0
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Resource":
        """Create from API response dictionary.

        Args:
            data: API response data

        Returns:
            Resource instance
        """
        # Handle datetime fields
        created_at_val = data.get("created_at")
        if created_at_val and isinstance(created_at_val, str):
            data["created_at"] = datetime.fromisoformat(created_at_val.replace("Z", "+00:00"))
        updated_at_val = data.get("updated_at")
        if updated_at_val and isinstance(updated_at_val, str):
            data["updated_at"] = datetime.fromisoformat(updated_at_val.replace("Z", "+00:00"))

        # Map metadata field
        if "metadata" in data and "extra_metadata" not in data:
            data["extra_metadata"] = data.pop("metadata", {})

        return cls(**data)  # type: ignore[arg-type]


@dataclass
class Skill(Resource):
    """Skill resource model."""

    type: str = "skill"


@dataclass
class Agent(Resource):
    """Agent resource model."""

    type: str = "agent"


@dataclass
class McpServer(Resource):
    """MCP Server resource model."""

    type: str = "mcp"


@dataclass
class KnowledgeBase(Resource):
    """Knowledge Base resource model."""

    type: str = "knowledge"


@dataclass
class Rating:
    """Rating model."""

    id: str
    resource_id: str
    user_id: str
    score: int
    comment: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Rating":
        """Create from API response dictionary."""
        created_at_val = data.get("created_at")
        if created_at_val and isinstance(created_at_val, str):
            data["created_at"] = datetime.fromisoformat(created_at_val.replace("Z", "+00:00"))
        updated_at_val = data.get("updated_at")
        if updated_at_val and isinstance(updated_at_val, str):
            data["updated_at"] = datetime.fromisoformat(updated_at_val.replace("Z", "+00:00"))
        return cls(**data)  # type: ignore[arg-type]


@dataclass
class AverageRating:
    """Average rating model."""

    resource_id: str
    average_rating: float
    total_ratings: int
    rating_distribution: dict[int, int] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "AverageRating":
        """Create from API response dictionary."""
        return cls(**data)  # type: ignore[arg-type]


@dataclass
class Review:
    """Review model."""

    id: str
    resource_id: str
    user_id: str
    content: str
    rating_id: str | None = None
    created_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Review":
        """Create from API response dictionary."""
        created_at_val = data.get("created_at")
        if created_at_val and isinstance(created_at_val, str):
            data["created_at"] = datetime.fromisoformat(created_at_val.replace("Z", "+00:00"))
        return cls(**data)  # type: ignore[arg-type]


@dataclass
class SearchResult:
    """Search result model."""

    results: list[Resource]
    total: int
    query: str

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SearchResult":
        """Create from API response dictionary."""
        results_val = data.get("results")
        results_list: list[object] = []
        if isinstance(results_val, list):
            results_list = results_val
        results = []
        for r in results_list:
            if isinstance(r, dict):
                results.append(Resource.from_dict(r))
            else:
                results.append(Resource.from_dict({}))  # type: ignore[arg-type]
        total_val = data.get("total", 0)
        total = int(total_val) if isinstance(total_val, (int, str)) else 0
        query_val = data.get("query", "")
        query = str(query_val) if query_val else ""
        return cls(results=results, total=total, query=query)


@dataclass
class ResourceListResponse:
    """Resource list response model."""

    items: list[Resource]
    total: int
    page: int
    page_size: int

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ResourceListResponse":
        """Create from API response dictionary."""
        items_val = data.get("items")
        items_list: list[object] = []
        if isinstance(items_val, list):
            items_list = items_val
        items = []
        for r in items_list:
            if isinstance(r, dict):
                items.append(Resource.from_dict(r))
            else:
                items.append(Resource.from_dict({}))  # type: ignore[arg-type]
        total_val = data.get("total", 0)
        total = int(total_val) if isinstance(total_val, (int, str)) else 0
        page_val = data.get("page", 1)
        page = int(page_val) if isinstance(page_val, (int, str)) else 1
        page_size_val = data.get("page_size", 20)
        page_size = int(page_size_val) if isinstance(page_size_val, (int, str)) else 20
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
