from fastapi import FastAPI
from .config import (
    RABBIT_PROTOCOL,
    RABBIT_USER,
    RABBIT_PASSWORD,
    RABBIT_HOST,
    RABBIT_PORT,
    OPEN_API_PATH,
)
from .const import TAGS_METADATA
from .routes import (
    default_router,
)
from nameko import config

config_setup = {
    "AMQP_URI": f"{RABBIT_PROTOCOL}://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}"
}
config.setup(config_setup)
print(config_setup)
print(config.get("AMQP_URI"))


def create_app() -> FastAPI:
    app = FastAPI(
        title="TaraChat API",
        version="0.0.1",
        openapi_url=OPEN_API_PATH,
        openapi_tags=TAGS_METADATA,
    )
    app.include_router(default_router)
    return app
