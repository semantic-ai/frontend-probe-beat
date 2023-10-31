from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import decision, annotation, taxonomy, health

app = FastAPI()

origins = ["http://localhost:5173"]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

app.include_router(health.router)
app.include_router(decision.router)
app.include_router(annotation.router)
app.include_router(taxonomy.router)
