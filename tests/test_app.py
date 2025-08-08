# tests/test_app.py

import unittest
import os

os.environ["TESTING"] = "true"

from app import app
from app import mydb
from app import TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        if mydb.is_closed():
            mydb.connect()
            mydb.create_tables([TimelinePost])

    def tearDown(self):  # avoids peewee resource leaks
        if not mydb.is_closed():
            mydb.close()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        headers = dict(response.headers)

        assert "<title>MLH Fellows</title>" in html
        assert '<h2 class="card-title fs-4">Anitha Amarnath</h2>' in html
        assert headers["Content-Type"] == "text/html; charset=utf-8"

    def test_timeline(self):
        endpoint = "/api/timeline_post"

        # GET
        get_res = self.client.get(endpoint)
        assert get_res.status_code == 200
        assert get_res.is_json
        json = get_res.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # POST
        post_res = self.client.post(
            endpoint,
            data={"name": "aname", "email": "fake@mailcom", "content": "test"},
        )
        assert post_res.status_code == 200
        json = post_res.get_json()
        assert json["name"] == "aname"
        assert json["email"] == "fake@mailcom"
        assert json["content"] == "test"
        assert json["id"] == 1

        # GET
        get_res = self.client.get(endpoint)
        assert get_res.status_code == 200
        json = get_res.get_json()
        assert (len(json["timeline_posts"]) == 1)  # table should have updated with the post request

        # DELETE
        delete_response = self.client.delete(endpoint + "/1")
        assert delete_response.status_code == 200
        assert delete_response.is_json

        json = delete_response.get_json()
        assert json == {"message": "Post deleted successfully", "status": "success"}
