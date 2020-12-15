import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = Question(question='What?',
                                     answer='Oh',
                                     category='2',
                                     difficulty=4).format()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for
    expected errors.
    """
    def test_category_list(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['total_questions'])
        self.assertNotEqual(len(data['questions']), 0)
        self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/question?page=1000', json={'rating': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Use invalid data
        res = self.client().post('/questions', json={'question': '',
                                                     'answer': 'Oh',
                                                     'category': '2',
                                                     'difficulty': 4})
        self.assertIsNone(data.get('previous_questions'))
        self.assertEqual(res.status_code, 422)

        # Use invalid data
        res = self.client().post('/questions', json={'question': 44,
                                                     'answer': 'Oh',
                                                     'category': '2',
                                                     'difficulty': 4})
        self.assertIsNone(data.get('previous_questions'))
        self.assertEqual(res.status_code, 422)

        res = self.client().post('/questions', json={'question': 'question',
                                                     'answer': 'Oh',
                                                     'category': '2',
                                                     'difficulty': 0})
        self.assertIsNone(data.get('previous_questions'))
        self.assertEqual(res.status_code, 422)

    def test_delete_questions(self):
        question_id = Question.query.all()[-1].id
        total_questions = len(Question.query.all())
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertIsNotNone(len(Question.query.all()), total_questions - 1)

    def test_delete_invalid_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)

        res2 = self.client().post('/questions', json={'searchTerm': 'N0NSENS'})
        data2 = json.loads(res2.data)

        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)
        self.assertEqual(data2['total_questions'], 0)

    def test_get_category_questions(self):
        category_id = 1

        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['total_questions'])
        self.assertNotEqual(len(data['questions']), 0)
        self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(data['current_category'], 'science')

    def test_play_quiz(self):
        category = Category.query.filter(Category.id == 1).one_or_none()
        res = self.client().post('/quizzes', json={
                'quiz_category': category.format()})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Test when all the questions in this category have been asked
        formatted_questions = [q.id for q in Question.query
                               .filter(Question.category == category.id)
                               .all()]
        res = self.client().post('/quizzes', json={
                        'quiz_category': category.format(),
                        'previous_questions': formatted_questions})
        data = json.loads(res.data)
        self.assertIsNone(data.get('previous_questions'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
