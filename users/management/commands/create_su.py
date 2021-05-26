from django.core.management.base import BaseCommand
from users.models import User
import os


class Command(BaseCommand):
    help = "This Command creates Super Users"

    def handle(self, *args, **options):
        try:
            User.objects.get(username="eb_admin")
        except User.DoesNotExist:
            User.objects.create_superuser("eb_admin", "dnstlr2933@naver.com", os.environ.get("SU_PASSWORD"))
            self.stdout.write(self.style.SUCCESS(f"Superuser is Created !"))
            return
        self.stdout.write(self.style.SUCCESS(f"Superuser is already exist"))

