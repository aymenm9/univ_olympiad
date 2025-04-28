# creat acustom permissions for users

from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsHospital(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'hospital'
    
class IsDSP_APC(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'APC' or request.user.role == 'DSP'