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
            "No Shower After 10 P.M.",
            "No Laundry After 10 P.M.",
            "No Cook After 10 P.M.",
            "Smokey Dishes Are Restricted",
            "Don't Make Too Much Noise",
            "Let's Be Considerate Of Our Neighbors"
        ]
        for rule in rules:
            room_models.HouseRule.objects.create(name=rule)
        self.stdout.write(self.style.SUCCESS(f"house_rules {len(rules)} is Created !"))
