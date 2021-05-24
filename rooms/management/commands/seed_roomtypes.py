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
            "Guest house",
            "Hotel",
            "Resort",
            "Villa",
        ]
        for type in roomtypes:
            room_models.RoomType.objects.create(name=type)
        self.stdout.write(self.style.SUCCESS(f"roomtype {len(roomtypes)} is Created !"))
