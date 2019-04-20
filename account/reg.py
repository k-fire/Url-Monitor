# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from django.contrib.auth.models import User
from .models import UserProfile
import re

def reg(request):
    if request.POST:
        user_name = request.POST['user_name']
        user_mail = request.POST['user_mail']
        user_password = request.POST['user_password']
        second_password = request.POST['second_password']
        invite_code = request.POST['invite_code']
        pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

        if not check_invite_code(invite_code):
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>邀请码不存在!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif len(user_name) < 4:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>用户名太短，应不小于4个字符!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif len(user_name) > 149:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>用户名太长，应不大于149个字符!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif len(User.objects.filter(username=user_name)) > 0:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>用户名已存在，换一个试试吧!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif not re.match(pattern, user_mail):
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>请输入有效的邮箱!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif user_password in user_name:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>密码不得与用户名相似!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif len(user_password) < 6:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>密码不得少于6个字符!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        elif len(user_password) > 15:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>密码不得大于15个字符!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})

        elif not user_password == second_password:
            return_info = '''<div class="alert alert-danger alert-dismissible fade show">
            <strong>两次密码输入不一样!</strong>
            </div>'''
            return render(request, 'reg.html',{'return_info':return_info})
        else:
            global invite_code_list
            user = User.objects.create_user(username=user_name, password=user_password)
            user_profile = UserProfile(user=user)
            user_profile.save()
            del_invite_code=open('./invite_code.txt','wb+')
            invite_code_list.remove(invite_code)
            data = "\n".join(invite_code_list)
            del_invite_code.write(data.encode('gbk','ignore'))
            del_invite_code.close()
            mail_add = open('./mail/%s.mail'%(user_name),'wb+')
            mail_add.write(user_mail.encode('gbk','ignore'))
            mail_add.close()
            return render(request, 'reg_done.html')
    else:
        return render(request, 'reg.html')


def check_invite_code(invite_code):
    global invite_code_list
    invite_code_list = []
    for line in open('./invite_code.txt','rt'):
        code = line.replace('\n','')
        invite_code_list.append(code)
    if invite_code not in invite_code_list:
        return False
    else:
        return True
