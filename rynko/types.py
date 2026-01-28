"""
Rynko SDK Type Definitions
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict


# Document Types
class GenerateDocumentOptions(TypedDict, total=False):
    template_id: str
    format: Literal["pdf", "excel"]
    variables: Optional[Dict[str, Any]]
    workspace_id: Optional[str]
    webhook_url: Optional[str]
    webhook_secret: Optional[str]
    metadata: Optional[Dict[str, Any]]


class BatchDocument(TypedDict, total=False):
    variables: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]


class GenerateBatchOptions(TypedDict, total=False):
    template_id: str
    format: Literal["pdf", "excel"]
    documents: List[BatchDocument]
    workspace_id: Optional[str]
    webhook_url: Optional[str]
    webhook_secret: Optional[str]


DocumentJobStatus = Literal["queued", "processing", "completed", "failed"]

WebhookEventType = Literal[
    "document.completed",
    "document.failed",
    "batch.completed",
]


class CreateWebhookOptions(TypedDict, total=False):
    url: str
    events: List[WebhookEventType]
    name: Optional[str]


class ListDocumentJobsOptions(TypedDict, total=False):
    status: Optional[DocumentJobStatus]
    format: Optional[Literal["pdf", "excel"]]
    template_id: Optional[str]
    workspace_id: Optional[str]
    date_from: Optional[str]
    date_to: Optional[str]
    limit: Optional[int]
    page: Optional[int]


class ListTemplatesOptions(TypedDict, total=False):
    type: Optional[Literal["pdf", "excel"]]
    limit: Optional[int]
    page: Optional[int]
