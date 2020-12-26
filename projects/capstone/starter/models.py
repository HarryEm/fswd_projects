import os
from sqlalchemy import Column, Integer, String, Date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# database_name = "movie_casting"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()


def db_drop_and_create_all():
    '''
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple
    verisons of a database
    '''
    db.drop_all()
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

  def format(self):
    return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date,
    }


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

  def format(self):
    return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
    }
