"""Clerk authentication for the codice-fiscale API.

Delegates JWT verification to aecs4u-auth, which handles JWKS caching,
clock-drift tolerance, and proper signature verification — replacing the
previous implementation that skipped signature verification entirely.
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status

from aecs4u_auth import (
    get_current_clerk_user,
    get_current_clerk_user_optional,
)


def _to_dict(clerk_user) -> dict[str, Any]:
    """Map ClerkUser to the dict shape expected by route handlers."""
    return {
        "sub": clerk_user.id,
        "email": clerk_user.email,
        "name": clerk_user.full_name,
        "given_name": clerk_user.first_name,
        "family_name": clerk_user.last_name,
    }


async def clerk_auth(request: Request) -> dict[str, Any]:
    """FastAPI dependency: require a valid Clerk JWT, return user dict."""
    clerk_user = await get_current_clerk_user(request)
    return _to_dict(clerk_user)


async def optional_clerk_auth(request: Request) -> dict[str, Any]:
    """FastAPI dependency: return user dict if authenticated, empty dict otherwise."""
    clerk_user = await get_current_clerk_user_optional(request)
    if not clerk_user:
        return {}
    return _to_dict(clerk_user)


def get_user_metadata(auth_data: dict[str, Any]) -> dict[str, Any]:
    """Extract structured user info from the auth dict returned by dependencies."""
    return {
        "user_id": auth_data.get("sub"),
        "email": auth_data.get("email"),
        "name": auth_data.get("name"),
        "given_name": auth_data.get("given_name"),
        "family_name": auth_data.get("family_name"),
        "created_at": auth_data.get("created_at"),
        "updated_at": auth_data.get("updated_at"),
    }
