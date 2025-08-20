from fastapi import FastAPI
from app.api.routes import caption
from app.api.routes import hashtags, elements
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.timeout import RequestTimeoutMiddleware

app = FastAPI(
  title="Image Caption Generator API",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"], 
  allow_headers=["*"],
)

app.add_middleware(RequestTimeoutMiddleware, timeout=settings.request_timeout_seconds)

app.include_router(caption.router, prefix="/api/v1/caption", tags=["Caption"])
app.include_router(hashtags.router, prefix="/api/v1/hashtags", tags=["Hashtags"])
app.include_router(elements.router, prefix="/api/v1/elements", tags=["Elements"])
