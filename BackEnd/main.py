from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.conversations_routes import router as conversation_router
from api.routes import router
import observability

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(conversation_router)