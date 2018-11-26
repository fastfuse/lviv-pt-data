"""
Celery tasks.
"""

from app import celery, utils, app

DATA_DIR = app.config['DATA_DIR']
VEHICLE_POSITION_URL = app.config['VEHICLE_POSITION_URL']
STATIC_DATA_URL = app.config['STATIC_DATA_URL']


@celery.task
def update_static_data():
    """
    Update static data (stops, routes, etc.)
    """
    static_zip = utils.download_file(STATIC_DATA_URL, dest_dir=DATA_DIR)

    utils.unzip_archive(static_zip, DATA_DIR)


@celery.task
def update_vehicle_position():
    """
    Update vehicle real-time data
    """
    utils.download_file(VEHICLE_POSITION_URL, dest_dir=DATA_DIR)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call update_vehicle_position() every 10 seconds
    sender.add_periodic_task(12.0, update_vehicle_position.s(), name='update vehicle positions')
