from flask import render_template, jsonify, make_response

from app import app, utils


@app.route('/')
@app.route('/index')
def index():
    routes = utils.get_routes()

    return render_template('index.html', routes=routes)


# ====================   API   ==========================

@app.route('/api/stops')
def stops():
    """
    Return geojson w/ stops data
    """
    stops = utils.get_stops(geojson=False)

    return make_response(jsonify(stops)), 200


@app.route('/api/positions')
def positions():
    """
    Return vehicle positions
    """
    vehicle_positions = utils.get_vehicle_positions()['entity']
    routes = utils.get_routes(dict_=True)

    for item in vehicle_positions:
        route_id = item['vehicle']['trip']['routeId']
        item['vehicle']['trip']['route'] = routes.get(route_id)

    return make_response(jsonify(vehicle_positions)), 200


# TODO:
# * refresh static data
# * refresh vehicle_position
# * filter by route
# * mqtt
