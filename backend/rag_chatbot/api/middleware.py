"""API middleware for rate limiting and error handling."""

import logging
import time
from collections import defaultdict
from typing import Callable

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import get_settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using sliding window algorithm.

    Limits requests per IP address to prevent abuse.
    """

    def __init__(self, app, requests_per_minute: int | None = None) -> None:
        """Initialize rate limiter.

        Args:
            app: The FastAPI application.
            requests_per_minute: Max requests per minute per IP.
                                Defaults to settings value.
        """
        super().__init__(app)
        settings = get_settings()
        self.requests_per_minute = requests_per_minute or settings.rate_limit_per_minute
        self.window_size = 60  # seconds
        self.request_counts: dict[str, list[float]] = defaultdict(list)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check for forwarded header (behind proxy)
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        # Fall back to direct connection
        if request.client:
            return request.client.host
        return "unknown"

    def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit."""
        current_time = time.time()
        window_start = current_time - self.window_size

        # Clean old entries
        self.request_counts[client_ip] = [
            ts for ts in self.request_counts[client_ip] if ts > window_start
        ]

        # Check limit
        if len(self.request_counts[client_ip]) >= self.requests_per_minute:
            return True

        # Record this request
        self.request_counts[client_ip].append(current_time)
        return False

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with rate limiting."""
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        client_ip = self._get_client_ip(request)

        if self._is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests. Please wait before trying again.",
                    "retry_after_seconds": self.window_size,
                },
            )

        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request details."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response details."""
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")

        response = await call_next(request)

        # Log response
        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"status={response.status_code} duration={duration_ms}ms"
        )

        return response
