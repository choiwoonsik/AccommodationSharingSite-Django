from os import times
from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This Command creates amenities"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Chairs",
            "Children Area",
            "Cooking hob",
            "Dishwasher",
            "Double bed",
            "Free Parking",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for amenity in amenities:
            if room_models.Amenity.objects.get_or_none(name=amenity) is None:
                room_models.Amenity.objects.create(name=amenity)
        self.stdout.write(
            self.style.SUCCESS(f"Amenities {len(amenities)} is Created !")
        )
