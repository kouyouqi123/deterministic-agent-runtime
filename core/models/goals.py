"""Goal models."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class GoalStatus(str, Enum):
    """Goal lifecycle status."""

    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class Goal(BaseModel):
    """What the agent is trying to achieve."""

    name: str
    description: str = ""
    status: GoalStatus = GoalStatus.ACTIVE
    priority: int = 0
