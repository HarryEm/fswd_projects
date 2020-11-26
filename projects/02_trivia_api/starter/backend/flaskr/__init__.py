import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
  completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET,PATCH,POST,DELETE,OPTIONS')

      return response

  @app.route('/')
  def hello():
      return "Hello World"
  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = [c.type for c in Category.query.all()]
      return jsonify({"categories": categories})

  '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  def get_paginated_questions(request,
                              questions,
                              total_questions,
                              num_of_questions=QUESTIONS_PER_PAGE):

    page = request.args.get('page', 1, type=int)

    start = (page - 1) * num_of_questions
    end = min(start + num_of_questions, total_questions - 1)
    formatted_questions = [q.format() for q in questions]
    current_questions = formatted_questions[start:end]

    return current_questions

  @app.route('/questions', methods=['GET'])
  def get_questions():
      try:
          questions = Question.query.all()
          total_questions = len(questions)
          current_questions = get_paginated_questions(request,
                                                      questions,
                                                      total_questions)

          if len(current_questions) == 0:
              abort(404)

          categories = [c.type for c in Category.query.all()]

          return jsonify({
                    'success': True,
                    'status_code': 200,
                    'questions': current_questions,
                    'total_questions': total_questions,
                    'categories': categories,
                    'current_category': None
                })
      except Exception:
          abort(404)

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be
  removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.filter(Question.id == question_id).\
            one_or_none()
      if not question:
          abort(404)
      try:
          question.delete()

          return jsonify({
                'success': True,
                'deleted': question_id
          })
      except Exception as e:
          print(e)
          abort(422)

  '''@TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
      body = request.get_json()

      search_term = body.get('searchTerm', None)

      try:
          if search_term:
              questions = Question.query.\
                    filter(Question.question.ilike(f'%{search_term}%')).\
                    all()
              questions_formatted = [q.format() for q in questions]

              return jsonify({
                        'success': True,
                        'status_code': 200,
                        'questions': questions_formatted,
                        'total_questions': len(questions),
                        'current_category': None
              })
          else:
              question_text = body.get('question', None)
              answer = body.get('answer', None)
              category = body.get('category', None)
              difficulty = body.get('difficulty', None)

              question = Question(question=question_text,
                                  answer=answer,
                                  category=category,
                                  difficulty=difficulty)
              question.insert()

              return jsonify({
                    'success': True,
                    'status_code': 200,
                    'created': question.id
              })

      except Exception as e:
          print(e)
          abort(422)

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''


  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
      }), 404

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

  return app
