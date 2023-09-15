from django.http import JsonResponse
from rest_framework import status


class MissingUniqueFormKey(Exception):
    pass


class TooManyUniqueFormKeys(Exception):
    pass


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, MissingUniqueFormKey):
            return JsonResponse(
                {"__all__": ["Missing unique form key."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif isinstance(exception, TooManyUniqueFormKeys):
            return JsonResponse(
                {"__all__": ["Too many unique form keys."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
