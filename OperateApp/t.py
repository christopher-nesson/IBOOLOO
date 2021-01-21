from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


# Create your views here.

class RelationshipViewSets(viewsets.GenericViewSet):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Relationship.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == "get_follows":
            return RelationshipSerializer(*args, **kwargs)
        elif self.action == "set_relation":
            return RelationshipSetSerializer(*args, **kwargs)

    @action(methods=["post"], detail=False)
    def set_relation(self, request):
        seria = self.get_serializer(data=request.data)
        seria.is_valid(raise_exception=True)
        try:
            data = Relationship.objects.get(user=request.user, target=seria.validated_data.get("target"))
            if data.state == seria.validated_data.get("state"):
                data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                data.state = seria.validated_data.get("state")
                data.save()
                # 如果state==1 需要向消息表写入关注信息
                if seria.validated_data.get("state") == "1":
                    msg = Message()
                    msg.origin = request.user
                    msg.target = seria.validated_data.get("target")
                    msg.messagetype = "1"
                    msg.save()
                seria = self.get_serializer(instance=data)
                return Response(seria.data)
        except Exception as e:
            seria.save()
            if seria.validated_data.get("state") == "1":
                msg = Message()
                msg.origin = request.user
                msg.target = seria.validated_data.get("target")
                msg.messagetype = "1"
                msg.save()
            # 如果state==1 需要向消息表写入关注信息
            return Response(seria.data)

    @action(methods=["get"], detail=False)
    def get_follows(self, request):
        follows = Relationship.objects.filter(user=request.user, state="1")
        seria = self.get_serializer(instance=follows, many=True)
        return Response(seria.data)


class MessageViewSets(viewsets.GenericViewSet, mixins.ListModelMixin):
    def get_queryset(self):
        return Message.objects.filter(target=self.request.user)

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer(self, *args, **kwargs):
        return MessageSerializer(*args, **kwargs)


class ReplyViewSets(viewsets.GenericViewSet, mixins.CreateModelMixin):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Reply.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return ReplySerializer(*args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        msg = Message()
        msg.origin = instance.user
        msg.target = instance.diary.diarybook.user
        msg.messagetype = "2"
        msg.replay = instance
        msg.save()
