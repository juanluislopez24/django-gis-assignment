import json
import requests
import geojson

"""
Loads the municipalities geojson file and creates post requests to the API endpoint.
"""
BASE_URL = 'http://localhost:8000/api/'


def get_token():
    token_url = f'{BASE_URL}token/'
    # TODO: replace with env file
    user = "admin"
    password = "admin"
    # Get refresh token
    response = requests.post(token_url, data={'username': user, 'password': password})
    if response.status_code == 200:
        data = response.json()
        return data.get('refresh'), data.get('access')
    else:
        print("Failed to get refresh token")
        exit(1)


refresh_token, access_token = get_token()

geojson_file_path = './data/municipalities_nl.geojson'

try:
    with open(geojson_file_path, 'r') as f:
        geojson_data = json.load(f)
except FileNotFoundError:
    print(f"Error: GeoJSON file not found at {geojson_file_path}")
    exit(1)

api_url = f'{BASE_URL}municipalities/'

if geojson_data['type'] == 'FeatureCollection':
    for feature in geojson_data['features']:
        # Handle potential missing properties gracefully.
        name = feature['properties'].get('name', 'Unnamed')
        try:
            # Convert shapely geometry (if present) to GeoJSON using geojson library
            geometry = geojson.loads(geojson.dumps(feature['geometry'])) 
        except (KeyError, TypeError) as e:
            print(f"Error processing geometry for feature: {e}")
            continue # Skip this feature if geometry processing fails.

        data = {
            'name': name,
            'geom': geometry
        }
        response = requests.post(api_url, json=data, headers={'Authorization': f'Bearer {access_token}'})
        print(f"Feature: Status code - {response.status_code}, Response - {response.json()}")

else:
    print("Error: Input file is not a valid GeoJSON FeatureCollection")
    exit(1)
