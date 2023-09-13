import typing as t

from common.helpers.generators import get_hashed_login_id
from common.models import Student
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest

User = get_user_model()


class DependentStudentBackend(BaseBackend):
    def authenticate(
        self,
        request: HttpRequest,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        classId: t.Optional[str] = None,
        **kwargs
    ) -> t.Optional[AbstractBaseUser]:
        if username is None or password is None or classId is None:
            return

        try:
            user = User.objects.get(
                username=username,
                new_student__class_field__access_code=classId,
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return

    def get_user(self, user_id: int) -> t.Optional[AbstractBaseUser]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return


class DependentStudentTokenBackend(BaseBackend):
    def authenticate(
        self,
        request: HttpRequest,
        user_id: t.Optional[int] = None,
        login_id: t.Optional[str] = None,
        **kwargs
    ) -> t.Optional[AbstractBaseUser]:
        user = self.get_user(user_id)
        if user:
            # Check the url against the student's stored hash.
            student = Student.objects.get(new_user=user)
            if (
                student.login_id
                and get_hashed_login_id(login_id) == student.login_id
            ):
                return user

    def get_user(self, user_id: int) -> t.Optional[AbstractBaseUser]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return
