"""
Master:Chao
Datetime:2021/1/15 15:56
Reversion:1.0
File: serializers.py
新建模型的序列化类
CustomUserSerializer：用户序列化类
CustomUserRegistSerializer：注册用户序列化类
CustomUserHeadPicSerializer：用户头像序列化类
"""

from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "introduce", "headpic", "email"]


class CustomUserRegistSerializer(serializers.ModelSerializer):
    verify_password = serializers.CharField(label="重复密码", write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'verify_password']

    def validate(self, attrs):
        verify_password = attrs.pop("verify_password")
        password = attrs.get("password")
        if verify_password != password:
            raise serializers.ValidationError("密码不一致")
        return attrs

    def create(self, validated_data):
        """
        创建用户
        :param validated_data:
        :return:用户
        """
        username = validated_data.__getitem__("username")
        email = validated_data.__getitem__("email")
        password = validated_data.__getitem__("password")
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        return user


class CustomUserHeadPicSerializer(serializers.ModelSerializer):
    headpic = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ["headpic"]


class CustomUserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password", "new_password2"]

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        new_password2 = attrs.get("new_password2")
        user = self.context["request"].user
        if user.check_password(old_password):
            if new_password == new_password2:
                return attrs
            else:
                raise serializers.ValidationError("密码不一致")
        else:
            raise serializers.ValidationError("原始密码错误")
