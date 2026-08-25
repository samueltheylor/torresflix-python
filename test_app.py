import unittest

from app import app


class TorresFlixRegressionTests(unittest.TestCase):
    def login(self, client):
        with client.session_transaction() as session:
            session["user"] = "user"
            session["user_name"] = "Usuario"
            session["profile"] = "test-" + str(id(client))
        client.get("/home")

    def csrf(self, client):
        with client.session_transaction() as session:
            return session["csrf_token"]

    def test_search_page_has_its_own_input_id(self):
        client = app.test_client()
        self.login(client)
        response = client.get("/search")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="pageSearchInput"', response.data)

    def test_browse_rejects_unknown_categories(self):
        client = app.test_client()
        self.login(client)
        self.assertEqual(client.get("/browse?category=not-real").status_code, 404)

    def test_list_and_likes_reject_unknown_movie_ids(self):
        client = app.test_client()
        self.login(client)
        for path in ("/api/toggle-list", "/api/toggle-like"):
            self.assertEqual(client.post(path, json={"movie_id": 99999}, headers={"X-CSRF-Token": self.csrf(client)}).status_code, 400)

    def test_ratings_are_private_to_each_session(self):
        first = app.test_client()
        second = app.test_client()
        self.login(first)
        self.login(second)

        self.assertEqual(first.post("/api/rate", json={"movie_id": 1, "rating": 5}, headers={"X-CSRF-Token": self.csrf(first)}).status_code, 200)
        self.assertEqual([m["id"] for m in first.get("/api/search?min_rating=5").get_json()], [1])
        self.assertEqual(second.get("/api/search?min_rating=5").get_json(), [])

    def test_search_ignores_accents(self):
        client = app.test_client()
        self.login(client)
        result = client.get("/api/search?q=accion").get_json()
        self.assertTrue(any(movie["id"] == 2 for movie in result))

    def test_progress_is_saved_and_removed_when_complete(self):
        client = app.test_client()
        self.login(client)
        token = self.csrf(client)
        response = client.post(
            "/api/progress",
            json={"movie_id": 19, "position": 30, "duration": 120, "percent": 25},
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(client.get("/api/progress?movie_id=19").get_json()["percent"], 25)

        response = client.post(
            "/api/progress",
            json={"movie_id": 19, "position": 120, "duration": 120, "percent": 100},
            headers={"X-CSRF-Token": token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(client.get("/api/progress?movie_id=19").get_json(), {})

    def test_rating_must_be_in_range(self):
        client = app.test_client()
        self.login(client)
        self.assertEqual(client.post("/api/rate", json={"movie_id": 1, "rating": 6}, headers={"X-CSRF-Token": self.csrf(client)}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
