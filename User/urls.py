from django.urls import path

from .views import *

urlpatterns = [
    path('', add_delete_friend),
    path('status/', friend_status),
    path('list/', friend_list),
    path('all_requests/', all_requests),
    path('register/', register),
]
