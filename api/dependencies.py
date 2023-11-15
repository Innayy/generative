import os

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="api_key", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == os.getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API key")
