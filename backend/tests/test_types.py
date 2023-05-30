from backend.api.models.category import Category
from backend.api.types.category import CategoryType


def test_category_type() -> None:
    [name_field] = CategoryType._type_definition.fields

    assert name_field.python_name == "name"

    instance = Category(name="Plot")
    data = CategoryType.from_pydantic(instance)
    assert data.name == "Plot"
