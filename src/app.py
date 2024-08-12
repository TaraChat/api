import logging
from fastapi.middleware.cors import CORSMiddleware
from .extensions.database.connection.redis import get_async_in_memory_connection
from .utils import treat_return_exception, authorize, is_blocked
from fastapi import Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from . import create_app

app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("https")
@app.middleware("http")
async def treat_request(request: Request, call_next):
    call_endpoint = False
    try:
        logging.info(f"Starting request: [{request.url.path}]")
        response = await call_next(request)
        return response
    except Exception as err:
        return treat_return_exception(err, call_endpoint)


@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(get_async_in_memory_connection())
