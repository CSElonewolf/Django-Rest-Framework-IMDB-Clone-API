from rest_framework import permissions


# check if the user is admin or not , only then it allows POTS,PUT,DELETE request
class AdminOrReadOnly(permissions.IsAdminUser):
	def has_permission(self,request,view):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):
	def has_object_permission(self,request,view,obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.review_user == request.user