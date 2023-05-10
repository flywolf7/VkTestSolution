from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from User.models import *


def main_page(request):
    return HttpResponse(f'<h1>You are not a user, you need to register<h1>')


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = request.GET
        username, password = data["username"], data["password"]
        new_user = User(username=username, password=password)
        new_user.save()
        return HttpResponse(f'<h1>user with username "{username}" successfully registered!<h1>')
    else:
        return bad_request


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')


def bad_request(request, exception):
    return HttpResponseNotFound('<h1>Неверные данные<h1>')


def method_not_allowed(request, exception):
    return HttpResponseNotFound('<h1>Метод не разрешен<h1>')


def conflict(request, exception):
    return HttpResponseNotFound('<h1>Конфликт данных<h1>')


def internal_error(request, *args):
    return HttpResponseNotFound('<h1>Ошибка Базы данных<h1>')
