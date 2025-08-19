from fastapi import FastAPI
from app.api.routes import caption
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="Image Caption Generator API",
  version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(caption.router, prefix="/api/v1/caption", tags=["Caption"])
