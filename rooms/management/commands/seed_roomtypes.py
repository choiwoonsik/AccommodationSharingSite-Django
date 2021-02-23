from os import times
from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This Command creates roomtypes"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):

        roomtypes = [
            "House",
            "Flat",
            "Bed and breakfast",
            "Boutique hotel",
            "Bungalow",
            "Cabin",
            "Cottage",
            "Guest house",
            "Guest suite",
            "Hostel",
            "Hotel",
            "Loft",
            "Resort",
            "Serviced apartment",
            "Townhouse",
            "Villa",
        ]
        for type in roomtypes:
            room_models.RoomType.objects.create(name=type)
        self.stdout.write(self.style.SUCCESS(f"roomtype {len(roomtypes)} is Created !"))
