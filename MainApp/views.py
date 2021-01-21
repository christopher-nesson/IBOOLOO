# 身份验证和权限
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from IBOOLOO.authentication import NoCsrfSessionAuthentication
from IBOOLOO.pagination import SuperPageNumberPagination
# 扩展的认证类
from IBOOLOO.permissions import IsSuperAdminUser
from .models import Topic, Theme, Diary
from .serializers import TopicSerializer, ThemeSerializer, DiarySerializer


# Create your views here.
class TopicViewSets(ModelViewSet):
    """
    话题的视图集
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['create_time', 'id']
    search_fields = ['info', 'img']
    ordering_fields = ['create_time', 'id']
    # queryset = Topic.objects.filter(check="1")
    serializer_class = TopicSerializer
    authentication_classes = [BasicAuthentication, NoCsrfSessionAuthentication, JWTAuthentication,
                              SessionAuthentication]

    def get_queryset(self):
        """
        :return: 查询集
        """
        topic = Topic.objects.all()
        if self.request.user.is_superuser:
            return topic
        else:
            return Topic.objects.filter(check="1")

    # 默认许可类
    # permission_classes = [IsAdminUser]
    def get_permissions(self):
        """
        如果请求的方式GET(list,获得话题列表)，返回话题列表倒序
        elif 的请求为 PUT(update) PATCH(partial_update)修改话题 GET(retrieve获得指定id的话题)为普通管理员的权限范围，
        else 的请求诶 POST(create) DEL(destroy) 为超级管理员的权限，只有其才能增加和删除
        :return: 权限 AllowAny:所有人  IsAdminUser:管理员  IsSuperAdminUser:超级管理员
        """
        if self.action == "list":
            return [AllowAny()]
        elif self.action == "create_topic_diary" or self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "retrieve"]:
            return [IsAdminUser()]
        else:
            return [IsSuperAdminUser()]

    """
    detail 代表是列表路由后拼接  或者是详情路由后拼接
    detail False /topics/current
    detail True  /topics/101/current
    """

    # /topics/1/create_topic_diary
    @action(methods=["post"], detail=True)
    def create_topic_diary(self, request, pk):
        try:
            topic = Topic.objects.get(id=int(pk))
        except(TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 需要跟model字段保持一致，在postman中请求也一致
        seria = DiarySerializer(data=request.data)
        if seria.is_valid():
            instance = seria.save()
            instance.topic = topic
            instance.save()
            return Response(seria.data, status=status.HTTP_201_CREATED)
        else:
            return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["put"], detail=True)
    def check_publish(self, request):
        """
        超级管理员审核用户话题的function
        :param request:
        :return:
        """
        global queryset
        if self.request.user.is_superuser:
            queryset = Topic.objects.all()
        else:
            queryset = Topic.objects.filter(check="1")
        return queryset


class ThemeViewSets(ModelViewSet):
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        用户的查询集必须为自己的日记本主题列表
        超级管理员可看所有人的日记主题列表
        :return: 查询集
        """
        theme = Theme.objects.all()
        if self.request.user.is_superuser:
            return theme
        else:
            return Theme.objects.filter(user=self.request.user)

    @action(detail=True)
    def get_diarys(self, request, pk):
        """
        获取主题下的日记
        :param request: 请求
        :param pk: 用户id
        :return: 当前请求用户的当前日记主题所有日记数据
        """
        try:
            theme = Theme.objects.get(id=int(pk))
            seria = DiarySerializer(instance=theme.diary_set.all(), many=True)
            return Response(seria.data)
        except (TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)


class DiaryViewSets(GenericViewSet, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin,
                    ListModelMixin):
    """
    日记视图集
    """

    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    ordering_fields = ['create_time', 'id']

    def get_permissions(self):
        if self.action in ["create", "partial_update", "retrieve", "update", "destroy"]:
            return [IsAuthenticated()]
        else:
            return []

    @action(methods=["get"], detail=False, pagination_class=SuperPageNumberPagination)
    def get_latest(self, request, **kwargs, ):
        """
        获取最新日记
        :param request:get请求
        :param kwargs:
        :return:分页过的最新日记或不够分页的日记
        """
        from datetime import date
        diarys = Diary.objects.filter(create_time__date=date.today()).order_by("-create_time")

        if self.paginator:
            # 分页过的最新日记
            paged_diarys = self.paginate_queryset(diarys)
            seria = DiarySerializer(instance=paged_diarys, many=True)
            paged_seriadata = self.get_paginated_response(seria.data)
            return paged_seriadata
        else:
            seria = DiarySerializer(instance=diarys, many=True)
            return Response(seria.data)
