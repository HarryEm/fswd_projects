# FSND Capstone Project: Movie Casting Agency

The Casting Agency models a company that is responsible for creating movies and
managing and assigning actors to those movies. As an Executive Producer within
the company, this app helps create a system to simplify and streamline your process.

The app enables you to view, create, delete, and edit both actors and movies.
Each actor can be assigned to multiple movies and each movie can also be
assigned multiple actors.

## Motivation

Running a Movie Casting Agency is hard work and its particularly difficult keeping
track of actors and movies in an industry which is so fast moving. Every day
there are changes and instead of attempting to maintain a physical record of the
comings & goings, an app which manages an online database is far preferable.
It also calls for different permissions dependining on how senior someone's role is. 

## Using the app

The app has been deployed to heroku and can be accessed at https://movie-casting-agency.herokuapp.com/

This will take you to a log in page powered by Auth0 where you can sign up, or log in with
previously authorised credentials.

### RBAC controls

There are three Roles: Casting Assistant, Casting Director, and Executive Producer.

**Casting Assistant** can view actors and movies.
Auth0 permssions: `get:actors`, `get:movies`

**Casting Directors** have all the permissions of a Casting Assistant, and can also add or delete an actor, or modify actors or movies.
Auth0 permssions: `get:actors`, `get:movies`, ` post:actors`, `delete:actors`, `patch:actors`, `patch:movies`

**Executive Producers** have all the permissions of a Casting Director, and can also add or delete a movie from the database.
Auth0 permssions: `get:actors`, `get:movies`, ` post:actors`, `delete:actors`, `patch:actors`, `patch:movies`, `post:movies` `delete:movies`

A sample user for each role has been created for testing:

username: assistant1@gmail.com
pw: Assistant1

username: director1@gmail.com
pw: Director1

username: producer1@gmail.com
pw: Producer1

## API Endpoints

**Show Actors**
----
  Returns json data about all actors

* **URL**

  /actors

* **Method:**

  `GET`

*  **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200, actors :
      [ { 'id': 1, 'name': 'Brad Bitt', 'age': '57', 'gender': 'Male' } ] }`


* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ success: false, error: 404, message : "Not found" }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/actors

**Show Movies**
----
  Returns json data about all movies

* **URL**

  /movies

* **Method:**

  `GET`

*  **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200, movies :
      [ { 'id': 1, 'title': 'Night Club', 'release_date': '1999-11-12' } ] }`


* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ success: false, error: 404, message : "Not found" }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/movies


  **Create Actor**
  ----
    Create actor

  * **URL**

    /actors

  * **Method:**

    `POST`

  *  **URL Params**

    None

  * **Data Params**

    name=[string]

    age=[integer]

    gender=[string]

  * **Success Response:**

    * **Code:** 200 <br />
      **Content:** `{ success : true, status_code : 200 }`


  * **Sample Call:**
  https://movie-casting-agency.herokuapp.com/actors

  Request body

  ```json
  {
      "name": "Brad Bitt",
      "age": 57,
      "gender": "Male"
  }
  ```

**Create Movie**
  ----
  Create movies.

* **URL**

  /movies

* **Method:**

  `POST`

*  **URL Params**

  None

* **Data Params**

  title=[string]
  release_date=[string]

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200 }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/movies

Request body

```json
{
    "title": "Night Club",
    "release_date": "1999-11-12"
}
```

**Edit Actor**
----
  Edit actor

* **URL**

  /actors

* **Method:**

  `PATCH`

*  **URL Params**

  id=[integer]

* **Data Params**

  name=[string], optional

  age=[integer], optional

  gender=[string], optional

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200,
      actor: { 'id': 1, 'name': 'Brad Pitt', 'age': '57', 'gender': 'Male' } }`


* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ success: false, error: 404, message : "Not found" }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/actors/1

Request body

```json
{
    "name": "Brad Pitt"
}
```

**Edit Movie**
----
  Edit movies.

* **URL**

  /movies

* **Method:**

  `PATCH`

*  **URL Params**

  id=[integer]

* **Data Params**

  title=[string], optional
  release_date=[string], optional

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200,
      movie = { 'id': 1, 'title': 'Fight Club', 'release_date': '1999-11-12' }}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ success: false, error: 404, message : "Not found" }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/movies/1

Request body

```json
{
    "title": "Fight Club",
}
```

**Delete Actor**
----
  Delete actor by ID

* **URL**

  /actors

* **Method:**

  `DELETE`

*  **URL Params**

  id=[integer]

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200,
      delete: 1 }`


* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ success: false, error: 404, message : "Not found" }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/actors/1


**Delete Movie**
----
  Delete movie by ID

* **URL**

  /movies

* **Method:**

  `DELETE`

*  **URL Params**

  id=[integer]

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ success : true, status_code : 200,
      delete: 1 }`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ success: false, error: 404, message : "Not found" }`


* **Sample Call:**
https://movie-casting-agency.herokuapp.com/movies/1


## Local Development

Please follow the below to run the development server locally.

### Database Setup
This app interacts with a Postgres database called `movie_casting`.
If you do not have this database set up, with Postgres running, run:
```bash
createdb movie_casting
```

### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

## Testing
To run the tests, from within postgres run
``` bash
dropdb movie_casting_test
createdb movie_casting_test
python test_app.py
```
