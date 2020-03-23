import requests
import yaml
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


with open("config/config.yml", 'r') as file:
    config_yml = yaml.safe_load(file)
    DATA_PATH = config_yml['paths']['data']
    DATA_PATH += "opensky/"
    INTERVAL = config_yml['load']['opensky']['interval']
    if INTERVAL < 5:
        logger.warning("Opensky interval is too small. It will be reset to 5 seconds.")
        INTERVAL = 5

with open("config/logins.yml", 'r') as file:
    logins_yml = yaml.safe_load(file)
    OPENSKY_USERNAME = logins_yml['opensky']['username']
    OPENSKY_PASSWORD = logins_yml['opensky']['password']
    OPENSKY_ENDPOINT = f"https://{OPENSKY_USERNAME}:{OPENSKY_PASSWORD}@opensky-network.org/api"


def load_all(timestamp):
    url = f"{OPENSKY_ENDPOINT}/states/all"
    if timestamp is not None:
        url += f"?time={timestamp}"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def save_json(name, data):
    with open(f"{DATA_PATH}{name}.json", "w") as file:
        json.dump(data, file)


def load_and_save(timestamp=None):
    data = load_all(timestamp)
    timestamp = data["time"]
    save_json(timestamp, data)
    logger.info(f"Saved opensky {timestamp}")


def load_and_save_range(start_time, end_time):
    # increase end_time to include original value in range
    # and to return next timestamp that should be retrieved
    next_time = end_time + INTERVAL

    for timestamp in range(start_time, next_time, INTERVAL):
        try:
            load_and_save(timestamp)
        except requests.exceptions.RequestException:
            logging.error(f"Error while retrieving opensky data for timestamp {timestamp}")
            return timestamp
        except IOError:
            logging.error(f"Error while saving opensky data for timestamp {timestamp}")
            return timestamp

    return next_time
