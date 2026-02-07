"""
Shared Type Definitions for Feedback
Feedback 相关的共享类型定义
"""

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class FeedbackType(str, Enum):
    """反馈类型"""

    BUG = "bug"
    FEATURE = "feature"
    QUESTION = "question"
    USABILITY = "usability"
    PERFORMANCE = "performance"
    OTHER = "other"


class FeedbackStatus(str, Enum):
    """反馈状态"""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Feedback(BaseModel):
    """用户反馈"""

    id: str = Field(..., description="反馈 ID")
    type: FeedbackType = Field(..., description="反馈类型")
    title: str = Field(..., min_length=1, max_length=500, description="标题")
    description: str = Field(..., min_length=1, description="详细描述")
    email: str | None = Field(None, description="联系邮箱")

    # 自动附加信息
    systemInfo: dict = Field(default_factory=dict, description="系统信息")
    appLogs: list[str] = Field(default_factory=list, description="应用日志")
    screenshots: list[str] = Field(default_factory=list, description="截图（Base64）")

    # 可选信息
    reproductionSteps: list[str] | None = Field(None, description="重现步骤")
    userId: str | None = Field(None, description="用户 ID")

    # 元数据
    timestamp: str = Field(..., description="提交时间")
    status: FeedbackStatus = Field(default=FeedbackStatus.OPEN, description="状态")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "fb_123",
                "type": "bug",
                "title": "应用崩溃",
                "description": "点击生成代码按钮后应用闪退",
                "email": "user@example.com",
                "systemInfo": {
                    "appVersion": "1.0.0",
                    "platform": "linux",
                },
                "appLogs": ["ERROR: Something went wrong"],
                "screenshots": [],
                "reproductionSteps": [
                    "打开应用",
                    "点击生成代码",
                    "应用崩溃",
                ],
                "timestamp": "2025-01-22T10:00:00Z",
                "status": "open",
            }
        }
    )


class FeedbackResponse(BaseModel):
    """反馈提交响应"""

    success: bool = Field(..., description="是否成功")
    feedbackId: str = Field(..., description="反馈 ID")
    message: str = Field(default="感谢您的反馈！", description="响应消息")


class FeedbackListResponse(BaseModel):
    """反馈列表响应"""

    total: int = Field(..., description="总数")
    items: list[Feedback] = Field(..., description="反馈列表")
