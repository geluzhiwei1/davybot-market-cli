"""
Shared Type Definitions for Sync
Sync 相关的共享类型定义
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Any
from datetime import datetime, timezone


class SyncConfiguration(BaseModel):
    """同步配置"""

    # 用户偏好设置
    preferences: dict[str, Any] = Field(
        default_factory=dict,
        description="用户偏好（主题、语言、字体等）",
    )

    # Agent 配置
    agentSettings: dict[str, Any] = Field(
        default_factory=dict,
        description="Agent 设置（默认模式、模型等）",
    )

    # Workspace 配置
    workspaceSettings: dict[str, Any] = Field(
        default_factory=dict,
        description="工作区设置",
    )

    # 工具配置
    toolSettings: dict[str, Any] = Field(
        default_factory=dict,
        description="工具配置",
    )

    # 快捷键
    keybindings: dict[str, str] = Field(
        default_factory=dict,
        description="快捷键设置",
    )

    # 元数据
    lastSyncTime: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="最后同步时间",
    )
    version: str = Field(default="1.0.0", description="配置版本")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "preferences": {
                    "theme": "dark",
                    "language": "zh-CN",
                    "fontSize": 14,
                },
                "agentSettings": {
                    "defaultMode": "code",
                    "defaultModel": "deepseek/deepseek-chat",
                    "temperature": 0.7,
                },
                "workspaceSettings": {
                    "autoSave": True,
                    "checkpointFrequency": 5,
                },
                "toolSettings": {
                    "enabledTools": [],
                },
                "keybindings": {},
                "lastSyncTime": "2025-01-22T10:00:00Z",
                "version": "1.0.0",
            }
        }
    )


class SyncStatus(BaseModel):
    """同步状态"""

    enabled: bool = Field(..., description="是否启用同步")
    lastSyncTime: str | None = Field(None, description="最后同步时间")
    status: str = Field(..., description="同步状态 (synced, syncing, error)")
    errorMessage: str | None = Field(None, description="错误消息")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enabled": True,
                "lastSyncTime": "2025-01-22T10:00:00Z",
                "status": "synced",
                "errorMessage": None,
            }
        }
    )


class SyncConflict(BaseModel):
    """同步冲突"""

    key: str = Field(..., description="冲突的配置键")
    localValue: Any = Field(..., description="本地值")
    remoteValue: Any = Field(..., description="远程值")
    localTimestamp: str = Field(..., description="本地更新时间")
    remoteTimestamp: str = Field(..., description="远程更新时间")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "key": "preferences.theme",
                "localValue": "dark",
                "remoteValue": "light",
                "localTimestamp": "2025-01-22T10:00:00Z",
                "remoteTimestamp": "2025-01-22T09:00:00Z",
            }
        }
    )
