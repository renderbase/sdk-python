"""
Documents Resource
"""

import asyncio
import time
from typing import Any, Dict, List, Optional

from ..http import HttpClient, AsyncHttpClient


class DocumentsResource:
    """Synchronous documents resource."""

    def __init__(self, http: HttpClient):
        self._http = http

    def generate(
        self,
        template_id: str,
        format: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a document from a template.

        Args:
            template_id: Template ID to use
            format: Output format ('pdf' or 'excel')
            variables: Template variables for content generation
            workspace_id: Workspace ID to generate document in (optional)
            webhook_url: Webhook URL to receive completion notification
            webhook_secret: Secret for webhook signature verification
            metadata: Custom metadata to pass through to webhook

        Returns:
            Document job with jobId and downloadUrl

        Example:
            >>> result = client.documents.generate(
            ...     template_id="tmpl_invoice",
            ...     format="pdf",
            ...     variables={
            ...         "customerName": "John Doe",
            ...         "invoiceNumber": "INV-001",
            ...         "amount": 150.00,
            ...     }
            ... )
            >>> print(f"Job ID: {result['jobId']}")
            >>> print(f"Download URL: {result['downloadUrl']}")
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "format": format,
        }

        if variables:
            body["variables"] = variables
        if workspace_id:
            body["workspaceId"] = workspace_id
        if webhook_url:
            body["webhookUrl"] = webhook_url
        if webhook_secret:
            body["webhookSecret"] = webhook_secret
        if metadata:
            body["metadata"] = metadata

        response = self._http.post("/api/v1/documents/generate", body)
        return response.get("data", response)

    def generate_pdf(
        self,
        template_id: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a PDF document from a template.

        Example:
            >>> result = client.documents.generate_pdf(
            ...     template_id="tmpl_invoice",
            ...     variables={"invoiceNumber": "INV-001"}
            ... )
        """
        return self.generate(
            template_id=template_id,
            format="pdf",
            variables=variables,
            workspace_id=workspace_id,
            webhook_url=webhook_url,
            webhook_secret=webhook_secret,
            metadata=metadata,
        )

    def generate_excel(
        self,
        template_id: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate an Excel document from a template.

        Example:
            >>> result = client.documents.generate_excel(
            ...     template_id="tmpl_report",
            ...     variables={"reportDate": "2025-01-15"}
            ... )
        """
        return self.generate(
            template_id=template_id,
            format="excel",
            variables=variables,
            workspace_id=workspace_id,
            webhook_url=webhook_url,
            webhook_secret=webhook_secret,
            metadata=metadata,
        )

    def generate_batch(
        self,
        template_id: str,
        format: str,
        documents: List[Dict[str, Any]],
        *,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate multiple documents in a batch.

        Args:
            template_id: Template ID to use
            format: Output format ('pdf' or 'excel')
            documents: List of documents with variables and metadata
            workspace_id: Workspace ID to generate documents in (optional)
            webhook_url: Webhook URL to receive batch completion notification
            webhook_secret: Secret for webhook signature verification

        Example:
            >>> result = client.documents.generate_batch(
            ...     template_id="tmpl_invoice",
            ...     format="pdf",
            ...     documents=[
            ...         {"variables": {"invoiceNumber": "INV-001"}},
            ...         {"variables": {"invoiceNumber": "INV-002"}},
            ...     ]
            ... )
            >>> print(f"Batch ID: {result['batchId']}")
        """
        body: Dict[str, Any] = {
            "templateId": template_id,
            "format": format,
            "documents": documents,
        }

        if workspace_id:
            body["workspaceId"] = workspace_id
        if webhook_url:
            body["webhookUrl"] = webhook_url
        if webhook_secret:
            body["webhookSecret"] = webhook_secret

        response = self._http.post("/api/v1/documents/generate/batch", body)
        return response.get("data", response)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """
        Get a document job by ID.

        Example:
            >>> job = client.documents.get_job("job_abc123")
            >>> if job["status"] == "completed":
            ...     print(f"Download: {job['downloadUrl']}")
        """
        response = self._http.get(f"/api/v1/documents/jobs/{job_id}")
        return response.get("data", response)

    def list_jobs(
        self,
        *,
        status: Optional[str] = None,
        format: Optional[str] = None,
        template_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        List document jobs with optional filters.

        Returns:
            Dict with 'data' (list) and 'meta' (pagination)

        Example:
            >>> result = client.documents.list_jobs(
            ...     status="completed",
            ...     format="pdf",
            ...     limit=10
            ... )
            >>> print(f"Found {result['meta']['total']} jobs")
        """
        params = {
            "status": status,
            "format": format,
            "templateId": template_id,
            "workspaceId": workspace_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": limit,
            "page": page,
        }
        return self._http.get("/api/v1/documents/jobs", params)

    def wait_for_completion(
        self,
        job_id: str,
        *,
        poll_interval: float = 1.0,
        timeout: float = 30.0,
    ) -> Dict[str, Any]:
        """
        Wait for a document job to complete.

        Args:
            job_id: Job ID to wait for
            poll_interval: Time between polls in seconds (default: 1.0)
            timeout: Maximum wait time in seconds (default: 30.0)

        Returns:
            Completed job with downloadUrl

        Raises:
            TimeoutError: If job doesn't complete within timeout

        Example:
            >>> result = client.documents.generate(
            ...     template_id="tmpl_invoice",
            ...     format="pdf",
            ...     variables={"invoiceNumber": "INV-001"}
            ... )
            >>> completed = client.documents.wait_for_completion(result["jobId"])
            >>> print(f"Download: {completed['downloadUrl']}")
        """
        start_time = time.time()

        while True:
            job = self.get_job(job_id)

            if job["status"] in ("completed", "failed"):
                return job

            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for job {job_id} to complete")

            time.sleep(poll_interval)


class AsyncDocumentsResource:
    """Asynchronous documents resource."""

    def __init__(self, http: AsyncHttpClient):
        self._http = http

    async def generate(
        self,
        template_id: str,
        format: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a document from a template (async)."""
        body: Dict[str, Any] = {
            "templateId": template_id,
            "format": format,
        }

        if variables:
            body["variables"] = variables
        if workspace_id:
            body["workspaceId"] = workspace_id
        if webhook_url:
            body["webhookUrl"] = webhook_url
        if webhook_secret:
            body["webhookSecret"] = webhook_secret
        if metadata:
            body["metadata"] = metadata

        response = await self._http.post("/api/v1/documents/generate", body)
        return response.get("data", response)

    async def generate_pdf(
        self,
        template_id: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a PDF document from a template (async)."""
        return await self.generate(
            template_id=template_id,
            format="pdf",
            variables=variables,
            workspace_id=workspace_id,
            webhook_url=webhook_url,
            webhook_secret=webhook_secret,
            metadata=metadata,
        )

    async def generate_excel(
        self,
        template_id: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate an Excel document from a template (async)."""
        return await self.generate(
            template_id=template_id,
            format="excel",
            variables=variables,
            workspace_id=workspace_id,
            webhook_url=webhook_url,
            webhook_secret=webhook_secret,
            metadata=metadata,
        )

    async def generate_batch(
        self,
        template_id: str,
        format: str,
        documents: List[Dict[str, Any]],
        *,
        workspace_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate multiple documents in a batch (async)."""
        body: Dict[str, Any] = {
            "templateId": template_id,
            "format": format,
            "documents": documents,
        }

        if workspace_id:
            body["workspaceId"] = workspace_id
        if webhook_url:
            body["webhookUrl"] = webhook_url
        if webhook_secret:
            body["webhookSecret"] = webhook_secret

        response = await self._http.post("/api/v1/documents/generate/batch", body)
        return response.get("data", response)

    async def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get a document job by ID (async)."""
        response = await self._http.get(f"/api/v1/documents/jobs/{job_id}")
        return response.get("data", response)

    async def list_jobs(
        self,
        *,
        status: Optional[str] = None,
        format: Optional[str] = None,
        template_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 20,
        page: int = 1,
    ) -> Dict[str, Any]:
        """List document jobs with optional filters (async)."""
        params = {
            "status": status,
            "format": format,
            "templateId": template_id,
            "workspaceId": workspace_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": limit,
            "page": page,
        }
        return await self._http.get("/api/v1/documents/jobs", params)

    async def wait_for_completion(
        self,
        job_id: str,
        *,
        poll_interval: float = 1.0,
        timeout: float = 30.0,
    ) -> Dict[str, Any]:
        """
        Wait for a document job to complete (async).

        Args:
            job_id: Job ID to wait for
            poll_interval: Time between polls in seconds (default: 1.0)
            timeout: Maximum wait time in seconds (default: 30.0)

        Returns:
            Completed job with downloadUrl

        Raises:
            TimeoutError: If job doesn't complete within timeout
        """
        start_time = time.time()

        while True:
            job = await self.get_job(job_id)

            if job["status"] in ("completed", "failed"):
                return job

            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for job {job_id} to complete")

            await asyncio.sleep(poll_interval)
