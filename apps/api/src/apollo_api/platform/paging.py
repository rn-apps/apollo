"""Paging shapes for beets-backed lists."""

from __future__ import annotations

from typing import Final

from pydantic import field_validator
from rn_forge.web import WireModel

MAX_LIMIT: Final = 500
"""The largest page an offset list serves."""


class OffsetPage[T](WireModel):
    """One page of a beets-backed list: a window and the full count."""

    items: list[T]
    offset: int
    limit: int
    total: int

    @field_validator("limit")
    @classmethod
    def _clamp_limit(cls, value: int) -> int:
        return min(value, MAX_LIMIT)
