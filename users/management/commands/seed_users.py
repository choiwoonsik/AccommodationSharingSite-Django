from os import times
from django.core.management.base import BaseCommand
from django.template.defaultfilters import default
from django_seed import Seed
from users import models as user_models


class Command(BaseCommand):
    help = "This Command creates users"

    def add_arguments(self, parser):

        parser.add_argument("--number", help="how many users do you want to create?")

        pass

    def handle(self, *args, **options):

        number = options.get("number")

        if user_models.User.objects.all().count() >= int(number):
            return None

        seeder = Seed.seeder()
        seeder.add_entity(
            user_models.User, int(number), {"is_staff": False, "is_superuser": False}
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"user {number} is Created !"))
