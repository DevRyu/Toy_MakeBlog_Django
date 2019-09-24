from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose'),
)


class UserManager(BaseUserManager):
    # 베이스유저메니저 열어보면 크리에이트유저,슈퍼유저가 들어가 있음
    # 이메일을 받기 위해서
    # 아래는 이메일로 로그인하기 위해 유효성 검사를 만드는것
    # 코드 중복 제거하기
    def _create_user(self, email, username, password, gender=2, **extra_fields):
        # 처음에 _(언더바를)붙이는 건 클래스 내에서만 쓰겟다는 목적인 것이다.
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username,
                          gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, 'blog/like_section.html',  password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)  # 이메일은 유니크하게
    username = models.CharField(max_length=30)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)

    objects = UserManager()  # 위의 클래스 받음
    USERNAME_FIELD = 'email'  # 유저네임을 이메일로 치환을
    REQUIRED_FIELDS = []  # 필수로 받고 싶은 필드를 넣기위한 칸
    # 원래 소스코드에는 email 필드지만 로그인을 이메일로 하니까 또 요구할필요없음

    def __str__(self):
        return "<%d %s>" % (self.pk, self.email)
