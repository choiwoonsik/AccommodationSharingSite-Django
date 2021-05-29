from os import times
from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This Command creates facilities"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):

        facilities = [
            "Private entrance",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for facility in facilities:
            room_models.Facility.objects.create(name=facility)
        self.stdout.write(
            self.style.SUCCESS(f"Facilities {len(facilities)} is Created !")
        )
