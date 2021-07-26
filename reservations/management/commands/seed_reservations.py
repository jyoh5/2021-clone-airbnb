import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservations_model
from users import models as users_model
from rooms import models as rooms_model


NAME = "reservations"


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """

        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_model.User.objects.all()
        rooms = rooms_model.Room.objects.all()

        seeder.add_entity(
            reservations_model.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "room": lambda x: random.choice(rooms),
                "guest": lambda x: random.choice(users),
                "check_in": lambda x: datetime.now()
                - timedelta(days=random.randint(0, 7)),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(1, 30)),
            },
        )

        seeder.execute()

        self.stdout.write(f"{number} {NAME} created!")
