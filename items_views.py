from fastapi import Path, APIRouter
from typing import Annotated


router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
def list_items():
    return ["item1", "item1"]


@router.get("/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}



@router.get("{item_id}/")
def get_item(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]): # Annotated список для типизации, Path - для создания доп фильтрации параметра из ссылки ge - больше чем  lt меньше чем
    return {
        "item":{
            "item_id": item_id,
        }
    }
