import yaml
import logging
import time

from load.opensky.load_save import load_and_save_range


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("config/config.yml", 'r') as file:
    config_yml = yaml.safe_load(file)
    INTERVAL = config_yml['load']['opensky']['interval']
    INTERVALS_IN_PAST = config_yml['load']['opensky']['intervals_in_past']


def get_current_opensky_time():
    return int(time.time() / INTERVAL) * INTERVAL


def get_start_time(intervals_in_past):
    if intervals_in_past * INTERVAL >= 3600:
        logger.warning("Parameter intervals_in_past is too large, "
                       "can't retrieve more than an hour in the past. "
                       "It will be changed to almost that maximum.")
        intervals_in_past = int(3600 / INTERVAL) - 1
    return get_current_opensky_time() - INTERVAL * intervals_in_past


def continuously_retrieve_and_save(start_time=None):
    if start_time is None:
        start_time = get_start_time(0)

    while True:
        end_time = get_current_opensky_time()

        if end_time - start_time >= 3600:
            logger.warning(f"Range from start_time {start_time} to end_time {end_time} "
                           "is longer than an hour. "
                           "It will be changed to almost that maximum.")
            start_time = end_time - 3600 + INTERVAL

        start_time = load_and_save_range(start_time, end_time)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    first_start_time = get_start_time(INTERVALS_IN_PAST)
    continuously_retrieve_and_save(first_start_time)
