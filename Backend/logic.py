import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase credentials
url = "https://xmpyaomajehoojncybvz.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtcHlhb21hamVob29qbmN5YnZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIwMzI0MDYsImV4cCI6MjA1NzYwODQwNn0.vYM5VWdDtC922C-t34Od-hUlTNYIdeVs5PSJCpb-Txg"
supabase: Client = create_client(url, key)

# Initialize geolocator with a custom user agent
geolocator = Nominatim(user_agent="my_custom_geocoder")

@app.route('/data', methods=['GET'])
def get_data():
    logger.info("\033[94mReceived GET request for /data\033[0m")
    response = supabase.table('tast').select('*').execute()
    logger.info(f"\033[92mData retrieved from database: {response.data}\033[0m")
    return jsonify(response.data)

@app.route('/map-data', methods=['GET'])
def get_map_data():
    logger.info("\033[94mReceived GET request for /map-data\033[0m")
    response = supabase.table('tast').select('*').execute()
    logger.info(f"\033[92mMap data retrieved from database: {response.data}\033[0m")
    return jsonify(response.data)

@app.route('/safe-areas', methods=['GET'])
def get_safe_areas():
    logger.info("\033[94mReceived GET request for /safe-areas\033[0m")
    response = supabase.table('tast').select('name').eq('safety_status', True).execute()
    safe_areas = list(set([area['name'] for area in response.data]))  # Remove duplicates
    logger.info(f"\033[92mSafe areas retrieved from database: {safe_areas}\033[0m")
    return jsonify(safe_areas)

@app.route('/unsafe-areas', methods=['GET'])
def get_unsafe_areas():
    logger.info("\033[94mReceived GET request for /unsafe-areas\033[0m")
    response = supabase.table('tast').select('name').eq('safety_status', False).execute()
    unsafe_areas = list(set([area['name'] for area in response.data]))  # Remove duplicates
    logger.info(f"\033[92mUnsafe areas retrieved from database: {unsafe_areas}\033[0m")
    return jsonify(unsafe_areas)

@app.route('/crime-time-data', methods=['GET'])
def get_crime_time_data():
    logger.info("\033[94mReceived GET request for /crime-time-data\033[0m")
    response = supabase.table('tast').select('crime_time').execute()
    crime_times = [entry['crime_time'] for entry in response.data]
    logger.info(f"\033[92mCrime time data retrieved from database: {crime_times}\033[0m")
    return jsonify(crime_times)

@app.route('/geocode', methods=['GET'])
def geocode_place():
    place_query = request.args.get('place')
    if not place_query:
        return jsonify({"error": "Place query is required"}), 400

    try:
        location = geolocator.geocode(place_query)
        if location:
            return jsonify({"latitude": location.latitude, "longitude": location.longitude})
        else:
            return jsonify({"error": "Place not found"}), 404
    except Exception as e:
        logger.error(f"\033[91mError geocoding place: {e}\033[0m")
        return jsonify({"error": "Error processing geocode request"}), 500

@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    logger.info(f"\033[94mReceived POST request with data: {data}\033[0m")

    # Ensure the crime_time is in the correct format
    if 'crime_time' in data:
        data['crime_time'] = datetime.fromisoformat(data['crime_time']).isoformat()
    else:
        data['crime_time'] = datetime.now().isoformat()

    # Ensure safety_status is provided and is a boolean
    if 'safety_status' not in data or not isinstance(data['safety_status'], bool):
        logger.error("\033[91msafety_status is required and must be a boolean\033[0m")
        return jsonify({"error": "safety_status is required and must be a boolean"}), 400

    # Convert coords to POINT format
    if 'coords' in data:
        coords = data.pop('coords')
        data['coords'] = f"({coords['longitude']}, {coords['latitude']})"

    try:
        response = supabase.table('tast').insert(data).execute()
        logger.info(f"\033[92mData inserted into database: {response.data}\033[0m")
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"\033[91mError inserting data: {e}\033[0m")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
