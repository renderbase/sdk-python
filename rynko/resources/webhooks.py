"""
Webhooks Resource

Provides read-only access to webhook subscriptions.
Webhook subscriptions are managed through the Rynko dashboard.
"""

from typing import Any, Dict

from ..http import HttpClient, AsyncHttpClient


class WebhooksResource:
    """Synchronous webhooks resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a webhook subscription by ID."""
        response = self._http.get(f"/api/v1/webhook-subscriptions/{webhook_id}")
        return response.get("data", response)

    def list(self) -> Dict[str, Any]:
        """List all webhook subscriptions."""
        return self._http.get("/api/v1/webhook-subscriptions")


class AsyncWebhooksResource:
    """Asynchronous webhooks resource."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a webhook subscription by ID (async)."""
        response = await self._http.get(f"/api/v1/webhook-subscriptions/{webhook_id}")
        return response.get("data", response)

    async def list(self) -> Dict[str, Any]:
        """List all webhook subscriptions (async)."""
        return await self._http.get("/api/v1/webhook-subscriptions")
