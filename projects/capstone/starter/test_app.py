# import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movie, Actor

token_assistant1 = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR1dkhfMVdMTEtoZkdkZVF1eWtobiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWFwcGgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGZjYzNjNDUyMjY4MDA3NTU5ZGU2MCIsImF1ZCI6Im1vdmllLWNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjA4NTcwMDIwLCJleHAiOjE2MDg1NzcyMjAsImF6cCI6IkhmYUxwOTNPcDkwT3NRTzZhUUNHZ2dBUktsODZJUmlTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.nCrUoAr7ar0456LCdZU82uRnj9L9w3ZNIhjHKShi23j-c0hQU-PL2vuSk_cqArpUdvvhs1JsQOumd0aYRMyaO1X31xiC6ZE9HJ-gQgFlw9UtwhrVUQqiRhn-uS7Wx7yExvg5wT5S9EeUnO7vtlQbbDMIov3OjLODzyPVZTSist_eXDTsTRQFsdWkSMYF-blmlp71IRRWMAqq43nsIb1ThlB7lVF-USACQRZ7Ii3bRY9c-O_6IMT9SgvnBkxOfQrVTd7q3ezzZz5leCo8KAe_5r198JDvV7_Fgn10KFNllmZeVGLV_wlwK2uWq6LB8tVKQexVelG3HKCGsiu3hW0bIA'

token_director1 = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR1dkhfMVdMTEtoZkdkZVF1eWtobiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWFwcGgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGZjZTEyZTAwYTgzMDA2ZTg5MDEzZSIsImF1ZCI6Im1vdmllLWNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjA4NTcwMjEzLCJleHAiOjE2MDg1Nzc0MTMsImF6cCI6IkhmYUxwOTNPcDkwT3NRTzZhUUNHZ2dBUktsODZJUmlTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.IVeXCCd_JW0cQ2LU2UoU4RMtCUEVcdiTOBU0g8CpoVQKw5qY1P2zl5O8l-zakxnXwRc6PyVhqXLP3FKFdX0shrb7MDxrEP36GqIBon-J6DnYz2mT8hczgsEL06gQV2p_dmGUFcrBsli3D0P6riycLHQ7r0fk9QB_GQ84lKozziNWoA_Ta-irqM3QVr3hmNMENNstUYcrEflSuyL_kkAaQIZy3DPqKe1MXM2Cr0RPb9pfx7MDeY75L8SIgA90XV9N7AsSLxnq061-w5oKTFy3GSsWAQEdbp5ZClIoDdCab6z0j4X0pzBkY6-ohRqjmqLDq8U-5ehjso35EzWGsqCvjw'

token_producer1 = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR1dkhfMVdMTEtoZkdkZVF1eWtobiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWFwcGgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGZkNDA2YmJjNGY5MDA2ZjFmNTcyMSIsImF1ZCI6Im1vdmllLWNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjA4NTY3ODcxLCJleHAiOjE2MDg1NzUwNzEsImF6cCI6IkhmYUxwOTNPcDkwT3NRTzZhUUNHZ2dBUktsODZJUmlTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.gokzKug0jxiVbrn6F4W80Fw1qwRIxVgs9uXusHUK-M9uRn_hFZ9EcTz7imrm8JHucqeHvpdKNzH5NO3_9L_3Fz65boqGSNqHdjxWaMaX4iHoNppkhXc_nOTU0qLgD9InSER6rboq_K-VDFQSbpAB-W5WOrtOa3ErYjycvpuEVrnBMW2MROG7bqaw3SERPnq-6WA18RxcHNRdpotMf1kudQLuIChjzKiavSWmrmWxWuyn-smfrtIhEvTQobu50TfkhOVtdiWDGNqhf7ClMy0UDZq8A03TYDbnf71HXxWh2ez9h-ji1mMNHAOVdulWUaTq_z1wWHI4ADATGo1OqOawPQ'


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

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
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
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)

        res2 = self.client().get('/movies',
                                headers={'Authorization': token_producer1})
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)

        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['movies'])
        self.assertEqual(len(data2['movies']), 1)

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
        self.assertEqual(res2.status_code, 200)
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
        self.assertEqual(res.status_code, 200)

        res2 = self.client().get('/movies',
                                 headers={'Authorization': token_producer1})
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)
        self.assertEqual(data2['success'], True)
        self.assertIsNotNone(data2['movies'])
        self.assertEqual(len(data2['movies']), 1)

        res3 = self.client().delete('/movies/1',
                                    headers={'Authorization': token_producer1})
        self.assertEqual(res3.status_code, 200)
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
