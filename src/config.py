import os


RABBIT_PROTOCOL = os.environ.get("RABBIT_PROTOCOL", "amqp")
RABBIT_USER = os.environ.get("RABBIT_USER", "guest")
RABBIT_PASSWORD = os.environ.get("RABBIT_PASSWORD", "guest")
RABBIT_HOST = os.environ.get("RABBIT_HOST", "localhost")
RABBIT_PORT = os.environ.get("RABBIT_PORT", "5672")
OPEN_API_PATH = os.environ.get("OPEN_API_PATH", "/openapi.json")
TOKEN_COOKIE_NAME = os.environ.get("TOKEN_COOKIE_NAME", "_tarachat_token")
