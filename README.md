# **README**

## **What does this Project do?**
This project will create a database with the movie title, director name, and MPAA movie rating based on the input the user provides at the specified route and display a list with this information at the other specified route in the web browser. See Accessing Application Routes below for details.

## **Definitions for Functions in SI507_project3.py**
SI507_project3.py contains three classes: Director, Distributor, and Movie. Each class is a model to create its table in the database_movie.db file. Under each class are relevant attributes to the table along with their specifications and relationships. The Database_diagram.png shows a relational diagram between the three tables along with their attributes. There is a one:many relationship between Distributor and Movie and a one:many relationship between Director and Movie, which is reflected in the code.


## **Project Dependencies**

This project requires installation of what is listed in the requirements.txt file to run the project.


## **Running Flask Application**

Since we are using Flask_SQLAlchemy, to run the Flask application, in the command prompt, run 'python SI507_project2.py'. Access the webpage either by using 1) the generated URL in the command prompt or by using the URL link 2) http://localhost:5000 and paste it into the browser. The home page should have a message saying, "Hello, everyone!"

### **Accessing the Application Routes**
To access the route to add the movie title, rating and director to the database, edit the URL parameters in the browser to include '/new/movie/<title>/<rating>/<director>/'. Please note the way the code is set up, each movie added can only be added once. This means if a movie title has been directed by multiple directors, once the movie title is saved with one director, it will not save the same movie title with a different director to the database. To access the route to view the full list of all movie tiles, ratings, and directors added to the database, edit the URL parameters in the browser to include '/movies/all/'.
