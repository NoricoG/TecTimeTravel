import logging
import time
import yaml

from load.opensky.load_save import load_and_save_range, get_latest_saved


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("config/config.yml", 'r') as file:
    config_yml = yaml.safe_load(file)
    INTERVAL = config_yml['load']['opensky']['interval']
    MINUTES_IN_PAST = config_yml['load']['opensky']['minutes_in_past']


def get_current_opensky_time():
    return int(time.time() / INTERVAL) * INTERVAL


def get_start_time(minutes_in_past=MINUTES_IN_PAST):
    if minutes_in_past > 60:
        logger.warning("Parameter minutes_in_past is too large, "
                       "can't retrieve more than an hour in the past. "
                       "It will be changed to almost that maximum.")
        minutes_in_past = 60
    intervals_in_past = minutes_in_past * 60 / INTERVAL - 1
    return get_current_opensky_time() - INTERVAL * intervals_in_past


def continuously_retrieve_and_save(start_time=None):
    if start_time is None:
        start_time = get_start_time()

    while True:
        end_time = get_current_opensky_time()

        if end_time - start_time >= 3600:
            logger.warning(f"Range from start_time {start_time} to current time {end_time} "
                           "is longer than an hour. "
                           "It will be changed to almost that maximum.")
            start_time = end_time - 3600 + INTERVAL

        start_time = load_and_save_range(start_time, end_time)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    first_start_time = get_latest_saved()
    if first_start_time is not None:
        first_start_time += INTERVAL
        logger.info(f"The next timestamp that needs to be retrieved is {first_start_time}")

    continuously_retrieve_and_save(first_start_time)
