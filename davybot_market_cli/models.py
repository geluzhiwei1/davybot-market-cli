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
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))  # type: ignore[arg-type]
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))  # type: ignore[arg-type]

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
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))  # type: ignore[arg-type]
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))  # type: ignore[arg-type]
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
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))  # type: ignore[arg-type]
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
        results = [Resource.from_dict(r) for r in data.get("results", [])]  # type: ignore[list-item]
        return cls(results=results, total=data.get("total", 0), query=data.get("query", ""))  # type: ignore[arg-type]


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
        items = [Resource.from_dict(r) for r in data.get("items", [])]  # type: ignore[list-item]
        return cls(
            items=items,
            total=data.get("total", 0),  # type: ignore[arg-type]
            page=data.get("page", 1),  # type: ignore[arg-type]
            page_size=data.get("page_size", 20),  # type: ignore[arg-type]
        )
