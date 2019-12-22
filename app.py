from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# import credentials
username = os.environ.get("username")
password = os.environ.get("password")
cluster = os.environ.get("cluster")
# remote_db_port = os.environ.get("remote_db_port")
dbname = os.environ.get("dbname")

# Create an instance of Flask
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@{cluster}/{dbname}?retryWrites=true&w=majority"

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_scraped')
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route('/')
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html",mars=mars_data)


# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():

    # Run the scrape function and save the results to a variable
    results = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({},results, upsert=True)

    # Redirect back to home page
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
