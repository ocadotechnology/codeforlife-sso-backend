import typing as t

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest

User = get_user_model()


class TeacherOrIndependentStudentBackend(BaseBackend):
    def authenticate(
        self,
        request: HttpRequest,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        **kwargs
    ) -> t.Optional[AbstractBaseUser]:
        return super().authenticate(request, username, password, **kwargs)

    def get_user(self, user_id: int) -> t.Optional[AbstractBaseUser]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return
