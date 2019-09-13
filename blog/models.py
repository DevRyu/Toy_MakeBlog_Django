from django.db import models
from helper.models import BaseModel
from users.models import User


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.id, self.title)
    # 쿼리셋 리턴값 문자로 변환되게 (어드민에서 에서 실제 {{}}형식이 아닌텍스트로)정의
