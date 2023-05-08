from flask import Flask, request
from pymongo import MongoClient
import os
from gunicorn.app.wsgiapp import WSGIApplication


app = Flask(__name__)

# Create a MongoDB client
db_uri = os.environ['MONGO_URI']
client = MongoClient(db_uri)

# Create a database and collection
db = client['mydatabase']
collection = db['mycollection']

@app.route('/api/save-data', methods=['POST'])
def save_data():
    # Get the data from the request
    data = request.json

    # Save the data to the database
    collection.insert_many(data)

    return 'Data saved successfully'

if __name__ == '__main__':
    #app.run(debug=True)
    options = {
        'bind': '0.0.0.0:80',
        'workers': 2
    }
    
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
