from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .routers import decision, annotation, taxonomy, health

config = Config()

app = FastAPI()

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.fastapi.origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

app.include_router(health.router)
app.include_router(decision.router)
app.include_router(annotation.router)
app.include_router(taxonomy.router)
