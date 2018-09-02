import json
import numbers
import urllib


def parse_geoloc_coords(cookietext):
    try:
        jsontext = urllib.parse.unquote(cookietext)
        coords = json.loads(jsontext)
    except json.JSONDecodeError as e:
        raise ValueError(e)

    if not (
        isinstance(coords.get('lat'), numbers.Number) and
        isinstance(coords.get('lon'), numbers.Number)
    ):
        raise ValueError("lat and lon must be numbers")

    return coords
