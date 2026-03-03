from fastapi import FastAPI
import uvicorn

from app.config.app_config import add_cors_middleware
from app.controller import (
    buildable_controller,
    collection_controller,
    favorites_controller,
    parts_controller,
    search_controller,
    system_controller,
    user_controller,
    wishlist_controller,
)


app = FastAPI(title="LEGO Finder API")

add_cors_middleware(app)

app.include_router(search_controller.router)
app.include_router(collection_controller.router)
app.include_router(parts_controller.router)
app.include_router(wishlist_controller.router)
app.include_router(favorites_controller.router)
app.include_router(buildable_controller.router)
app.include_router(user_controller.router)
app.include_router(system_controller.router)


def run_app():
    """
    Starts the FastAPI application using Uvicorn.
    - Runs on host 0.0.0.0 (accessible from outside container)
    - Port 8000
    - Reload enabled for development
    """
    uvicorn.run(
        "app.api.fast_api:app", host="0.0.0.0", port=8000, reload=True
    )  # pragma: no cover
