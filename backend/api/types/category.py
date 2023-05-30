import strawberry

from backend.api.models.category import Category


@strawberry.experimental.pydantic.type(Category, fields=["name"])
class CategoryType:
    pass
