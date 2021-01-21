"""
Master:Chao
Datetime:2021/1/16 14:11
Reversion:1.0
File: serializers.py
"""
from rest_framework import serializers

from .models import Topic, Theme, Diary


class TopicSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Topic
        fields = "__all__"

    def validate(self, attrs):
        """
        fuc校验：自动向属性中添加用户信息，用户不能由前端数据传递
        :param attrs:
        :return:
        """
        attrs["user"] = self.context["request"].user
        return attrs


class ThemeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Theme
        fields = ["id", "user", "motif", "themetype"]

    def validate(self, attrs):
        attrs["user"] = self.context["request"].user
        return attrs

    def validate_motif(self, value):
        """
        fuc检验：用户与主题唯一
        :param value:
        :return:
        """
        if Theme.objects.filter(user=self.context["request"].user, motif=value).exists():
            raise serializers.ValidationError("已创建该主题")
        else:
            return value


class DiarySerializer(serializers.ModelSerializer):
    """
    展示日记主题相关内容：
    外键约束，不能添加read_only=True，需要指定queryset
    1、主键展示,主键默认id
    2、model模型类中def __str__函数展示
    3、展示任意字段，slug_field = 需要展示的model类中需要展示的字段
    4、展示外键的超链接地址
    5、展示外键模型类的所有字段
    """

    # theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all())
    # theme = serializers.StringRelatedField()
    theme = serializers.SlugRelatedField(slug_field="motif", queryset=Theme.objects.all())

    # theme = serializers.HyperlinkedRelatedField(view_name="daybook-detail", queryset=Theme.objects.all())
    # theme = ThemeSerializer()

    class Meta:
        model = Diary
        fields = ["id", "content", "create_time", "theme", "topic"]

    def validate(self, attrs):
        return attrs
