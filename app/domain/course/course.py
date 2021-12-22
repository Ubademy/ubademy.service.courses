from typing import List, Optional


class Course:
    def __init__(
        self,
        id: str,
        creator_id: str,
        name: str,
        price: float,
        active: bool,
        language: str,
        country: str,
        description: str,
        categories: List[str],
        presentation_video: str,
        image: str,
        subscription_id: int,
        recommendations: dict,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.creator_id: str = creator_id
        self.name: str = name
        self.price: float = price
        self.active: bool = active
        self.language: str = language
        self.country: str = country
        self.description: str = description
        self.categories: List[str] = categories
        self.presentation_video: str = presentation_video
        self.image: str = image
        self.subscription_id: int = subscription_id
        self.recommendations: dict = recommendations
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Course):
            return self.id == o.id

        return False
