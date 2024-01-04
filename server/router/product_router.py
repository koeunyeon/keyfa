from typing import List
from fastapi import APIRouter, Path

from pydantic import BaseModel, Field

router = APIRouter(prefix="/product", tags=["product"])

class GetProductListResponseSchema(BaseModel):
    id: int = Field(default=None, description="id")
    name: str = Field(default=None, description="name")
    category_id: int = Field(default=None, description="category id")
    price: int = Field(default=None, description="price")


@router.get("")
async def get_product_list() -> List[GetProductListResponseSchema]:
    pass

class GetProductItemResponseSchema(BaseModel):
    id: int = Field(default=None, description="id")
    name: str = Field(default=None, description="name")
    category_id: int = Field(default=None, description="category id")
    price: int = Field(default=None, description="price")

@router.get("/{id}")
async def get_product_item(*, id:int = Path()) -> GetProductItemResponseSchema:
    pass

class PostProductRequestSchema(BaseModel):
    name: str = Field(default=None, description="name")
    category_id: int = Field(default=None, description="category id")
    price: int = Field(default=None, description="price")

class PostProductResponseSchema(BaseModel):
    id: int = Field(default=None, description="id")

@router.post("")
async def post_product(product: PostProductRequestSchema) -> PostProductResponseSchema:
    pass
