from django.contrib.auth import views
from django.conf.urls import url
from django.urls import path
from . import addurl,delurl,view,reg

urlpatterns = [
path('login/',views.LoginView.as_view(),name='login'),
url(r'^addurl$', addurl.addurl,name='addurl'),
url(r'^delurl$', delurl.delurl,name='delurl'),
url(r'^view$', view.view,name='view'),
url(r'^reg', reg.reg,name='reg'),
]
