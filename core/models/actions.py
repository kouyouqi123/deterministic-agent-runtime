"""Action and action result models."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from core.models.state import Position


class ActionType(str, Enum):
    """Available agent actions."""

    MOVE = "move"
    ATTACK = "attack"
    RETREAT = "retreat"
    WAIT = "wait"
    SCAN = "scan"


class Action(BaseModel):
    """What the agent wants to do."""

    action_type: ActionType
    target: Position | None = None
    reason: str = ""


class ActionResult(BaseModel):
    """What happened when the agent tried an action."""

    action: Action
    success: bool
    message: str = ""
    energy_cost: int = Field(default=0, ge=0)
    tick: int = 0
