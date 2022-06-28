from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.
#아직 완성되지 않은 모델입니다. migrate 하지 말아주세요^^
class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True #abstractbaseclass가 되도록


class Article(BaseModel):
    title = models.CharField("제목", max_length=200)
    # user = models.ForeignKey(
    #     'user.User', verbose_name="작성자", on_delete=models.CASCADE)
    is_active = models.BooleanField("공개 여부", default=True)
    tags = TaggableManager("태그",blank=True)
    exposure_end_date = models.DateField("노출 종료일", default=timezone.now)
    image_location = models.CharField("이미지 주소", max_length=200, null=True)
    image = models.ImageField("이미지", upload_to='uploads/', null=True)


    def __str__(self):
        return f"Article:{self.title}"