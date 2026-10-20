"""Uvicorn entry point kept at the backend root for a short launch command."""

from app.main import app, create_app


__all__ = ["app", "create_app"]
