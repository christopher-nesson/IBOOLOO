"""
Master:Chao
Datetime:2021/1/15 17:44
Reversion:1.0
File: permissions.py
自定义权限认证类
"""
from rest_framework.permissions import BasePermission


class IsSuperAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
