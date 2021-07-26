import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """

        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 10),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )

        # 생성된 room의 pk 얻기
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        for pk in created_clean:
            tmp_room = room_models.Room.objects.get(pk=pk)

            # 생성된 room에 사진 추가하기
            for i in range(3, random.randint(10, 15)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=tmp_room,
                    file=f"room_photos/{random.randint(10,17)}.jpg",
                )

            # 생성된 room에 amenities 추가하기
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    tmp_room.amenities.add(a)

            # 생성된 room에 facilities 추가하기
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    tmp_room.facilities.add(f)

            # 생성된 room에 house_rule 추가하기
            for f in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    tmp_room.house_rules.add(f)

        self.stdout.write(f"{number} rooms created!")
