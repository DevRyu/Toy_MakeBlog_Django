from django.db import models
from helper.models import BaseModel
from users.models import User
# from taggit.managers import TaggableManager


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.id, self.title)
    # 쿼리셋 리턴값 문자로 변환되게 (어드민에서 에서 실제 {{}}형식이 아닌텍스트로)정의


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 댓글달릴 글의 외래키
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 댓글단 유저의 외래키
    content = models.TextField()
    # 댓글 내용
    image = models.ImageField(blank=True, null=True)
    # 차이점은: Null의 경우 DB와 관련이 되어있고 데이터 베이이스 컬럼이 널을 가질건지 아닌지 가진다
    # blank의 경우 유효성검사에서 할지 안할지
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    # 유저클래스와 이어서 여러유저가 여러라이크를 누르는데 토글로 막을거임
    # 어터케 M대M이쥬? M대1아닌가 각 유저들당 하나의 좋아요만 누르면되는거 아님?
    # tags = TaggableManager()
    #

    def __str__(self):
        return '%s - %s' % (self.id, self.user)

    def total_likes(self):
        return self.likes.count()
        # 총 좋아요 카운트
