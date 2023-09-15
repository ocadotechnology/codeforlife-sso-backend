import typing as t

from common.helpers.generators import get_hashed_login_id
from common.models import Student
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.handlers.wsgi import WSGIRequest

User = get_user_model()


class UserIdAndLoginIdBackend(BaseBackend):
    def authenticate(
        self,
        request: WSGIRequest,
        user_id: t.Optional[int] = None,
        login_id: t.Optional[str] = None,
        **kwargs
    ) -> t.Optional[AbstractBaseUser]:
        if user_id is None or login_id is None:
            return

        user = self.get_user(user_id)
        if user and getattr(user, "is_active", True):
            # Check the url against the student's stored hash.
            student = Student.objects.get(new_user=user)
            if (
                student.login_id
                # TODO: refactor this
                and get_hashed_login_id(login_id) == student.login_id
            ):
                return user

    def get_user(self, user_id: int) -> t.Optional[AbstractBaseUser]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return
