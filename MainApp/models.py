from django.db import models

from DjangoUeditor.models import UEditorField
from UserApp.models import CustomUser

STATE = (
    ("0", "公开主题"),
    ("1", "隐私主题"),

)

CHECK = (
    ("0", "未通过审核"),
    ("1", "通过审核"),
)


# Create your models here.

class Topic(models.Model):
    """
    话题模型类
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="所属用户")
    title = models.CharField(max_length=7, verbose_name="话题名称")
    describe = models.CharField(max_length=18, verbose_name="话题介绍")
    img = models.ImageField(upload_to="topic/", default="topic/default.png", verbose_name="话题配图")
    info = models.CharField(max_length=230, null=True, blank=True, verbose_name="话题内容")
    create_time = models.DateField(auto_now_add=True, verbose_name="发布时间")
    check = models.CharField(max_length=1, choices=CHECK, verbose_name="是否通过审核", default="0")

    def __str__(self):
        return self.title + "\n" + self.describe

    class Meta:
        ordering = ["-id"]
        unique_together = ["title"]
        # managed = False


class Theme(models.Model):
    """
    主题详情类
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="所属用户")
    motif = models.CharField(max_length=14, verbose_name="主题名称")
    themetype = models.CharField(max_length=1, choices=STATE, verbose_name="主题类型", default="0")

    def __str__(self):
        return self.user.username + "的主题" + self.motif

    class Meta:
        unique_together = ["user", "motif"]


class Diary(models.Model):
    """
    日记模型类
    """
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name="所属主题")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, verbose_name="所属话题", null=True, blank=True)
    content = UEditorField(verbose_name="日记内容", imagePath="diaryimage/", filePath="diaryfile/")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:200]
