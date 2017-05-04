import json
import logging
import os
import time
from urllib.parse import urlencode

import requests

logging.basicConfig(level=logging.INFO)

ENDPOINT = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
API_KEY = os.environ['API_KEY']

LOCATIONS = [
    "46.343135602601954,6.383056640625",
    "46.21024960018722,7.3333740234375",
    "46.23305294479828,8.0859375",
    "46.18363372751014,8.909912109375",
    "46.494610770689384,9.7283935546875",
    "46.773730730079386,10.01953125",
    "47.431803338643334,9.327392578125",
    "46.87145819560722,9.140625",
    "46.777492763768265,8.26171875",
    "47.44666502261753,8.3935546875",
    "47.27922900257082,7.4542236328125",
    "46.73233101286786,7.2344970703125",
    "46.81133924039194,6.932373046875"
]


def search_results(params):
    base_params = {
        'key': API_KEY
    }
    initial_params = {
        'type': 'restaurant',
        'keyword': 'McDonalds',
        # 'rankby': 'distance',
        'radius': '50000',
        **params
    }

    next_params = {
        **base_params,
        **initial_params,
    }
    results = []
    while range(10):  # Should never go further than 3 pages
        url = f'{ENDPOINT}?{urlencode(next_params)}'
        r = requests.get(url)
        data = r.json()
        if data['status'] == 'INVALID_REQUEST':
            logging.info('Page not ready, retrying...')
            time.sleep(2)
            continue
        results.extend(data['results'])

        next_page_token = data.get('next_page_token')
        if next_page_token:
            next_params = {
                **base_params,
                'pagetoken': next_page_token
            }
            time.sleep(2)
        else:
            break
    return results


def gather_places():
    places = {}
    for location in LOCATIONS:
        logging.info('Retrieving for location: %s', location)
        for place in search_results({'location': location}):
            key = place['place_id']
            places[key] = place
        logging.info('Number of places: %d', len(places))
    return places


def main():
    places = gather_places()
    print(json.dumps(places))


if __name__ == '__main__':
    main()
