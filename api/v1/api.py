from fastapi import APIRouter, Depends

from api.dependencies import get_api_key
from api.v1.endpoints import openai_gpt

api_router = APIRouter()

api_router.include_router(
    openai_gpt.router,
    prefix="/openai",
    tags=["OpenAI GPT"],
    dependencies=[Depends(get_api_key)],
)
