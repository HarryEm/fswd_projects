# import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movie, Actor

token_assistant1  = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR1dkhfMVdMTEtoZkdkZVF1eWtobiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWFwcGgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGZjYzNjNDUyMjY4MDA3NTU5ZGU2MCIsImF1ZCI6Im1vdmllLWNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjA4NTAyMzgwLCJleHAiOjE2MDg1MDk1ODAsImF6cCI6IkhmYUxwOTNPcDkwT3NRTzZhUUNHZ2dBUktsODZJUmlTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.olgk4o-wPqu-wql0jzLmFiQwm93MXK_yundHQBxzUFCZiyxM4ftouVwLD5OMHwpqZ9ysHG5MocLHs7zZKjySr0WqQ12p3jIZ3izjdgI2vmJ6l5CzcQFp3fM3AszSmhTfmaVpG0xsERwwsRCXFro1Wh8_XaDcc6ASfQ5aVs6uSxeZffvVFw3aSbzvOzdHj71Bbuj3OYxEcBx7D737xX1szTFRLFYizwjD_Y5A-k2j5UnL4sLjf5tH11pGbreAdnmu1xSBplq0mL26t_F6elAys_DxDF9Xyl7ymgJAHb4mpVMyDJyy-wi9gO5weFm40LJ-oaBl5_lky4gGHNHqo23p8w'

token_director1 = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR1dkhfMVdMTEtoZkdkZVF1eWtobiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWFwcGgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGZjZTEyZTAwYTgzMDA2ZTg5MDEzZSIsImF1ZCI6Im1vdmllLWNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjA4NTAzOTU4LCJleHAiOjE2MDg1MTExNTgsImF6cCI6IkhmYUxwOTNPcDkwT3NRTzZhUUNHZ2dBUktsODZJUmlTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.NZEipC0fmwdnk2rS6EuYhPc6xpUG7xHRdVQRc5bZlKyO-dwR8AjimQ6l-jqbFsFNOZfAecS8mSeOrGXvegLx7a3rxx05KLdCRO87H9C6e5h2P4pJYVAswmvd3HCBHxoJ5if3PqoNaSpsCC79QbQ_URYOXvmstNBphwRHcAITsJMKZpIRKTv-idpD1tqD9SPzkpC-jGXGNLBtsbONkamJD5IRnc3mpHW77ZnktAPtgxHXBS1eg97jFYyQtNdj_V-KkytZDGIr0v6cR72_2cw0VNk0yDNQZWOs0gdixHf67TnV6vLrvO8v_-AaHqqrdn4LnPpmCgJCQ-C94KMjIEW-qw'

token_producer1 = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR1dkhfMVdMTEtoZkdkZVF1eWtobiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWFwcGgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGZkNDA2YmJjNGY5MDA2ZjFmNTcyMSIsImF1ZCI6Im1vdmllLWNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjA4NTA0NDc4LCJleHAiOjE2MDg1MTE2NzgsImF6cCI6IkhmYUxwOTNPcDkwT3NRTzZhUUNHZ2dBUktsODZJUmlTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.SllgJI9ngzUdQTBdO5yU2A93w9r_jT9QBwqCINqrIPhRehTqhA-_CsqCAp2AUj9N0Q3TSNvJpIrYuy84_cvbUUv6CwTIKZcaJSHlAtMP39wLSlW4QcT00jL2_lUircM7-Z_DbVUK530I2RgX7huzdL7EJogsBw-eby-2C-uRiN517HB7vYXR2Py1a1xMhpxAoqp44hB1bMvtkz95sg9vuAXhbzqCzH9hHQ1z0eQxiJvhhoTD0_Je2JtLG913uOvoMm8dLq8HAbHPPhNUg5esxn0IirwxFrrlPvOQ07Q3ZdavQXIRQfunjpvzYaZD1yNyWOXIyK7WYpJfnRrso6bqpQ'


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
                                headers={'Authorization': token_assistant1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_movies_401(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_get_movies_404(self):
        '''No actors to find yet'''
        res = self.client().get('/movies',
                                headers={'Authorization': token_assistant1})
        self.assertEqual(res.status_code, 404)

    def test_create_new_actor_401(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1)
        self.assertEqual(res.status_code, 401)

        res2 = self.client().post('/actors', json=test_actor_1,
                                  headers={'Authorization': token_assistant1})
        self.assertEqual(res2.status_code, 401)

    def test_create_new_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers={'Authorization': token_director1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().get('/actors',
                                headers={'Authorization': token_director1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(len(data['actors']), 1)

    def test_create_new_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers={'Authorization': token_producer1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().get('/movies',
                                headers={'Authorization': token_producer1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])
        self.assertEqual(len(data['movies']), 1)

    def test_edit_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers={'Authorization': token_director1})
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/actors/1', json={"name": "Brad Pitt"},
                                   headers={'Authorization': token_director1})
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['actor']['name'], "Brad Pitt")

        res3 = self.client().get('/actors',
                                 headers={'Authorization': token_director1})
        data = json.loads(res3.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertEqual(len(data['actors']), 1)

    def test_edit_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/movies/1', json={"title": "Fight Club"},
                                   headers={'Authorization': token_producer1})

        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['movie']['title'], "Fight Club")

        res3 = self.client().get('/movies',
                                 headers={'Authorization': token_producer1})
        data3 = json.loads(res3.data)
        self.assertEqual(data3['success'], True)
        self.assertIsNotNone(data3['movies'])
        self.assertEqual(len(data3['movies']), 1)

    def test_delete_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers={'Authorization': token_director1})

        res2 = self.client().get('/actors',
                                 headers={'Authorization': token_director1})
        data2 = json.loads(res2.data)
        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['actors'])
        self.assertEqual(len(data2['actors']), 1)

        res3 = self.client().delete('/actors/1',
                                    headers={'Authorization': token_director1})
        data3 = json.loads(res3.data)
        self.assertEqual(data3['success'], True)
        self.assertEqual(data3['delete'], 1)

        res4 = self.client().get('/actors',
                                 headers={'Authorization': token_director1})
        self.assertEqual(res4.status_code, 404)

    def test_delete_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers={'Authorization': token_producer1})

        res2 = self.client().get('/movies',
                                 headers={'Authorization': token_producer1})
        data2 = json.loads(res2.data)
        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['movies'])
        self.assertEqual(len(data2['movies']), 1)

        res3 = self.client().delete('/movies/1',
                                    headers={'Authorization': token_producer1})
        data3 = json.loads(res3.data)
        self.assertEqual(data3['success'], True)
        self.assertEqual(data3['delete'], 1)

        res4 = self.client().get('/movies',
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res4.status_code, 404)

    def test_edit_invalid_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/actors/99999', json={"name": "Brad Pitt"},
                                   headers={'Authorization': token_producer1})
        self.assertEqual(res2.status_code, 404)

    def test_delete_invalid_actor(self):
        test_actor_1 = Actor(name="Brad Bitt", age="57", gender="Male")\
            .format()
        res = self.client().post('/actors', json=test_actor_1,
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res.status_code, 200)

        res2 = self.client().delete('/actors/99999',
                                    headers={'Authorization': token_producer1})
        self.assertEqual(res2.status_code, 404)

    def test_edit_invalid_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res.status_code, 200)

        res2 = self.client().patch('/movies/99999', json={"name": "Brad Pitt"},
                                   headers={'Authorization': token_producer1})
        self.assertEqual(res2.status_code, 404)

    def test_delete_invalid_movie(self):
        test_movie_1 = Movie(title="Night Club", release_date="1999-11-12")\
            .format()
        res = self.client().post('/movies', json=test_movie_1,
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res.status_code, 200)

        res2 = self.client().delete('/movies/99999',
                                    headers={'Authorization': token_producer1})
        self.assertEqual(res2.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
