import csv
import os

from flask import render_template, jsonify, make_response

from app import app


@app.route('/')
@app.route('/index')
def index():
    routes_data = os.path.join(f"{app.config['DATA_DIR']}", "static", "routes.txt")

    routes = list()

    with open(routes_data, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            routes.append(row)

    return render_template('index.html', routes=routes)


@app.route('/api/stops')
def stops():
    """
    Return geojson w/ stops data
    """
    stops_data = os.path.join(f"{app.config['DATA_DIR']}/stops.txt")

    with open(stops_data, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        collection = {"type": "FeatureCollection"}
        features = []

        for row in reader:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row.pop('stop_lon'), row.pop('stop_lat')],
                },
                "properties": row
            }

            features.append(feature)

        collection['features'] = features

        # with open('data.json', 'w') as f:
        #     json.dump(collection, f)

    return make_response(jsonify(collection)), 200
