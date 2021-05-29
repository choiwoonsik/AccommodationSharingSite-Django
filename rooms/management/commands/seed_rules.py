from os import times
from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This Command creates house_rules"

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):

        rules = [
            "Pets Allowed",
            "NonSmoking Area",
        ]
        for rule in rules:
            if room_models.HouseRule.objects.get_or_none(name=rule) is None:
                room_models.HouseRule.objects.create(name=rule)
        self.stdout.write(self.style.SUCCESS(f"house_rules {len(rules)} is Created !"))
