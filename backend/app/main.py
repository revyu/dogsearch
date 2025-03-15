from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import animals, users

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)




