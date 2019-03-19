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

# Set up association Table between artists and albums
# collections = db.Table('collections',db.Column('album_id',db.Integer, db.ForeignKey('albums.id')),db.Column('artist_id',db.Integer, db.ForeignKey('artists.id'))) #template

# collections = db.Table('collections',db.Column('director_id',db.Integer, db.ForeignKey('directors.id')),db.Column('distributor_id',db.Integer, db.ForeignKey('distributors.id')))

# class Album(db.Model):
#     __tablename__ = "albums"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     artists = db.relationship('Artist',secondary=collections,backref=db.backref('albums',lazy='dynamic'),lazy='dynamic')
#     songs = db.relationship('Song',backref='Album')

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    movies = db.relationship('Movie',backref='Director')


# class Artist(db.Model):
#     __tablename__ = "artists"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     songs = db.relationship('Song',backref='Artist')
    #
    # def __repr__(self):
    #     return "{} (ID: {})".format(self.name,self.id)

class Distributor(db.Model):
    __tablename__ = "distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    budget = db.Column(db.Integer) #integer, float?
    usgross = db.Column(db.Integer) #integer, float?
    worldgross = db.Column(db.Integer) #integer, float?
    movies = db.relationship('Movie',backref='Distributor')


# class Song(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(64),unique=True) # Only unique title songs can exist in this data model
    # album_id = db.Column(db.Integer, db.ForeignKey("albums.id")) #ok to be null for now
    # artist_id = db.Column(db.Integer, db.ForeignKey("artists.id")) # ok to be null for now
    # genre = db.Column(db.String(64)) # ok to be null
    # # keeping genre as atomic element here even though in a more complex database it could be its own table and be referenced here
    #
    # def __repr__(self):
    #     return "{} by {} | {}".format(self.title,self.artist_id,self.genre)

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

# def get_or_create_artist(artist_name):
#     artist = Artist.query.filter_by(name=artist_name).first()
#     if artist:
#         return artist
#     else:
#         artist = Artist(name=artist_name)
#         session.add(artist)
#         session.commit()
#         return artist

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

def get_or_create_movie(movie_name):
    movie = Movie.query.filter_by(name=movie_name).first()
    if movie:
        return movie
    else:
        movie = Movie(name=movie_name)
        session.add(movie)
        session.commit()
        return movie
##### Set up Controllers (route functions) #####

## Main route
@app.route('/')
def home():
    return '<h1> Hello, everyone!</h1>'

# @app.route('/')
# def index():
#     songs = Song.query.all()
#     num_songs = len(songs)
#     return render_template('index.html', num_songs=num_songs)
#
# @app.route('/song/new/<title>/<artist>/<genre>/')
# def new_song(title, artist, genre): #instances
#     if Song.query.filter_by(title=title).first(): # if there is a song by that title
#         return "That song already exists! Go back to the main app!"
#     else:
#         artist = get_or_create_artist(artist) #instance
#         song = Song(title=title, artist_id=artist.id,genre=genre)
#         session.add(song)
#         session.commit()
#         return "New song: {} by {}. Check out the URL for ALL songs to see the whole list.".format(song.title, artist.name)

@app.route('/new/movie/<title>/<rating>/<director>/')
def new_movie(title, rating, director):
    if Movie.query.filter_by(title=title).first():
        return "That movie and director already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        movie = Movie(title=title, director_id=director.id,mpaarating=rating)
        session.add(movie)
        session.commit()
        return "Saving new movie: {} by {} to our database.".format(movie.title,director.name)

@app.route('/movies/all/')
def see_all():
    all_movies = [] #will be tuple list of title
    movies = Movie.query.all()
    for m in movies:
        director = Director.query.filter_by(id=director_id).first() #just get one director instance if any is there
        all_movies.append((m.title,director.name,m.rating)) #get list of movies with info
        return render_template('all_movies.html',all_movies=all_movies)
# @app.route('/all_songs')
# def see_all():
#     all_songs = [] # Will be be tuple list of title, genre
#     songs = Song.query.all()
#     for s in songs:
#         artist = Artist.query.filter_by(id=s.artist_id).first() # get just one artist instance if any is there
#         all_songs.append((s.title,artist.name, s.genre)) # get list of songs with info to easily access [not the only way to do this]
#     return render_template('all_songs.html',all_songs=all_songs) # check out template to see what it's doing with what we're sending!
#
# @app.route('/all_artists')
# def see_all_artists():
#     artists = Artist.query.all()
#     names = []
#     for a in artists:
#         num_songs = len(Song.query.filter_by(artist_id=a.id).all())
#         newtup = (a.name,num_songs)
#         names.append(newtup) # names will be a list of tuples
#     return render_template('all_artists.html',artist_names=names)
#
# @app.route('/songs/<genre>')
# def see_all_genre_songs(genre):
#     genre_songs = []
#     songs = Song.query.all()
#     for s in songs:
#         genre_x = Song.query.filter_by(genre=genre).all()
#         genre_songs.append(x.title,genre_x)
#     return render_template('genre.html',genre = genre_songs)
# def get_all_of_genre(genre):
#     songs_w_genre = Song.query.filter_by(genre=genre).all() #still SQL query (not giving the actual data, "asking a question")
#     # print(str(songs_w_genre))
#     # return "hello"            #testing
#     return render_template('genre_songs.html',genresongs=songs_w_genre)



if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
