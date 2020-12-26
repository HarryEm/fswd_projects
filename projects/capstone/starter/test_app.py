# import os
import unittest
import json
from os import environ as env
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movie, Actor

token_assistant1 = env.get('TOKEN_ASSISTANT_ONE')
token_director1 = env.get('TOKEN_DIRECTOR_ONE')
token_producer1 = env.get('TOKEN_PRODUCER_ONE')

headers_assistant1 = {'Authorization': 'Bearer ' + str(token_assistant1)}
headers_director1 = {'Authorization': 'Bearer ' + str(token_director1)}
headers_producer1 = {'Authorization': 'Bearer ' + str(token_producer1)}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movie_casting_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_actors_401(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_get_actors_404(self):
        '''No actors to find yet'''
        res = self.client().get('/actors',
                                headers=headers_assistant1)
        self.assertEqual(res.status_code, 404)

    def test_get_movies_401(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_get_movies_404(self):
        '''No actors to find yet'''
        res = self.client().get('/movies',
                                headers=headers_assistant1)
        self.assertEqual(res.status_code, 404)

    def test_create_new_actor_401(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1)
        self.assertEqual(res.status_code, 401)

        res2 = self.client().post('/actors', json=test_actor_1,
                                  headers=headers_assistant1)
        self.assertEqual(res2.status_code, 401)

    def test_create_new_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers=token_director1)

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

        res = self.client().get('/actors',
                                headers=token_director1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(len(data['actors']), 1)

    def test_create_new_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)

        res2 = self.client().get('/movies',
                                 headers=token_producer1)
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)

        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['movies'])
        self.assertEqual(len(data2['movies']), 1)

    def test_edit_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers=token_director1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/actors/1', json={"name": "Brad Pitt"},
                                   headers=token_director1)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['actor']['name'], "Brad Pitt")

        res3 = self.client().get('/actors',
                                 headers=token_director1)
        data = json.loads(res3.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(len(data['actors']), 1)

    def test_edit_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/movies/1', json={"title": "Fight Club"},
                                   headers=token_producer1)

        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['movie']['title'], "Fight Club")

        res3 = self.client().get('/movies',
                                 headers=token_producer1)
        data3 = json.loads(res3.data)
        self.assertEqual(data3['success'], True)
        self.assertIsNotNone(data3['movies'])
        self.assertEqual(len(data3['movies']), 1)

    def test_delete_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers=token_director1)

        res2 = self.client().get('/actors',
                                 headers=token_director1)
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)
        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['actors'])
        self.assertEqual(len(data2['actors']), 1)

        res3 = self.client().delete('/actors/1',
                                    headers=token_director1)
        data3 = json.loads(res3.data)
        self.assertEqual(data3['success'], True)
        self.assertEqual(data3['delete'], 1)

        res4 = self.client().get('/actors',
                                 headers=token_director1)
        self.assertEqual(res4.status_code, 404)

    def test_delete_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().get('/movies',
                                 headers=token_producer1)
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)
        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['movies'])
        self.assertEqual(len(data2['movies']), 1)

        res3 = self.client().delete('/movies/1',
                                    headers=token_producer1)
        self.assertEqual(res3.status_code, 200)
        data3 = json.loads(res3.data)
        self.assertEqual(data3['success'], True)
        self.assertEqual(data3['delete'], 1)

        res4 = self.client().get('/movies',
                                 headers=token_producer1)
        self.assertEqual(res4.status_code, 404)

    def test_edit_invalid_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/actors/99999', json={"name": "Brad Pitt"},
                                   headers=token_producer1)
        self.assertEqual(res2.status_code, 404)

    def test_delete_invalid_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().delete('/actors/99999',
                                    headers=token_producer1)
        self.assertEqual(res2.status_code, 404)

    def test_edit_invalid_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/movies/99999', json={"name": "Brad Pitt"},
                                   headers=token_producer1)
        self.assertEqual(res2.status_code, 404)

    def test_delete_invalid_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers=token_producer1)
        self.assertEqual(res.status_code, 200)

        res2 = self.client().delete('/movies/99999',
                                    headers=token_producer1)
        self.assertEqual(res2.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
