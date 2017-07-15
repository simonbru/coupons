import argparse
import json

import sys
from django.core.management.base import BaseCommand, CommandError
from ...models import Restaurant


class Command(BaseCommand):
    help = 'Import restaurants from JSON data gathered using Google Maps API'

    def add_arguments(self, parser):
        parser.add_argument(
            'input_file',
            type=argparse.FileType('r'),
            default=sys.stdin,
        )

    def handle(self, *args, **options):
        data = json.load(options['input_file'])

        for place_id, place in data.items():
            try:
                restaurant = Restaurant.objects.get(id=place_id)
                self.stdout.write(f'Already exists: {restaurant}')
            except Restaurant.DoesNotExist:
                restaurant = Restaurant.objects.create(
                    id=place_id,
                    name=place['name'],
                    address=place['vicinity'],
                    lat=place['geometry']['location']['lat'],
                    lon=place['geometry']['location']['lng'],
                )

                self.stdout.write(f"Imported: {restaurant}")
