from schemas.category import Category, CategoryUpdate
from database import prisma

# POST create category
async def create_category(category: Category):
    categories = await prisma.category.create(
        data = {
            "name": category.name,
            "icon": category.icon
        }
    )

    return categories

# GET All Category
async def read_all_category():
    categories = await prisma.category.find_many()
    return categories

# GET Category by id
async def query_category(categoryId: int):
    category = await prisma.category.find_unique(
        where={"id": categoryId}
    )

    return category

# PUT Edit Category
async def edit_category(categoryId: int, update_category: CategoryUpdate):
    updated_category = await prisma.category.update(
        where={"id": categoryId},
        data = {
            "name": update_category.name,
            "icon": update_category.icon
        }
    )

    return updated_category

async def delete_category(categoryId: int):
    deleted_category = await prisma.category.delete(
        where={"id": categoryId}
    )

    return deleted_category