from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.conversations_routes import router as conversation_router
from api.ragas_dashboard import router as ragas_dashboard_router
from api.routes import router
from api.csv_routes import router as csv_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(conversation_router)
app.include_router(csv_router)
app.include_router(ragas_dashboard_router)