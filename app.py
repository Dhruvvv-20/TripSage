from flask import Flask, jsonify, request
import boto3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Hardcoded AWS S3 Configuration
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
REGION = 'eu-north-1'
BUCKET_NAME = 'tripsage'

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

@app.route('/api/places', methods=['GET'])
def get_places():
    season = request.args.get('season')  # Get the current season from the query parameter

    if season not in ['Summer', 'Winter', 'Monsoon']:
        return jsonify({'error': 'Invalid season'}), 400

    # Retrieve images and itineraries from S3 based on the season folder
    folder_path = f'{season}/'
    try:
        objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_path)
        if 'Contents' not in objects:
            return jsonify([])  # Return an empty list if no images are found

        places = []
        for obj in objects['Contents']:
            file_name = obj['Key']
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                destination = file_name.split('/')[1]
                itinerary_key = f'{season}/{destination}/itinerary.json'
                
                # Try to fetch the itinerary file
                try:
                    itinerary_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=itinerary_key)
                    itinerary = itinerary_obj['Body'].read().decode('utf-8')
                except s3_client.exceptions.NoSuchKey:
                    itinerary = {}

                # Append place details including itinerary
                places.append({
                    'name': destination,
                    'image_url': f'https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file_name}',
                    'itinerary': itinerary
                })
        return jsonify(places)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_itinerary/<season>/<place>', methods=['GET'])
def get_itinerary(season, place):
    try:
        # Construct the key for the itinerary JSON file
        itinerary_key = f'{season}/{place}/itinerary.json'

        # Fetch the itinerary file from S3
        itinerary_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=itinerary_key)
        itinerary = itinerary_obj['Body'].read().decode('utf-8')
        
        return jsonify({'itinerary': itinerary})
    except s3_client.exceptions.NoSuchKey:
        return jsonify({'itinerary': 'No itinerary found for this place.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
