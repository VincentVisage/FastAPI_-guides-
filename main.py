from fastapi import FastAPI
from pydantic import EmailStr, BaseModel
from contextlib import asynccontextmanager

import uvicorn

from core.models import Base, db_helper
from api_v1 import router as router_v1
from items_views import router as items_router
from users.views import router as users_router

from core.config import settings



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Проверим соединение с базой данных
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)



@app.get("/")
def hello():
    return {"message": "Hello world"}


@app.get("/hello/")
def hell_name(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
