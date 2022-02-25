from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedMixin

# from pyexpat import model


# Create your models here.

# 가장 우선적으로 주가 되는 클래스가
# Mixin -> 확장하는 기능을 하는 클래스
# 우측으로 갈수록 상위 클래스
# 즉 mixin 클래스가 앞에 와야함

# AbstractBaseUser - > AbstractUser - > User


class User(TimeStampedMixin, PermissionsMixin, AbstractBaseUser):

    # email -> 카카오 에서 가져옴
    # username - > 기본값 -> (카카오에서 가져온 닉네임)
    # is_staff
    # 이메일필드 ( unique, verbose_name)

    email = models.EmailField(verbose_name=_("email"), max_length=80, unique=True)
    username = models.CharField(verbose_name=_("username"), max_length=30)
    is_staff = models.BooleanField(verbose_name=_("is_staff"), default=False)
    is_active = models.BooleanField(verbose_name=_("is_active"), default=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name_plural = _("user")
        db_table = "user"

    def __str__(self) -> str:
        return self.email
