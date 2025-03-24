# Dog Search Backend

Бэкенд-сервер для проекта поиска собак, построенный на FastAPI.

## Установка и Запуск

### 1. Создание виртуального окружения
в терминале:  
python -m venv venv  
venv\Scripts\activate  
### 2. Установка зависимостей
в терминале:  
pip install -r requirements.txt  

### 3. Настройка базы данных
создайте файл .env, в нем:  
B_USER='sfp_user'
DB_PASSWORD='uIWVTcwnX7XNZ0wyksi3dDUJ9NClQH7J'
DB_NAME='animal_finder'
DB_HOST='dpg-cva02i2j1k6c739d0dm0-a.frankfurt-postgres.render.com'

DATABASE_URL=postgresql+asyncpg://spf_user:uIWVTcwnX7XNZ0wyksi3dDUJ9NClQH7J@dpg-cva02i2j1k6c739d0dm0-a.frankfurt-postgres.render.com:5432/animal_finder

### 4. Запуск сервера
в терминале:  
cd backend  
uvicorn app.main:app --reload  
## Документация API
FastAPI автоматически генерирует интерактивную документацию:
- Swagger UI: http://localhost:8000/docs  


В документации вы найдете:  
- Все доступные эндпоинты  
- Схемы запросов и ответов  
- Возможность тестировать API прямо из браузера  

## Парсер данных

Для запуска парсера данных с сайта:  
в терминале:  
python -m backend.app.database.db  
