from django.db import models


# Create your models here.
class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)  # 모델 생성 시 시간 저장
    updated = models.DateTimeField(auto_now=True)  # 모델 저장 시 시간 저장

    # TimeStampedModel은 데이터베이스와 등록되지 않아야 함(==추상모델)이것을 위한 설정
    class Meta:
        abstract = True
