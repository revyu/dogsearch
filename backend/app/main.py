from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.routes import animals, users
from app.database.autoupdate import fetch_and_store_pets

app = FastAPI(title="Поиск потерянных животных")

""" Целесообразно запустить парсинг обновление базы данных в отдельном процессе """
# Запуск фона обновления данных при старте приложения
@app.on_event("startup")
async def startup_event():
    # Запускаем автообновление данных в фоновом режиме
    asyncio.create_task(fetch_and_store_pets())

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)




