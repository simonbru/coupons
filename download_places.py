import json
import os
import time
from urllib.parse import urlencode

import requests


ENDPOINT = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
API_KEY = os.environ['API_KEY']


def main():
    base_params = {
        'key': API_KEY
    }
    initial_params = {
        'type': 'restaurant',
        'query': 'Switzerland+McDonalds',
    }
    next_params = {
        **base_params,
        **initial_params,
    }
    results = []
    while True:
        url = f'{ENDPOINT}?{urlencode(next_params)}'
        r = requests.get(url)
        data = r.json()
        results.extend(data['results'])
        next_page_token = data.get('next_page_token')
        if next_page_token:
            next_params = {
                **base_params,
                'pagetoken': next_page_token
            }
            time.sleep(5)
        else:
            break
    print(json.dumps(results))

if __name__ == '__main__':
    main()
