# tests.py

import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]
test_db = SqliteDatabase(":memory:")


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)

        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="John Doe", email="john@example.com", content="Hello World, I'm John!"
        )
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name="Jane Doe", email="jane@example.com", content="Hello World, I'm Jane!"
        )
        assert second_post.id == 2

        # get timeline posts and assert they are correct
        posts = [
            model_to_dict(p)
            for p in TimelinePost.select(
                TimelinePost.id,
                TimelinePost.name,
                TimelinePost.email,
                TimelinePost.content,  # `created_at` field is unpredictable, so we exclude it from our select
            ).order_by(TimelinePost.id)
        ]
        expected_posts = [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello World, I'm John!",
                "created_at": None,
            },
            {
                "id": 2,
                "name": "Jane Doe",
                "email": "jane@example.com",
                "content": "Hello World, I'm Jane!",
                "created_at": None,
            },
        ]
        assert posts == expected_posts
