from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.database import lifespan
from backend.routes import auth_router, note_router, user_router

app = FastAPI(
    title="Notes API",
    description="A simple API for managing notes with JWT authentication.",
    lifespan=lifespan,
    contact={
        "name": "Tariq Jamal A",
        "email": "tariqjamal4267324@gmail.com",
    },
)


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(note_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
