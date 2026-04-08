"""World and agent state models.

These are the authoritative state models. Observed facts only —
no inferred or speculative state mixed in.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Position(BaseModel):
    """2D grid position."""

    x: int = 0
    y: int = 0


class WorldState(BaseModel):
    """Observable environment state (authoritative).

    Contains only observed facts — no inferences or hypotheses.
    """

    tick: int = Field(default=0, description="Current simulation tick")
    width: int = Field(default=10, description="Grid width")
    height: int = Field(default=10, description="Grid height")
    obstacles: list[Position] = Field(default_factory=list)
    threats: list[Position] = Field(default_factory=list)


class AgentState(BaseModel):
    """Agent internal state (authoritative).

    Contains the agent's own state — health, position, inventory.
    """

    position: Position = Field(default_factory=Position)
    health: int = Field(default=100, ge=0, le=100)
    energy: int = Field(default=100, ge=0, le=100)
    alive: bool = True
