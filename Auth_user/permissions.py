from rest_framework.permissions import BasePermission
from .models import CoreUser
from rest_framework.permissions import IsAuthenticated

class IsClientOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method not in ['GET','POST']:
            return False
        if hasattr(request.user,'is_client'):
            if not request.user:
                return False
        return True
     
    
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','POST','PUT','DELETE']:
            return True
        if hasattr(request.user,'is_admin'):
            if not request.user:
                return False
        return True
    

class IsEmployeeOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method not in ['GET','POST']:
            return False
        if hasattr(request.user,'is_employee'):
            if not request.user:
                return False
        return True 



class CombinedPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.is_admin:
                return True
            elif user.is_employee:
                if request.method in ['GET', 'POST', 'PUT']:
                    return True
            elif user.is_client:
                if request.method in ['GET','POST']:
                    return True
        return False