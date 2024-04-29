from flask import Flask, request, jsonify, render_template
from utilities import fetch_and_create_shapefile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-shapefile', methods=['POST'])
def handle_request():
    content = request.get_json()
    if not content or 'apiUrl' not in content or 'district' not in content:
        return jsonify({'error': 'Missing parameters, please provide both api_url and district'}), 400

    api_url = content['apiUrl']
    district = content['district']

    # Pass API URL and district to the function and return the response
    result = fetch_and_create_shapefile(api_url, district)
    return jsonify(result), 200

@app.route('/display')
def display():
    api_url = request.args.get('apiUrl')
    district = request.args.get('district')

    # Fetch head of the GeoDataFrame using the provided API URL
    gdf_head = fetch_gdf_head(api_url)

    return render_template('display.html', district=district, gdf_head=gdf_head)

def fetch_gdf_head(api_url):
    # Your logic to fetch and process head of the GeoDataFrame using the provided API URL
    pass

if __name__ == '__main__':
    app.run(debug=True)
