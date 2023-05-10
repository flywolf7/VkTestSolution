from Friend.models import FriendRequest
from User.views import *


@csrf_exempt
def add_delete_friend(request):
    if request.method == "POST":
        data = request.GET
        from_id_id, to_id_id = data['from_id_id'], data['to_id_id']
        if FriendRequest.objects.extra(where=[f"from_id_id='{from_id_id}' OR from_id_id='{to_id_id}'",
                                              f"to_id_id='{to_id_id}' OR to_id_id='{from_id_id}'",
                                              "status='ACCEPTED'"]):
            return HttpResponse(f'<h1>{from_id_id} already friends with {to_id_id}<h1>')

        elif FriendRequest.objects.extra(where=[f"from_id_id='{from_id_id}'", f"to_id_id='{to_id_id}'"]):
            return HttpResponse(f'<h1>{from_id_id} already sent request for {to_id_id}<h1>')

        elif FriendRequest.objects.extra(where=[f"from_id_id='{to_id_id}'", f"to_id_id='{from_id_id}'"]):
            new = FriendRequest.objects.get(from_id=to_id_id, to_id=from_id_id, status="SENT")
            new1 = UserFriend(first_id=from_id_id, second_id=to_id_id)
            new.status = "ACCEPTED"
            new1.save()
            new.save()
            return HttpResponse(f'<h1>{from_id_id} now friends with {to_id_id}<h1>')
        else:
            add = FriendRequest.objects.create(from_id=from_id_id, to_id=to_id_id, status="SENT")
            return HttpResponse(f'<h1>{from_id_id} sent request for {to_id_id}<h1>')

    elif request.method == "DELETE":
        data = request.GET
        user_id, deleting_id = data['user_id'], data['deleting_id']
        FriendRequest.objects.extra(where=[f"from_id_id='{user_id}' OR to_id_id='{deleting_id}'"]).delete()
        UserFriend.objects.extra(where=[f"first_id='{user_id}' OR first_id='{deleting_id}'",
                                        f"second_id='{deleting_id}' OR second_id='{user_id}'"]
                                 ).delete()
        return HttpResponse('Successfully deleted')


def friend_status(request):
    if request.GET:
        data = request.GET
        user_id, checked_user_id = data['user_id'], data['checked_user_id']
        try:
            a = FriendRequest.objects.get(from_id=user_id, to_id=checked_user_id)
            if a.status == "SENT":
                return HttpResponse(f'<h1>{user_id} sent a friend request for {checked_user_id}<h1>')
            elif a.status == "ACCEPTED":
                return HttpResponse(f'<h1>{user_id} is friend for {checked_user_id}<h1>')
        except:
            try:
                a = FriendRequest.objects.get(from_id=checked_user_id, to_id=user_id)
                if a.status == "SENT":
                    return HttpResponse(f'<h1>{user_id} has a friend request from {checked_user_id}<h1>')
                elif a.status == "ACCEPTED":
                    return HttpResponse(f'<h1>{user_id} is friend for {checked_user_id}<h1>')
            except:
                return HttpResponse(f'<h1>{user_id} not a friend with {checked_user_id}<h1>')


def friend_list(request):
    if request.GET:
        data = request.GET
        user_id = int(data["user_id"])
        friends = str()
        for e in UserFriend.objects.all():
            if e.first_id == user_id:
                friends += " User - " + str(e.second_id) + ","
            elif e.second_id == user_id:
                friends += " User - " + str(e.first_id) + ","
        return HttpResponse(f'<h1>{friends} is all friends of {user_id}<h1>')
    return HttpResponse('<h1>friend list response<h1>')


def all_requests(request):
    if request.GET:
        data = request.GET
        user_id = int(data["user_id"])
        requests_from = ''
        requests_to = ''
        for e in FriendRequest.objects.all():
            if e.status == "SENT":
                if e.from_id == user_id:
                    requests_from += str(e.to_id) + ", "
                elif e.to_id == user_id:
                    requests_to += str(e.from_id) + ", "
        if len(requests_from) == 0 and len(requests_to) == 0:
            return HttpResponse('<h1>you dont have any requests from you and to you<h1>')
        return HttpResponse(f"""
        <h1>you have requests from users {requests_from[:-2]}<h1>\n<h1>you sent requests to users {requests_to[:-2]}<h1>
        """)
    return HttpResponse('<h1>all friends requests response<h1>')
