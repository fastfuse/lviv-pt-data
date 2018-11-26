import csv
import os
from zipfile import ZipFile

import requests
from google.protobuf import json_format

from app import app
from .gtfs_realtime_pb2 import FeedMessage

DATA_DIR = app.config['DATA_DIR']


def get_vehicle_positions():
    """
    Parse vehicle_positions file to get real-time data
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

    with open(routes_data, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        routes = {row['route_id']: row for row in reader} if dict_ else [row for row in reader]

    return routes


def get_stops(geojson=False):
    """
    Parse stops.csv file to get info about stops.
    :param geojson: return data in geojson format
    """

    stops_data = os.path.join(DATA_DIR, "stops.txt")

    with open(stops_data, 'r') as csvfile:
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


def download_file(url, filename=None, dest_dir=None):
    """
    Download file

    :param url: file url
    :param filename: optional filename
    :param dest_dir: optional destination dir
    :return: path to saved file
    """
    filename = filename or url.split('/')[-1]
    dest = os.path.join(dest_dir, filename) if dest_dir else os.path.join(os.getcwd(), filename)

    r = requests.get(url, stream=True)

    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return dest


def unzip_archive(arch_name, dest_dir=None):
    """
    Unzip archive
    """
    dest = dest_dir or os.getcwd()

    with ZipFile(arch_name) as zf:
        zf.extractall(dest)

# if __name__ == '__main__':
#     positions_url = "http://track.ua-gis.com/gtfs/lviv/vehicle_position"
#     static_url = "http://track.ua-gis.com/gtfs/lviv/static.zip"
#
#     download_file(positions_url, dest_dir="data")
#     static_zip = download_file(static_url, dest_dir="data")
#
#     static_zip_path = os.path.join("data", static_zip)
#
#     unzip_archive(static_zip, "data")
