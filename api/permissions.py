from codeforlife.user.models import User
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class UserHasSessionAuthFactors(BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            isinstance(request.user, User)
            and request.user.session.session_auth_factors.exists()
        )
