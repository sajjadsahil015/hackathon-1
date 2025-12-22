"""FastAPI application entry point for RAG Chatbot."""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

from dotenv import dotenv_values

# Load .env file to override system env vars
_env_path = Path(__file__).parent.parent.parent / ".env"
if _env_path.exists():
    _env_config = dotenv_values(_env_path)
    for key, value in _env_config.items():
        if value:
            os.environ[key] = value

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .api.middleware import RateLimitMiddleware, RequestLoggingMiddleware
from .api.routes import router as query_router
from .chatkit_server import get_chatkit_server
from .config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown."""
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")

    # Startup logic here (e.g., initialize connections)
    yield

    # Shutdown logic here (e.g., close connections)
    logger.info("Shutting down application")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "RAG-based chatbot that answers questions grounded strictly in the "
            "Physical AI & Humanoid Robotics book content."
        ),
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middleware
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Include API routers
    app.include_router(query_router)

    return app


# Create application instance
app = create_app()


@app.get("/")
async def root() -> dict:
    """API root endpoint with service info.

    Returns:
        API information and available endpoints.
    """
    settings = get_settings()
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "description": "RAG-based chatbot for Physical AI & Humanoid Robotics book",
        "endpoints": {
            "POST /query": "Submit a question about the book",
            "GET /health": "Health check",
            "GET /stats": "Service statistics",
        },
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> dict:
    """Check API health status.

    Returns:
        Health status with service information.
    """
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/chatkit")
async def chatkit_endpoint(request: Request) -> Response:
    """ChatKit protocol endpoint for streaming responses.

    This endpoint implements the ChatKit protocol for SSE streaming.
    Clients can use this for real-time response streaming.

    Args:
        request: The incoming HTTP request.

    Returns:
        StreamingResponse for SSE or JSON response.
    """
    server = get_chatkit_server()
    body = await request.body()
    result = await server.process(body, context={"request": request})

    # Check if result is an async iterator (streaming) or dict (JSON)
    if hasattr(result, "__aiter__"):
        return StreamingResponse(
            result,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        import json
        return Response(
            content=json.dumps(result),
            media_type="application/json",
        )


def main() -> None:
    """Run the application using uvicorn."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "rag_chatbot.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
