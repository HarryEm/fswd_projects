import os
from sqlalchemy import Column, Integer, String, Date
from flask_sqlalchemy import SQLAlchemy
# import json

database_name = "movie_casting"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
  '''
  Movie
  '''
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def __repr__(self):
      return '<Movie: {} released: {}>'.format(self.title, self.release_date)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # def format(self):
  #   return {
  #       'id': self.id,
  #       'question': self.question,
  #       'answer': self.answer,
  #       'category': self.category,
  #       'difficulty': self.difficulty
  #   }


class Actor(db.Model):
  '''
  Actor
  '''
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def __repr__(self):
      return '<Actor: {}>'.format(self.name)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # def format(self):
  #   return {
  #       'id': self.id,
  #       'question': self.question,
  #       'answer': self.answer,
  #       'category': self.category,
  #       'difficulty': self.difficulty
  #   }
