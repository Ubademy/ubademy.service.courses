from app.usecase.collab.collab_query_model import PaginatedUserReadModel, UserReadModel


class TestCollabQueryModel:
    def test_paginated_user_read_model(self):
        users = PaginatedUserReadModel(
            users=[UserReadModel(
                id="user_1",
                username="user_1",
                name="user_1",
                lastName="user_1",
                active=True,
                role=1,
                dateOfBirth="user_1",
                country="user_1",
                language="user_1",
                mail="user_1",
            )],
            count=1
        )
        assert len(users.users) == users.count
