# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
import os
# 接收POST请求数据
@login_required
def addurl(request):
    try:
        ctx ={}
        if request.POST:
            user = request.user
            user_profile = user.profile
            list = user_profile.url_list
            if list:
                url_list = list.split(",")
            else:
                url_list = []
            ctx['data'] = request.POST['url']
            if ctx['data'] not in url_list:
                if 'http://' in ctx['data']:
                    url_list.append(ctx['data'])
                    url = ",".join(url_list)
                    user_profile.url_list = url
                    savefile=open('./account/user/%s'%(user.username),'wb+')
                    savefile.write(url.encode('gbk','ignore'))
                    savefile.close()
                    user_profile.save()
                    addinfo = '''<div class="alert alert-success alert-dismissible">
                    <button type="button" class="close" data-dismiss="alert">&times;</button><strong>添加 %s 成功!</strong></div>'''%(ctx['data'])
                elif 'https://' in ctx['data']:
                    url_list.append(ctx['data'])
                    url = ",".join(url_list)
                    user_profile.url_list = url
                    savefile=open('./account/user/%s'%(user.username),'wb+')
                    savefile.write(url.encode('gbk','ignore'))
                    savefile.close()
                    user_profile.save()
                    addinfo = '''<div class="alert alert-success alert-dismissible">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    <strong>添加 %s 成功!</strong></div>'''%(ctx['data'])
                else:
                    addinfo = '''<div class="alert alert-danger alert-dismissible fade show">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                    <strong>添加 %s 失败!</strong> 请输入正确格式的URL。</div>'''%(ctx['data'])
            else:
                addinfo = '''<div class="alert alert-danger alert-dismissible fade show">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <strong>添加 %s 失败!</strong> 该URL已存在队列中。</div>'''%(ctx['data'])

        return render(request, 'index.html', {"url_list": url_list,"addinfo": addinfo})
    except:
        return render(request, 'error.html')
