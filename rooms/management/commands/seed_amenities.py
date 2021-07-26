from django.core.management.base import BaseCommand
from rooms.models import Amenity


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
        amenities = [
            "주방",
            "난방",
            "에어컨",
            "세탁기",
            "건조기",
            "무선 인터넷",
            "아침식사",
            "실내 벽난로",
            "다리미",
            "헤어드라이어",
            "업무 전용 공간",
            "TV",
            "아기 침대",
            "유아용 식탁의자",
            "셀프 체크인",
            "화재경보기",
            "일산화탄소 경보기",
            "욕실 단독 사용",
            "해변에 인접",
            "수변에 인접",
        ]

        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write("Amenities created!")
