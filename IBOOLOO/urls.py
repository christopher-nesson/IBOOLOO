"""
IBOOLOO URL Configuration
    使用使用DRF注册资源，生成对应资源的路由
    Examples:
        router = DefaultRouter()
        此处basename有无取决于是否复写继承序列化类的fuc()
        router.register("examples", ExamplesViewSet, basename="example")

"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
# 获取刷新验证JWT
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify

from MainApp.views import TopicViewSets, ThemeViewSets, DiaryViewSets
from OperateApp.views import RelationshipViewSet, ReplyViewSet, MessageViewSet
from UserApp.views import CustomUserViewSets
from .settings import MEDIA_ROOT

router = DefaultRouter()
router.register("customusers", CustomUserViewSets, basename="customuser")
router.register("topics", TopicViewSets, basename="topic")
router.register("themes", ThemeViewSets, basename="theme")
router.register("diarys", DiaryViewSets, basename="diary")
router.register("replys", ReplyViewSet, basename="reply")
router.register("relationships", RelationshipViewSet, basename="relationship")
router.register("messages", MessageViewSet, basename="message")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('', include(router.urls)),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWT路由用于获取token的路由obtain
    path('obtainjwt/', token_obtain_pair),
    # JWT路由用于刷新token的路由refresh
    path('refreshjwt/', token_refresh),
    # JWT路由用于验证token的路由verify
    path('verifyjwt/', token_verify),

]
