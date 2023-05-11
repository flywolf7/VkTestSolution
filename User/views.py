from django.db import transaction
from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User.serializers import *


def main_page(request):
    return HttpResponse(f'<h1>You are not a user, you need to register<h1>')


@api_view(['POST'])
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = request.data
        try:
            username, password = data["username"], data["password"]
            new_user = User(username=username, password=password)
            new_user.save()
            return Response({"registered user": f"{new_user.pk}"})
        except Exception:
            return Response({"Details": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@csrf_exempt
def add_delete_friend(request):
    if request.method == "POST":
        data = request.data
        from_id_id, to_id_id = data['from_id_id'], data['to_id_id']
        if FriendRequest.objects.extra(where=[f"from_id_id='{from_id_id}' OR from_id_id='{to_id_id}'",
                                              f"to_id_id='{to_id_id}' OR to_id_id='{from_id_id}'",
                                              "status='ACCEPTED'"]):
            return Response({"detail": f'{from_id_id} already friends with {to_id_id}'},
                            status=status.HTTP_409_CONFLICT)

        elif FriendRequest.objects.extra(where=[f"from_id_id='{from_id_id}'", f"to_id_id='{to_id_id}'"]):
            return Response({"detail": f"{from_id_id} already sent request for {to_id_id}"},
                            status=status.HTTP_409_CONFLICT)

        elif FriendRequest.objects.extra(where=[f"from_id_id='{to_id_id}'", f"to_id_id='{from_id_id}'"]):
            atomic_db(
                FriendRequest.objects.get(from_id_id=to_id_id, to_id_id=from_id_id, status="SENT"),
                UserFriend(first_id_id=from_id_id, second_id_id=to_id_id),
                UserFriend(first_id_id=to_id_id, second_id_id=from_id_id),
            )
            return Response({"detail": f'{from_id_id} now friends with {to_id_id}'})
        else:
            try:
                FriendRequest.objects.create(from_id_id=from_id_id, to_id_id=to_id_id, status="SENT")
                return Response({"detail": f'Friend add from {from_id_id} request successfully sent for {to_id_id}'})
            except:
                return Response({"detail": f"Any requested User not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        data = request.GET
        user_id, deleting_id = data['user_id'], data['deleting_id']
        atomic_db(
            FriendRequest.objects.extra(where=[f"from_id_id='{user_id}' OR to_id_id='{deleting_id}'"]),
            UserFriend.objects.extra(where=[f"first_id_id='{user_id}'", f"second_id_id='{deleting_id}'"]),
            UserFriend.objects.extra(where=[f"first_id_id='{deleting_id}'", f"second_id_id='{user_id}'"]),
        )
        return Response({"detail:": "Friend is successfully deleted"})
    else:
        return Response({"detail": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def friend_status(request):
    if request.GET:
        data = request.data
        user_id, checked_user_id = data['user_id'], data['checked_user_id']
        try:
            if FriendRequest.objects.extra(where=[f"from_id_id='{user_id}'", f"to_id_id='{checked_user_id}'"]):
                friendship = f"{user_id} have a request from {checked_user_id}"
            elif FriendRequest.objects.extra(where=[f"from_id_id='{checked_user_id}'", f"to_id_id='{user_id}'"]):
                friendship = f"{checked_user_id} have a request from {user_id}"
            else:
                friendship = "No one have a requests"
            return Response({"details": friendship})
        except:
            return Response({"details": "User with passed ID not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"details": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def friend_list(request):
    if request.GET:
        data = request.GET
        user_id = int(data['user_id'])
        friends = str()
        try:
            UserFriend.objects.extra(where=[f"first_id_id='{user_id}' OR first_id_id='{user_id}'"])
        except:
            return Response({"details": "User with passed ID not found"}, status=status.HTTP_404_NOT_FOUND)
        for e in UserFriend.objects.all():
            if e.first_id_id == user_id:
                friends += "User " + str(e.second_id_id) + ","
            elif e.second_id_id == user_id:
                friends += "User " + str(e.first_id_id) + ","
        return Response({f"{user_id} friends": friends})
    else:
        return Response({"details": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_requests(request):
    if request.GET:
        data = request.GET
        user_id = int(data['user_id'])
        try:
            FriendRequest.objects.extra(where=[f"from_id_id='{user_id}' OR to_id_id='{user_id}'"])
        except:
            return Response({"details": "User with passed ID not found"}, status=status.HTTP_404_NOT_FOUND)
        requests_from = ''
        requests_to = ''
        for e in FriendRequest.objects.all():
            if e.status == "SENT":
                if e.from_id_id == user_id:
                    requests_from += str(e.to_id_id) + ", "
                elif e.to_id_id == user_id:
                    requests_to += str(e.from_id_id) + ", "
        if len(requests_from) == 0 and len(requests_to) == 0:
            return Response({"details": "you dont have any requests"})
        return Response({
            "You have requests from": requests_from[:-2],
            "You sent requests for": requests_to[:-2]
        })
    else:
        Response({"details": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)


@transaction.atomic
def atomic_db(req, obj_1, obj_2, obj_3):
    if req == "DELETE":
        obj_1.delete()
        obj_2.delete()
        obj_3.delete()
    elif req == "POST":
        obj_1.status = 'ACCEPTED'
        obj_1.save()
        obj_2.save()
        obj_3.save()


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')


def bad_request(request, exception):
    return HttpResponseNotFound('<h1>Неверные данные<h1>')


def method_not_allowed(request, exception):
    return HttpResponseNotFound('<h1>Метод не разрешен<h1>')


def conflict(request, exception):
    return HttpResponseNotFound('<h1>Конфликт данных<h1>')


def internal_error(request, *args):
    return HttpResponseNotFound('<h1>Ошибка<h1>')
