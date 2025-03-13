from fastapi import APIRouter, HTTPException
from typing import List

from app.models.user import User, UserCreate
from app.utils.auth import verify_vk_params

router = APIRouter(prefix="/users", tags=["users"])

#временная бд
fake_users_db = [
    {
        "id": 1,
        "vk_id": 123456789,
        "first_name": "Иван",
        "last_name": "Иванов",
        "created_at": "2025-03-08T12:00:00"
    }
]

@router.get("/me", response_model=User)
async def get_current_user(vk_id: int): #получить информацию о текущем пользователе
    for user in fake_users_db:
        if user["vk_id"] == vk_id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@router.post("/", response_model=User)
async def create_user(user: UserCreate): #создать или обновить пользователя при авторизации
   
    #проверяем, существует ли пользователь
    for existing_user in fake_users_db:
        if existing_user["vk_id"] == user.vk_id:
            #обновляем существующего пользователя
            existing_user.update(user.dict())
            return existing_user
    
    #создаем нового пользователя
    new_id = len(fake_users_db) + 1
    new_user = {
        "id": new_id,
        "created_at": "2025-03-09T14:30:00",
        **user.dict()
    }
    fake_users_db.append(new_user)
    return new_user
