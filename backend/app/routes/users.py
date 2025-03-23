from fastapi import APIRouter, HTTPException
from typing import List
from ..models.user import User, UserCreate, UserUpdate
from ..database.db import get_db_connection, close_db_connection

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
async def get_users():
    conn = await get_db_connection()
    try:
        users = await conn.fetch("""
            SELECT id, vk_id, first_name, last_name, created_at
            FROM users
        """)
        return [dict(user) for user in users]
    finally:
        await close_db_connection(conn)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    conn = await get_db_connection()
    try:
        user = await conn.fetchrow("""
            SELECT id, vk_id, first_name, last_name, created_at
            FROM users
            WHERE id = $1
        """, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return dict(user)
    finally:
        await close_db_connection(conn)

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    conn = await get_db_connection()
    try:
        created_user = await conn.fetchrow("""
            INSERT INTO users (vk_id, first_name, last_name)
            VALUES ($1, $2, $3)
            RETURNING id, vk_id, first_name, last_name, created_at
        """, user.vk_id, user.first_name, user.last_name)
        return dict(created_user)
    finally:
        await close_db_connection(conn)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    conn = await get_db_connection()
    try:
        updated_user = await conn.fetchrow("""
            UPDATE users
            SET vk_id = $1,
                first_name = $2,
                last_name = $3
            WHERE id = $4
            RETURNING id, vk_id, first_name, last_name, created_at
        """, user_update.vk_id, user_update.first_name, user_update.last_name, user_id)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return dict(updated_user)
    finally:
        await close_db_connection(conn)

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    conn = await get_db_connection()
    try:
        result = await conn.execute("""
            DELETE FROM users
            WHERE id = $1
        """, user_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return {"message": "Пользователь удален"}
    finally:
        await close_db_connection(conn)
