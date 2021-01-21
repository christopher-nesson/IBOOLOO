from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from IBOOLOO.permissions import IsSuperAdminUser
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserRegistSerializer, CustomUserPasswordSerializer, \
    CustomUserHeadPicSerializer


# Create your views here.
class CustomUserViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action in ["setheadpic", "setpassword", "getuserinfo"]:
            return [IsAuthenticated()]
        else:
            return [IsSuperAdminUser()]

    def get_serializer(self, *args, **kwargs):
        """
        重写父类中获取序列化类需要 给context赋值
        :param args:
        :param kwargs:
        :return:
        """
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == "create":
            return CustomUserRegistSerializer(*args, **kwargs)
        elif self.action == "setheadpic":
            return CustomUserHeadPicSerializer(*args, **kwargs)
        elif self.action == "setpassword":
            return CustomUserPasswordSerializer(*args, **kwargs)
        elif self.action == "getuserinfo":
            return CustomUserSerializer(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def getuserinfo(self, request):
        """
        获取用户详情
        :param request: 当前登录用户请求
        :return: 当前登录用户请求数据
        """
        seria = CustomUserSerializer(instance=request.user)
        return Response(seria.data)

    @action(methods=["patch"], detail=False)
    def setheadpic(self, request, *args, **kwargs):
        """
        设置用户头像
        :param request: 当前登录用户请求
        :param args:
        :param kwargs:
        :return:
        """
        seria = self.get_serializer(data=request.data, *args, **kwargs)
        seria.is_valid(raise_exception=True)
        request.user.headpic = seria.validated_data.get("headpic")
        request.user.save()
        seria2 = CustomUserSerializer(instance=request.user)
        return Response(seria2.data)

    @action(methods=["patch"], detail=False)
    def setpassword(self, request, *args, **kwargs):
        """
        设置用户密码
        :param request: 当前登录用户请求
        :param args:
        :param kwargs:
        :return:
        """
        seria = self.get_serializer(data=request.data, *args, **kwargs)
        seria.is_valid(raise_exception=True)
        request.user.set_password(seria.validated_data.get("new_password"))
        request.user.save()
        seria2 = CustomUserSerializer(instance=request.user)
        return Response(seria2.data)
