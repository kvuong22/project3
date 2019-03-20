import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'something something for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database_movie.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    movies = db.relationship('Movie',backref='Director')


class Distributor(db.Model):
    __tablename__ = "distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    budget = db.Column(db.Integer) #integer, float?
    usgross = db.Column(db.Integer) #integer, float?
    worldgross = db.Column(db.Integer) #integer, float?
    movies = db.relationship('Movie',backref='Distributor')


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    releasedate = db.Column(db.String(25))
    mpaarating = db.Column(db.String(5))
    source = db.Column(db.String(50))
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))
    distributor_id = db.Column(db.Integer, db.ForeignKey("distributors.id"))

##### Helper functions #####

### For database additions
### Relying on global session variable above existing

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

##### Set up Controllers (route functions) #####

## Main route
@app.route('/')
def homepage():
    return '<h1> Hello, everyone!</h1>'


@app.route('/new/movie/<title>/<rating>/<director>/')
def new_movie(title, rating, director):
    if Movie.query.filter_by(title=title).first():
        return "That movie already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        movie = Movie(title=title, director_id=director.id,mpaarating=rating)
        session.add(movie)
        session.commit()
        return "Saving new movie: {} by {} with {} rating to our database.".format(movie.title,director.name,rating.mpaarating)


@app.route('/movies/all/')
def see_all():
    all_movies = [] #will be tuple list of title
    movies = Movie.query.all()
    for m in movies:
        director = Director.query.filter_by(id=m.director_id).first() #just get one director instance if any is there
        all_movies.append((m.title,director.name,m.mpaarating)) #get list of movies with info
    return render_template('all_movies.html',all_movies=all_movies)


if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
