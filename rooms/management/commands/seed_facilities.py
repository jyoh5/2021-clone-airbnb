from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """

        # parser.add_argument(
        #     "--times",
        #     help="How many times do you want me to tell you that I love you?",
        # )

    def handle(self, *args, **options):
        facilities = [
            "건물 내 무료 주차",
            "헬스장",
            "자쿠지",
            "수영장",
            "전기차(EV) 충전시설",
        ]

        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write("Facilities created!")
