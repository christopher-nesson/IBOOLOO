from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    """
    继承Django自带的用户基类，扩展自定义属性
    :exception 设定三个用户admin root temp设定权限
    """
    email = models.EmailField(unique=True, verbose_name="邮箱")
    headpic = models.ImageField(upload_to="user/headpic", default="user/headpic/default.png", verbose_name="用户头像"
                                )
    introduce = models.CharField(max_length=60, null=True, blank=True, verbose_name="自我介绍")
