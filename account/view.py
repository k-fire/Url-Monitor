# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required

@login_required
def view(request):
    ctx ={}
    if request.GET:
        ctx['data'] = request.GET['url']
        url = request.GET['url']
        user = request.user
        list = user.profile.url_list
        suburl_list = []
        survive_list = []
        change_list = []
        if url in list:
            file_name1 = ctx['data'].replace('https://','')
            file_name2 = file_name1.replace('http://','')
            file_name = file_name2.replace('/','')
            try:
                for line in open('./teemo/output/%s.txt'%(file_name),'rt'):
                    suburl = line.replace('\n','')
                    suburl_list.append(suburl)
            except:
                pass
            try:
                for line in open('./teemo/output/%s-survive.txt'%(file_name),'rt'):
                    surviveurl = line.replace('\n','')
                    survive_list.append(surviveurl)
            except:
                pass
            try:
                for line in open('./teemo/output/%s-change.txt'%(file_name),'rt'):
                    changeurl = line.replace('\n','')
                    change_list.append(changeurl)
            except:
                pass
            lenth = len(suburl_list)
            survive_list_lenth = len(survive_list)
            change_list_lenth = len(change_list)
            return render(request, 'view.html', {"url":url,"suburl_list":suburl_list,"lenth": lenth,"survive_list":survive_list,"survive_list_lenth":survive_list_lenth,"change_list":change_list,"change_list_lenth":change_list_lenth})

        else:
            return render(request, 'error.html')
    else:
        return render(request, 'error.html')
