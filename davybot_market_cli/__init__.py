"""DavyBot Market - CLI and SDK for AI Agent Resources."""
__version__ = "0.1.0"

# SDK Client
from .client import DavybotMarketClient

# Data Models
from .models import (
    Resource,
    Skill,
    Agent,
    McpServer,
    KnowledgeBase,
    Rating,
    AverageRating,
    Review,
    SearchResult,
    ResourceListResponse,
)

# Exceptions
from .exceptions import (
    DavybotMarketError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    APIError,
    ConnectionError,
    DownloadError,
)

# Shared Types
from .types import (
    # Analytics
    AnalyticsEvent,
    SystemMetrics,
    AnalyticsSettings,
    AnalyticsSummary,
    # Feedback
    FeedbackType,
    FeedbackStatus,
    Feedback,
    FeedbackResponse,
    FeedbackListResponse,
    # Sync
    SyncConfiguration,
    SyncStatus,
    SyncConflict,
)

__all__ = [
    # SDK Client
    "DavybotMarketClient",
    # Data Models
    "Resource",
    "Skill",
    "Agent",
    "McpServer",
    "KnowledgeBase",
    "Rating",
    "AverageRating",
    "Review",
    "SearchResult",
    "ResourceListResponse",
    # Exceptions
    "DavybotMarketError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "APIError",
    "ConnectionError",
    "DownloadError",
    # Shared Types - Analytics
    "AnalyticsEvent",
    "SystemMetrics",
    "AnalyticsSettings",
    "AnalyticsSummary",
    # Shared Types - Feedback
    "FeedbackType",
    "FeedbackStatus",
    "Feedback",
    "FeedbackResponse",
    "FeedbackListResponse",
    # Shared Types - Sync
    "SyncConfiguration",
    "SyncStatus",
    "SyncConflict",
]
