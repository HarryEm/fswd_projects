import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def hello_world():
      return 'Hello, World from Flask!\n'

  @app.route('/actors', methods=['GET'])
  def get_actors():
    actors = [actor.format() for actor in Actor.query.all()]
    return jsonify({
              "success": True,
              'status_code': 200,
              "actors": actors
            }), 200

  @app.route('/movies', methods=['GET'])
  def get_movies():
    movies = [movie.format() for movie in Movie.query.all()]
    return jsonify({
              "success": True,
              'status_code': 200,
              "movies": movies
            }), 200

  @app.route('/actors/<int:actor_id>', methods=['POST'])
  def create_actor(actor_id):
    body = request.get_json()

  @app.route('/movies/<int:movie_id>', methods=['POST'])
  def create_movie(movie_id):
    body = request.get_json()

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def edit_actor(payload, actor_id):
    pass

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  def edit_movie(payload, movie_id):
    pass

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
    pass

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):
    pass

  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
