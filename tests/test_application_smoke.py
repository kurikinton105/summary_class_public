import unittest

from application import app


class ApplicationSmokeTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_main_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_main_page_summarizes_multiple_sentences(self):
        response = self.client.post(
            "/",
            data={"input_text": "東京は日本の首都です。大阪は大きな都市です。京都には寺があります。横浜は港町です。"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Error:", response.data)

    def test_develop_page_renders(self):
        response = self.client.get("/develop")
        self.assertEqual(response.status_code, 200)

    def test_cos5year_page_renders(self):
        response = self.client.get("/cos5year")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
