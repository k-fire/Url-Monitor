# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
import os

@login_required
def delurl(request):
    try:
        ctx ={}
        if request.POST:
            user = request.user
            user_profile = user.profile
            list = user_profile.url_list
            url_list = list.split(",") #转换为列表
            ctx['data'] = request.POST['url']
            if ctx['data'] in url_list:
                url_list.remove(ctx['data']) #删除数据，输出到index
                url = ",".join(url_list) #转换为字符串
                user_profile.url_list = url
                savefile=open('./account/user/%s'%(user.username),'wb+')
                savefile.write(url.encode('gbk','ignore'))
                savefile.close()
                user_profile.save()
                delinfo = '''<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <strong>删除 %s 成功!</strong> 返回主页即可显示。</div>'''%(ctx['data'])
            else:
                delinfo = '''<div class="alert alert-danger alert-dismissible">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <strong>删除 %s 失败!</strong> URL错误。
                '''%(ctx['data'])

        return render(request, 'index.html', {"url_list": url_list,"delinfo": delinfo})
    except:
        return render(request, 'error.html')
