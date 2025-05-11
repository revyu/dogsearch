from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.routes import animals, users
from app.database.db import get_db_connection
# from app.database.autoupdate import fetch_and_store_pets

app = FastAPI(title="Поиск потерянных животных")



# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение эндпоинтов
app.include_router(animals.router)
app.include_router(users.router)

@app.get("/test-db")
async def test_db_connection():
    try:
        conn = await get_db_connection()
        # Простой тестовый запрос
        result = await conn.fetch("SELECT 1")
        await conn.close()
        return {"status": "success", "message": "Подключение к БД установлено"}
    except Exception as e:
        return {"status": "error", "message": f"Ошибка подключения: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "API работает"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
