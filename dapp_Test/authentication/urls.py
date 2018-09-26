from django.conf.urls import url

from . import views

app_name = 'auth'

urlpatterns = [
    url(r'^$', views.index, name='authentication'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^createAccount/$', views.createAccount, name='createAccount'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.updateUser, name='update'),
    ]
