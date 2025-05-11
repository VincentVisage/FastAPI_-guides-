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
def get_item(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]): # Annotated список для типизации, Path - говорит о том что атрибут из url и в нем можно укзаать фильтры
    return {
        "item":{
            "item_id": item_id,
        }
    }
