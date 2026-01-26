"""
Renderbase Python SDK

Official SDK for the Renderbase document generation platform.

Example:
    >>> from renderbase import Renderbase
    >>>
    >>> client = Renderbase(api_key="your_api_key")
    >>>
    >>> # Generate a PDF document
    >>> result = client.documents.generate(
    ...     template_id="tmpl_invoice",
    ...     format="pdf",
    ...     variables={"invoiceNumber": "INV-001"}
    ... )
    >>> print(f"Job ID: {result['jobId']}")
    >>> print(f"Download URL: {result['downloadUrl']}")
"""

from .client import Renderbase, AsyncRenderbase
from .http import RetryConfig
from .exceptions import RenderbaseError, WebhookSignatureError
from .webhooks import verify_webhook_signature

__version__ = "1.0.0"
__all__ = [
    "Renderbase",
    "AsyncRenderbase",
    "RetryConfig",
    "RenderbaseError",
    "WebhookSignatureError",
    "verify_webhook_signature",
]
