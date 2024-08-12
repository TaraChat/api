import re, ast
from fastapi import Request, status
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.const import BLOCKLIST


TOKEN_TYPE = "Bearer"


def get_context_data(request: Request):
    return request.state.context_data


def authorize(request: Request) -> dict:
    authorization = request.headers.get("Authorization", "")
    parts = authorization.split(" ")
    if (not authorization) or len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    token_type, token = parts

    if token_type.upper() != TOKEN_TYPE.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token Type"
        )

    return token


def treat_return_exception(exception: Exception, endpoint_called: bool):
    """Normalizar o retorno de exception


    Notes:
        Exemplo de mensagem de Exception:

        "NotFound 404 Not Found: Pessoa não encontrada", onde:

        -> "NotFound" e "Not Found": Representam o tipo do exception;
        -> "404": Representa o código do exception;

        A ideia é extrair o maior número de informações da mensagem do Exception, por exemplo: Status HTTP, Tipo do erro
        e mensagem do erro. Caso não se possível, ainda assim, iremos verificar se o exception possui atributos que
        possibilitem essa extração, como por exemplo o 'code' (que representa o status HTTP para Exceptions herdados de
        werkzeug.exceptions.HTTPException).

    Args:
        exception (Exception): Exception disparado
    """

    if isinstance(exception, HTTPException):
        return JSONResponse(
            content={
                "detail": exception.detail,
                "raw_error": exception.__repr__(),
                "exception": str(exception),
                "endpoint_called": endpoint_called,
            },
            status_code=exception.status_code,
        )
    match = re.match(r"^([a-zA-Z ]*)(\d*)([a-zA-Z ]*):(.*)$", str(exception))
    if match:
        http_status = int(match.group(2).strip())
        message = match.group(4).strip()
    else:
        http_status = getattr(exception, "code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        message = str(exception)

    return JSONResponse(
        content={
            "detail": message,
            "raw_message": str(exception),
            "raw_error": exception.__repr__(),
            "endpoint_called": endpoint_called,
        },
        status_code=http_status,
    )


def str2dict(string):
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        return {}


def matches_pattern(pattern, url_path):
    """Check if a given URL path matches a pattern."""
    pattern_segments = pattern.split("/")
    url_segments = url_path.split("/")
    # Early exit if segment lengths differ
    if len(pattern_segments) != len(url_segments):
        return False
    # Iterate through each segment and compare
    for pattern_segment, url_segment in zip(pattern_segments, url_segments):
        if pattern_segment != "*" and pattern_segment != url_segment:
            return False
    return True


def is_blocked(role_id: int, request: Request):
    method, request_url_path = request.method, request.url.path
    """Check if a role is blocked from accessing a specific URL path for a given method."""
    blocked_patterns = BLOCKLIST.get(role_id, {}).get(method, [])
    for pattern in blocked_patterns:
        if matches_pattern(pattern, request_url_path):
            return True
    return False
