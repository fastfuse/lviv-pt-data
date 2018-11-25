import csv
import os

import requests
from google.protobuf import json_format

from app import app
from .gtfs_realtime_pb2 import FeedMessage

DATA_DIR = app.config['DATA_DIR']


def download_file(url, filename=None, dest=None):
    """
    Download file

    :param url: file url
    :param filename: optional filename
    :param dest: optional destination dir
    :return: path to saved file
    """
    filename = url.split('/')[-1] if not filename else filename
    dest = os.path.join(dest, filename) if dest else os.path.join(os.getcwd(), filename)

    r = requests.get(url, stream=True)

    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return dest


def get_vehicle_positions():
    """
    Parse vevicle_positions file to get real-time data
    """
    # TODO: read vehicle positions w/ time

    vehicle_data = os.path.join(DATA_DIR, "vehicle_position")
    message = FeedMessage()

    with open(vehicle_data, 'rb') as f:
        message.ParseFromString(f.read())

    return json_format.MessageToDict(message)


def get_routes(dict_=False):
    """
    Parse routes.csv file to get info about routes
    :return: list of all routes if :param dict_: False else dict w/ routes in form {'route_id': {route_data}}
    """

    routes_data = os.path.join(DATA_DIR, "routes.txt")

    with open(routes_data, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        routes = {row['route_id']: row for row in reader} if dict_ else [row for row in reader]

    return routes


def get_stops(geojson=False):
    """
    Parse stops.csv file to get info about stops.
    :param geojson: return data in geojson format
    """

    stops_data = os.path.join(DATA_DIR, "stops.txt")

    with open(stops_data, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        if not geojson:
            return {row['stop_id']: row for row in reader}

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

        return collection
