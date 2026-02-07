"""
Shared Type Definitions for Analytics
Analytics 相关的共享类型定义
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Any


class AnalyticsEvent(BaseModel):
    """分析事件"""

    eventType: str = Field(..., description="事件类型")
    timestamp: str = Field(..., description="时间戳 (ISO 8601)")
    sessionId: str = Field(..., description="会话 ID")
    userId: str | None = Field(None, description="用户 ID（可选，已 Hash）")
    data: dict[str, Any] = Field(default_factory=dict, description="事件数据")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "eventType": "feature_use",
                "timestamp": "2025-01-22T10:00:00Z",
                "sessionId": "sess_123",
                "userId": "user_hash",
                "data": {
                    "feature": "code_generation",
                    "action": "generate",
                },
            }
        }
    )


class SystemMetrics(BaseModel):
    """系统指标"""

    appVersion: str = Field(..., description="应用版本")
    platform: str = Field(..., description="操作系统平台")
    osVersion: str = Field(..., description="操作系统版本")
    arch: str = Field(..., description="系统架构")
    locale: str = Field(..., description="语言环境")
    theme: str = Field(..., description="主题 (light/dark/auto)")
    cpuCores: int | None = Field(None, description="CPU 核心数")
    totalMemory: int | None = Field(None, description="总内存 (MB)")
    screenResolution: str | None = Field(None, description="屏幕分辨率")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "appVersion": "1.0.0",
                "platform": "linux",
                "osVersion": "Ubuntu 22.04",
                "arch": "x86_64",
                "locale": "zh-CN",
                "theme": "dark",
                "cpuCores": 8,
                "totalMemory": 16384,
            }
        }
    )


class AnalyticsSettings(BaseModel):
    """Analytics 用户设置"""

    enabled: bool = Field(False, description="是否启用 Analytics")
    usageTracking: bool = Field(False, description="是否追踪使用情况")
    errorReporting: bool = Field(True, description="是否报告错误")
    performanceMonitoring: bool = Field(False, description="是否监控性能")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enabled": True,
                "usageTracking": True,
                "errorReporting": True,
                "performanceMonitoring": False,
            }
        }
    )


class AnalyticsSummary(BaseModel):
    """Analytics 摘要"""

    totalEvents: int = Field(..., description="总事件数")
    uniqueSessions: int = Field(..., description="唯一会话数")
    topEvents: dict[str, int] = Field(default_factory=dict, description="最常见的事件")
    errorRate: float = Field(..., description="错误率")
    avgSessionDuration: float | None = Field(None, description="平均会话时长（秒）")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "totalEvents": 1234,
                "uniqueSessions": 56,
                "topEvents": {
                    "feature_use": 456,
                    "session_start": 56,
                    "error": 12,
                },
                "errorRate": 0.0097,
                "avgSessionDuration": 342.5,
            }
        }
    )
