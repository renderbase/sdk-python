"""
Webhooks Resource
"""

from typing import Any, Dict, List, Optional

from ..http import HttpClient, AsyncHttpClient


class WebhooksResource:
    """Synchronous webhooks resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def create(
        self,
        url: str,
        events: List[str],
        *,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a webhook subscription.

        Args:
            url: Webhook endpoint URL
            events: List of event types to subscribe to (document.generated, document.failed, document.downloaded)
            description: Webhook description (optional)

        Returns:
            Webhook subscription with secret

        Example:
            >>> webhook = client.webhooks.create(
            ...     url="https://your-app.com/webhooks/renderbase",
            ...     events=["document.generated", "document.failed"],
            ...     description="My Webhook"
            ... )
            >>> print(f"Secret: {webhook['secret']}")
        """
        body: Dict[str, Any] = {
            "url": url,
            "events": events,
        }
        if description:
            body["description"] = description

        response = self._http.post("/api/v1/webhook-subscriptions", body)
        return response.get("data", response)

    def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a webhook subscription by ID."""
        response = self._http.get(f"/api/v1/webhook-subscriptions/{webhook_id}")
        return response.get("data", response)

    def list(self) -> Dict[str, Any]:
        """List all webhook subscriptions."""
        return self._http.get("/api/v1/webhook-subscriptions")

    def update(
        self,
        webhook_id: str,
        *,
        events: Optional[List[str]] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Update a webhook subscription.

        Example:
            >>> updated = client.webhooks.update(
            ...     "wh_abc123",
            ...     events=["document.generated", "document.failed"],
            ...     is_active=True
            ... )
        """
        body: Dict[str, Any] = {}
        if events is not None:
            body["events"] = events
        if description is not None:
            body["description"] = description
        if is_active is not None:
            body["isActive"] = is_active

        response = self._http.patch(f"/api/v1/webhook-subscriptions/{webhook_id}", body)
        return response.get("data", response)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook subscription."""
        self._http.delete(f"/api/v1/webhook-subscriptions/{webhook_id}")


class AsyncWebhooksResource:
    """Asynchronous webhooks resource."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def create(
        self,
        url: str,
        events: List[str],
        *,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a webhook subscription (async)."""
        body: Dict[str, Any] = {
            "url": url,
            "events": events,
        }
        if description:
            body["description"] = description

        response = await self._http.post("/api/v1/webhook-subscriptions", body)
        return response.get("data", response)

    async def get(self, webhook_id: str) -> Dict[str, Any]:
        """Get a webhook subscription by ID (async)."""
        response = await self._http.get(f"/api/v1/webhook-subscriptions/{webhook_id}")
        return response.get("data", response)

    async def list(self) -> Dict[str, Any]:
        """List all webhook subscriptions (async)."""
        return await self._http.get("/api/v1/webhook-subscriptions")

    async def update(
        self,
        webhook_id: str,
        *,
        events: Optional[List[str]] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a webhook subscription (async)."""
        body: Dict[str, Any] = {}
        if events is not None:
            body["events"] = events
        if description is not None:
            body["description"] = description
        if is_active is not None:
            body["isActive"] = is_active

        response = await self._http.patch(
            f"/api/v1/webhook-subscriptions/{webhook_id}", body
        )
        return response.get("data", response)

    async def delete(self, webhook_id: str) -> None:
        """Delete a webhook subscription (async)."""
        await self._http.delete(f"/api/v1/webhook-subscriptions/{webhook_id}")
