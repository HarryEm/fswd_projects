import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET,PATCH,POST,DELETE,OPTIONS')

      return response

  @app.route('/')
  def hello_world():
      return 'Hello, World from Flask!\n'

  @app.route('/actors', methods=['GET'])
  @requires_auth(permission='get:actors')
  def get_actors(payload):
    actors = [actor.format() for actor in Actor.query.all()]

    if len(actors) == 0:
        abort(404)

    return jsonify({
              "success": True,
              'status_code': 200,
              "actors": actors
            }), 200

  @app.route('/movies', methods=['GET'])
  @requires_auth(permission='get:movies')
  def get_movies(payload):
    movies = [movie.format() for movie in Movie.query.all()]

    if len(movies) == 0:
        abort(404)

    return jsonify({
              "success": True,
              'status_code': 200,
              "movies": movies
            }), 200

  @app.route('/actors', methods=['POST'])
  @requires_auth(permission='post:actors')
  def create_actor(payload):
    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    actor = Actor(name=name, age=age, gender=gender)

    actor.insert()

    return jsonify({
                "success": True,
                'status_code': 200
            }), 200

  @app.route('/movies', methods=['POST'])
  @requires_auth(permission='post:movies')
  def create_movie(payload):
    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release_date')

    movie = Movie(title=title, release_date=release_date)

    movie.insert()

    return jsonify({
                "success": True,
                'status_code': 200
            }), 200

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth(permission='patch:actors')
  def edit_actor(payload, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    # Check actor exists
    if not actor:
        abort(404)

    body = request.get_json()
    actor.name = body.get('name', actor.name)
    actor.age = body.get('age', actor.age)
    actor.gender = body.get('gender', actor.gender)

    actor.update()

    return jsonify({
                "success": True,
                'status_code': 200,
                "actor": actor.format()
            }), 200

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth(permission='patch:movies')
  def edit_movie(payload, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Check actor exists
    if not movie:
        abort(404)

    body = request.get_json()
    movie.title = body.get('title', movie.title)
    movie.release_date = body.get('release_date', movie.release_date)

    movie.update()

    return jsonify({
                "success": True,
                'status_code': 200,
                "movie": movie.format()
            }), 200

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth(permission='delete:actors')
  def delete_actor(payload, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    # Check drink exists
    if not actor:
        abort(404)

    id = actor.id

    actor.delete()

    return jsonify({
                "success": True,
                'status_code': 200,
                "delete": id
            }), 200

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth(permission='delete:movies')
  def delete_movie(payload, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Check drink exists
    if not movie:
        abort(404)

    id = movie.id

    movie.delete()

    return jsonify({
                "success": True,
                'status_code': 200,
                "delete": id
            }), 200

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
      }), 404

  @app.errorhandler(405)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method Not Allowed"
      }), 405

  @app.errorhandler(422)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
      }), 422

  @app.errorhandler(500)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
      }), 500

  @app.errorhandler(AuthError)
  def unprocessable(error):
      return jsonify({
                      "success": False,
                      "error": "AuthError",
                      "message": "Authorization error"
                  }), AuthError

  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
