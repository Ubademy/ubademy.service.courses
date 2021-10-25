from typing import List, Optional


class Course:
    def __init__(
        self,
        id: str,
        creator_id: str,
        name: str,
        price: float,
        language: str,
        description: str,
        categories: List[str],
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.creator_id: str = creator_id
        self.name: str = name
        self.price: float = price
        self.language: str = language
        self.description: str = description
        self.categories: List[str] = categories
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Course):
            return self.id == o.id

        return False
