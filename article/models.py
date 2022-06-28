from django.db import models
from django.utils import timezone

# Create your models here.
#아직 완성되지 않은 모델입니다. migrate 하지 말아주세요^^
class Article(models.Model):
    title = models.CharField("제목", max_length=200)
    # user = models.ForeignKey(
    #     'user.User', verbose_name="작성자", on_delete=models.CASCADE)
    is_active = models.BooleanField("", default=True)
    # tags = TaggableManager()
    exposure_end_date = models.DateField("노출종료일", default=timezone.now)
    image_location = models.CharField("이미지 주소", max_length=200, null=True)
    image = models.ImageField("이미지", upload_to='uploads/', null=True)


    # def __str__(self):
    #     return f"{self.user.username} 님이 작성하신 글입니다."