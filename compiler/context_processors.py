from .models import Collaboration,Customer
from django.http import HttpResponse
from django.shortcuts import render, redirect 
from .decorators import unauthenticated_user, allowed_users, admin_only


def notify(request):
    notify = 0

    try:
        author = Customer.objects.get(user=request.user)
        notify= Collaboration.objects.filter(members=author,Accepter=False).count()
    except:
        pass

    return dict(notify=notify)
   

