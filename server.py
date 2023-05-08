from flask import Flask, request
from pymongo import MongoClient
import os
from celery import Celery
from subprocess import run


app = Flask(__name__)

# Create a MongoDB client
db_uri = os.environ['MONGO_URI']
client = MongoClient(db_uri)

# Create a database and collection
db = client['mydatabase']
collection = db['mycollection']

@Celery.task
def insert_into_mongodb(data):
    collection.insert_many(data)

@app.route('/api/save-data', methods=['POST'])
def save_data():
    # Get the data from the request
    data = request.json
    insert_into_mongodb.delay(data)
    # Save the data to the database
    #collection.insert_many(data)

    return 'Data saved successfully'

@app.route('/health',methods=['GET'])
def check():
    return 'ok'

if __name__ == '__main__':
    #     app.run(debug=True)
    run("pipenv run gunicorn -w 2 -b 0.0.0.0:80 'server:app'".split(' '))
