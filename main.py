from fastapi import FastAPI
from app.api.v1.stats_controller import router
from app.services.config import settings
from app.database import engine, Base, wait_for_db
import uvicorn


wait_for_db(engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Сервис сбора и анализа статистики с устройств",
    docs_url="/swagger",
    redoc_url="/redoc"
)

app.include_router(router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

@app.get("/")
def root():
    return "Server is running"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
