from typing import Optional


class Review:
    def __init__(
        self,
        id: str,
        course_id: str,
        recommended: bool,
        review: str,
        date: Optional[int] = None,
    ):
        self.id: str = id
        self.course_id: str = course_id
        self.recommended: bool = recommended
        self.review: str = review
        self.date: Optional[int] = date

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Review):
            return self.id == o.id and self.course_id == o.course_id

        return False
