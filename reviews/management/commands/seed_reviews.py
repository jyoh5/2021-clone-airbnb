import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as reviews_model
from users import models as users_model
from rooms import models as rooms_model


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """

        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_model.User.objects.all()
        rooms = rooms_model.Room.objects.all()

        seeder.add_entity(
            reviews_model.Review,
            number,
            {
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(f"{number} reviews created!")
