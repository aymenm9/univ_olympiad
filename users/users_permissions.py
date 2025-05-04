# creat acustom permissions for users

from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsHospital(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'Hospital'
    
class IsAPC(BasePermission):

    def has_permission(self, request, view):
        return request.user.info.Organization == 'APC'

class IsDSP(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'DSP'

    
class IsDSP_Hospital(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'DSP' or request.user.info.Organization == 'Hospital'

class IsDSP_APC(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'DSP' or request.user.info.Organization == 'APC'

class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.role == 'Worker' or request.user.info.role == 'Admin'
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.info.role == 'Admin'