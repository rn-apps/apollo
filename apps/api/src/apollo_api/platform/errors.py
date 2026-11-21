"""Domain errors: each carries a stable problem code and HTTP status."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rn_forge.commons import AppException


def _camel(key: str) -> str:
    head, *tail = key.split("_")
    return head + "".join(part.capitalize() for part in tail)


class ApolloError(AppException):
    """Base domain failure: a stable problem code and an HTTP status."""

    code = "internal-error"
    status_code = 500

    def problem_extensions(self) -> Mapping[str, Any]:
        """Publish ``error_data`` as problem extensions, keys camelCased."""
        return {_camel(key): value for key, value in self.error_data.items()}


class NotFoundError(ApolloError):
    """A requested Apollo or beets record does not exist."""

    code = "not-found"
    status_code = 404


class ConflictError(ApolloError):
    """Current state diverges from a validated operation."""

    code = "conflict"
    status_code = 409


class FileMissingError(ConflictError):
    """An indexed media path is absent from disk."""

    code = "file-missing"
    status_code = 409


class WriteFailedError(ApolloError):
    """A file or tag mutation failed after validation."""

    code = "write-failed"
    status_code = 500


class ValidationError(ApolloError):
    """A domain-level input constraint was violated."""

    code = "validation"
    status_code = 422


class ArtworkFetchError(ApolloError):
    """An artwork URL could not be retrieved."""

    code = "artwork-fetch"
    status_code = 502


class ArtworkInvalidImageError(ValidationError):
    """Fetched artwork is not a supported image or exceeds the safety cap."""

    code = "artwork-invalid-image"
    status_code = 422


class JobFailedError(ApolloError):
    """A requested job cannot produce a successful outcome."""

    code = "job-failed"
    status_code = 500


class ICloudSyncActiveError(ConflictError):
    """A destructive action is blocked by Music Sync Library."""

    code = "icloud-sync-active"
    status_code = 409


class InvalidSourceError(ApolloError):
    """An intake source overlaps a path Apollo already manages."""

    code = "invalid-source"
    status_code = 422


class InboxPreviewStaleError(ConflictError):
    """An inbox file changed after promotion was previewed."""

    code = "inbox-preview-stale"
    status_code = 409


class TrimRangeError(ValidationError):
    """Requested trim endpoints do not form a valid range."""

    code = "trim-range"
    status_code = 422


class TrimResultTooShortError(ValidationError):
    """Requested trim would retain less than five seconds."""

    code = "trim-result-too-short"
    status_code = 422


class CapabilityUnavailableError(ApolloError):
    """A feature's required runtime capability is unavailable."""

    code = "capability-unavailable"
    status_code = 409


class InvalidQueryError(ApolloError):
    """A beets query could not be parsed."""

    code = "invalid-query"
    status_code = 422


class PlanStaleError(ConflictError):
    """A plan was made against state that has since changed."""

    code = "plan-stale"
    status_code = 409
