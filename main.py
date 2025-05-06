from fastapi import FastAPI, Body
from pydantic import EmailStr, BaseModel

import uvicorn


app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def hello():
    return {"message": "Hello world"}


@app.get("/hello/")
def hell_name(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.post("/users/")
def create_user(user: CreateUser):
    return {
        "message": "Succes",
        "email": user.email
    }


@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


@app.get("/items/")
def list_items():
    return ["item1", "item2"]


@app.get("/item/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}



@app.get("/items/{item_id}/")
def get_item(item_id: int):
    return {
        "item":{
            "item_id": item_id,
        }
    }




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
