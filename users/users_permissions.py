# creat acustom permissions for users

from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsHospital(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'hospital'
    
class IsAPC(BasePermission):

    def has_permission(self, request, view):
        return request.user.info.Organization == 'APC'

class IsDSP(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'DSP'

    
class IsDSP_Hospital(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.Organization == 'DSP' or request.user.info.Organization == 'hospital'


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.info.role == 'worker'
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.info.role == 'Admin'