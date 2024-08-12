from redis import Redis, ConnectionPool
import os
import redis.asyncio as redis

redis_pool = None


def get_in_memory_connection() -> Redis:
    global redis_pool
    if not redis_pool:
        host = os.environ.get(f"IN_MEMORY_STATE_HOST", "127.0.0.1")
        port = os.environ.get(f"IN_MEMORY_STATE_PORT", "6379")
        redis_pool = ConnectionPool(
            host=host, port=int(port), db=0, health_check_interval=30
        )
    return Redis(connection_pool=redis_pool)


def get_async_in_memory_connection():
    host = os.environ.get(f"IN_MEMORY_STATE_HOST", "127.0.0.1")
    port = os.environ.get(f"IN_MEMORY_STATE_PORT", "6379")
    return redis.from_url(
        f"redis://{host}:{int(port)}", encoding="utf-8", decode_responses=True
    )
