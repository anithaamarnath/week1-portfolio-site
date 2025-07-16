# test_db.py

import unittest
from peewee import *

from app import TimelinePost


MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')
print(f"Using database: {test_db.database} for testing")
print(f"Database path: {MODELS[0]._meta.database.database}")


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):

        first_post = TimelinePost.create(
            name='John Doe', email="john@example.com", content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name='Jane Doe', email="jane@example.com", content='Hello world, I\'m Jane!.')
        assert second_post.id == 2

        # Fetch the lastet post
        lastest_post = TimelinePost.select().order_by(
            TimelinePost.created_at.desc()).get()

        self.assertEqual(lastest_post.name, 'Jane Doe')
        self.assertEqual(lastest_post.email, 'jane@example.com')
        self.assertEqual(lastest_post.content, 'Hello world, I\'m Jane!.')
