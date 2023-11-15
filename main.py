from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api.v1.api import api_router
from core.config import settings
from core.get_custom_redoc_html import get_redoc_html


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redoc_url=None,
    lifespan=lifespan,
)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/redoc", include_in_schema=False)
async def redoc_try_it_out() -> HTMLResponse:
    title = f"{app.title} - Redoc with try it out"
    return get_redoc_html(openapi_url=app.openapi_url, title=title)


@app.get("/health")
def health_check():
    return {"success": True, "message": "Service health check passed"}


app.include_router(api_router, prefix=settings.API_V1_STR)
