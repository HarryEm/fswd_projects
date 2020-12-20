# FSND Capstone Project: Movie Casting Agency

The Casting Agency models a company that is responsible for creating movies and
managing and assigning actors to those movies. As an Executive Producer within
the company, this app helps create a system to simplify and streamline your process.

The app enables you to view, create, delete, and edit both actors and movies.
Each actor can be assigned to multiple movies and each movie can also be
assigned multiple actors.

## Getting Started

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
