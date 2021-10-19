from typing import Optional


class Course:
    def __init__(
        self,
        id: str,
        name: str,
        categories: str,
        price: int,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.name: str = name
        self.categories: str = categories
        self.price: int = price
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Course):
            return self.id == o.id

        return False
