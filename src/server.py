from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_dbname = 'lipreading_predictions'

app = Flask(__name__)
CORS(app)

# Connect to MongoDB using MongoClient
client = MongoClient(mongo_uri)
db = client[mongo_dbname]


# Call the model
def predict_speech(video_path):
    if video_path is None:
        return
    # test data
    result = "How are you?"

    return(result)

# Post the prediction to MongoDB
@app.route("/prediction/new", methods=['POST'])
def extract_prediction():
    # Get 'file path' from client
    request_data = request.get_json()
    video_path = request_data.get('filePath')
    
    # call the model to predict the speech with 'video_path'
    prediction = predict_speech(video_path)

    # Get prediction
    today_date = datetime.now().strftime('%m%d%Y')
    prediction_list = {"name": "Dean", "sendtime": today_date, "prediction": prediction}

    # Send it to MongoDB
    if prediction is not None:
        # Connect & save to DB with error handling
        try:
            collection = db["predictions"]
            collection.insert_one(prediction_list)
        except Exception as e:
            print(f'Error saving data to MongoDB: {str(e)}')
    else:
        print('Error: Missing required keys in result entries.')

    return jsonify(prediction)


# Get all predictions from MongoDB
# Get all predictions from MongoDB
@app.route("/predictions", methods=['GET'])
def get_predictionss():
    try:
        # Fetch all documents
        predictions = list(db["predictions"].find().sort("sendtime", -1))

        # Convert ObjectId to str for JSON serialization
        for predict in predictions:
            predict['_id'] = str(predict['_id'])  # Convert ObjectId to string
            formatted_date = datetime.strptime(predict['sendtime'], '%m%d%Y').strftime('%b %d, %Y')
            predict['sendtime'] = formatted_date

        return jsonify(predictions)
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

    
@app.route("/")
def index():
    return "Welcome to the lipreading predictions API!"


if __name__ == "__main__":
    app.run(debug=True)