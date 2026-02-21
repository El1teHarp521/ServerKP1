from fastapi import FastAPI

from app.config import load_config
from app.logger import logger
from app.models import User


# Загрузка кофига
config = load_config()
# Создание FastAPI
app = FastAPI(title="MIREA FastAPI Server")

if config.debug:
    app.debug = True


@app.get("/")
def read_root():
    logger.info("Кто-то зашел на главную страницу!")
    return {"message": "Hello, MIREA!"}


@app.post("/user")
async def create_user(user: User):
    logger.info(f"Получено сообщение от {user.username}")
    return {
        "status": "success",
        "received_message": user.message,
        "database_status": "Connected to " + config.db.database_url,
    }
