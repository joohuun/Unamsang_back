from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
import datetime

# Create your models here.
#아직 완성되지 않은 모델입니다. migrate 하지 말아주세요^^
class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True #abstractbaseclass가 되도록


class Article(BaseModel):
    title = models.CharField("제목", max_length=200)
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField("공개 여부", default=True)
    tags = TaggableManager("태그",blank=True)
    exposure_end_date = models.DateField("노출 종료일", default=(datetime.date.today() + datetime.timedelta(days=300)))
    image_location = models.CharField("이미지 주소", max_length=200, null=True, blank=True)
    image = models.ImageField("이미지", upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return f"Article:{self.title}"


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name="원글", on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    comment = models.TextField("댓글 내용")

    def __str__(self):
        return f"{self.user.username} 님 댓글입니다."
    
    
class Rating(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.SET_NULL, null=True)
    article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField("평점", null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}/{self.rating}점" 
    