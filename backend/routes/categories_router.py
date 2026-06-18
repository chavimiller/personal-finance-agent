from fastapi import APIRouter
from pydantic import BaseModel

from controllers.categories import (
    add_keyword_to_category,
    get_categories
)

router = APIRouter()

class AddCategoryRequest(BaseModel):
    category: str
    description: str

@router.get("/")
def list_categories():
    return get_categories()

@router.post("/add")
def add_category(req: AddCategoryRequest):
    return add_keyword_to_category(
        req.category,
        req.description
    )