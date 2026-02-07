"""
Shared Type Definitions
共享类型定义模块
"""

# Analytics Types
from .analytics import (
    AnalyticsEvent,
    SystemMetrics,
    AnalyticsSettings,
    AnalyticsSummary,
)

# Feedback Types
from .feedback import (
    FeedbackType,
    FeedbackStatus,
    Feedback,
    FeedbackResponse,
    FeedbackListResponse,
)

# Sync Types
from .sync import (
    SyncConfiguration,
    SyncStatus,
    SyncConflict,
)

__all__ = [
    # Analytics
    "AnalyticsEvent",
    "SystemMetrics",
    "AnalyticsSettings",
    "AnalyticsSummary",
    # Feedback
    "FeedbackType",
    "FeedbackStatus",
    "Feedback",
    "FeedbackResponse",
    "FeedbackListResponse",
    # Sync
    "SyncConfiguration",
    "SyncStatus",
    "SyncConflict",
]
