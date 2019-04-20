from django.shortcuts import render
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import os

# Create your views here.
@login_required
def index(request):
    """显示个人信息"""
    user = request.user
    email = user.email
    list = user.profile.url_list
    if list:
        url_list = list.split(",")
    else:
        url_list = ['暂时没有项目URL...']
    return render(request, 'index.html', {"url_list": url_list})

def reg(request):
    return render(request, 'reg.html')
