from django.shortcuts import render


def render_react(request):
    return render(request, "my_app_react.html")
