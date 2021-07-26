import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as lists_model
from users import models as users_model
from rooms import models as rooms_model


NAME = "lists"


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
            lists_model.List,
            number,
            {
                # "rooms": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )

        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            tmp_model = lists_model.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            tmp_model.rooms.add(*to_add)

        self.stdout.write(f"{number} lists created!")
