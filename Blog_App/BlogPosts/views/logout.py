
from django.contrib.auth import logout

from django.shortcuts import  redirect


def user_logout(reqeust):
    logout(reqeust)

    return redirect('Dashboard')
