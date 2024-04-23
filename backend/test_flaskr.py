import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # self.database_path = 'postgresql+psycopg2://postgres:12345678@localhost/trivia_test'
        user = os.getenv("DB_USER_TEST")
        password = os.getenv("DB_PASS_TEST")
        host = os.getenv("DB_HOST_TEST")
        port = os.getenv("DB_PORT_TEST")
        db_name = os.getenv("DB_NAME_TEST")
        self.database_path = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        self.add_question_form = {
            "question":"what time is it?", 
            "answer":"11:11", 
            "category":"1", 
            "difficulty":"3"
        }
        self.add_question_form_err = {}
        self.quizz = {
            "previous_questions": [1, 2, 3, 4],
            "quiz_category": {"id": "5"}
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_categories_error_404(self):
        res = self.client().get('/api/categories/100')
        # data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_get_questions_error_404(self):
        res = self.client().get('/api/questions?page=100')
        # data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete('/api/questions/23')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_error_404(self):
        res = self.client().delete('/api/questions/100')
        # data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_add_question(self):
        res = self.client().post('/api/questions', json=self.add_question_form)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_add_question_error_422(self):
        res = self.client().post('/api/questions', json=self.add_question_form_err)
        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):
        res = self.client().post('/api/search', json={"searchTerm": "What"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions_error_500(self):
        res = self.client().post('/api/search', json={"searchTerm": 0})
        self.assertEqual(res.status_code, 500)

    def test_get_questions_by_category(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_by_category_error_404(self):
        res = self.client().get('/api/categories/100/questions')
        self.assertEqual(res.status_code, 404)

    def test_get_question_to_play_quiz(self):
        res = self.client().post('/api/quizzes', json=self.quizz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_to_play_quiz_error_404(self):
        res = self.client().post('/api/quizzes', json={})
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()