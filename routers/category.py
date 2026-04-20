from fastapi import APIRouter, HTTPException, status
from crud import category as crud_category
from schemas.category import Category, CategoryResponse, CategoryWithMessageResponse, CategoryUpdate
from typing import List # send back data as list type to user

router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

#query all category
@router.get("/", response_model=List[CategoryResponse])
async def read_all_category():
    categories = await crud_category.read_all_category()
    return categories

#query by catID
@router.get("/{categoryId}", response_model=CategoryResponse)
async def query_category(categoryId: int):
    category = await crud_category.query_category(categoryId=categoryId)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category Id:{categoryId} not found."
        )

    return category

#create category
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: Category):
    categories = await crud_category.create_category(category=category)
    return categories

@router.put("/{categoryId}", response_model=CategoryWithMessageResponse)
async def edit_category(categoryId: int, update_category: CategoryUpdate):
    updated_category =  await crud_category.edit_category(categoryId=categoryId, update_category=update_category)
    return {
        "messages": f"Category Id:{categoryId} has been updated!",
        "category": updated_category
    }

@router.delete("/{categoryId}", response_model=CategoryWithMessageResponse)
async def delete_category(categoryId: int):
    deleted_category = await crud_category.delete_category(categoryId=categoryId)
    return {
        "messages": f"Category Id:{categoryId} has been deleted!",
        "category": deleted_category
    }