from datetime import date, time, timedelta, datetime
from os import times
import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_countries import Countries
from django_countries.fields import CountryField
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This Command creates rooms"

    def add_arguments(self, parser):

        parser.add_argument(
            "--number", default=1, help="how many rooms do you want to create?"
        )

        pass

    def handle(self, *args, **options):

        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        ontime = datetime.now() - timedelta(
            hours=datetime.now().hour, minutes=datetime.now().minute
        )
        countries = []
        for c in CountryField().countries:
            countries.append(c)

        seeder.add_entity(
            room_models.Room,
            int(number),
            {
                "country": lambda x: random.choice(countries),
                "city": lambda x: seeder.faker.city(),
                "address": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 1000),
                "guests": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
                "check_in": lambda x: ontime + timedelta(hours=random.randint(13, 16)),
                "check_out": lambda x: ontime + timedelta(hours=random.randint(7, 11)),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(0, random.randint(2, 6)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 5)
                if magic_number == 1:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 1)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)
        self.stdout.write(self.style.SUCCESS(f"room {number} is Created !"))
