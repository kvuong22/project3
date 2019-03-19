import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'something something for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_movie.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

# Set up association Table between artists and albums
# collections = db.Table('collections',db.Column('album_id',db.Integer, db.ForeignKey('albums.id')),db.Column('artist_id',db.Integer, db.ForeignKey('artists.id'))) #template

collections = db.Table('collections',db.Column('director_id',db.Integer, db.ForeignKey('directors.id')),db.Column('distributor_id',db.Integer, db.ForeignKey('distributors.id')))

class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    artists = db.relationship('Artist',secondary=collections,backref=db.backref('albums',lazy='dynamic'),lazy='dynamic')
    songs = db.relationship('Song',backref='Album')

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    songs = db.relationship('Song',backref='Artist')

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Distributor(db.Model):
    __tablename__ = "distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    budget = db.Column(db.Integer) #integer, float?
    usgross = db.Column(db.Integer) #integer, float?
    worldgross = db.Column(db.Integer) #integer, float?


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title songs can exist in this data model
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id")) #ok to be null for now
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id")) # ok to be null for now
    genre = db.Column(db.String(64)) # ok to be null
    # keeping genre as atomic element here even though in a more complex database it could be its own table and be referenced here

    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.artist_id,self.genre)

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

def get_or_create_artist(artist_name):
    artist = Artist.query.filter_by(name=artist_name).first()
    if artist:
        return artist
    else:
        artist = Artist(name=artist_name)
        session.add(artist)
        session.commit()
        return artist


##### Set up Controllers (route functions) #####
