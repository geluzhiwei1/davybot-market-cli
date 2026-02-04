"""Data models for DavyBot Market SDK."""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Resource:
    """Base resource model."""

    id: str
    name: str
    type: str = ""  # Default value, overridden by subclasses
    description: Optional[str] = None
    author: Optional[str] = None
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)
    extra_metadata: Dict[str, Any] = field(default_factory=dict)
    downloads: int = 0
    rating: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Resource":
        """Create from API response dictionary.

        Args:
            data: API response data

        Returns:
            Resource instance
        """
        # Handle datetime fields
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))

        # Map metadata field
        if "metadata" in data and "extra_metadata" not in data:
            data["extra_metadata"] = data.pop("metadata", {})

        return cls(**data)


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
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rating":
        """Create from API response dictionary."""
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        return cls(**data)


@dataclass
class AverageRating:
    """Average rating model."""

    resource_id: str
    average_rating: float
    total_ratings: int
    rating_distribution: Dict[int, int] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AverageRating":
        """Create from API response dictionary."""
        return cls(**data)


@dataclass
class Review:
    """Review model."""

    id: str
    resource_id: str
    user_id: str
    content: str
    rating_id: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Review":
        """Create from API response dictionary."""
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        return cls(**data)


@dataclass
class SearchResult:
    """Search result model."""

    results: List[Resource]
    total: int
    query: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """Create from API response dictionary."""
        results = [Resource.from_dict(r) for r in data.get("results", [])]
        return cls(results=results, total=data.get("total", 0), query=data.get("query", ""))


@dataclass
class ResourceListResponse:
    """Resource list response model."""

    items: List[Resource]
    total: int
    page: int
    page_size: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResourceListResponse":
        """Create from API response dictionary."""
        items = [Resource.from_dict(r) for r in data.get("items", [])]
        return cls(
            items=items,
            total=data.get("total", 0),
            page=data.get("page", 1),
            page_size=data.get("page_size", 20),
        )
