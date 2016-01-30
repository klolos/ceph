
from django.conf.urls import url
from . import views

app_name = 'demo'
urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),
    # /accounts/login
    url(r'^accounts/login/$', views.login, name='login'),
    # /accounts/logout
    url(r'^accounts/logout/$', views.logout, name='logout'),
    # /accounts/request_login
    url(r'^accounts/request_login/$', views.request_login, 
                                      name='request_login'),
    # /object/myobject
    url(r'^object/(?P<object_name>[a-zA-Z0-9\-]+)/$', 
        views.details, name='details'),
    # /object/myobject/edit
    url(r'^object/(?P<object_name>[a-zA-Z0-9\-]+)/edit/$', 
        views.edit, name='edit'),
    # /object/myobject/update
    url(r'^object/(?P<object_name>[a-zA-Z0-9\-]+)/update/$', 
        views.update, name='update'),
    # /object/myobject/delete
    url(r'^object/(?P<object_name>[a-zA-Z0-9\-]+)/delete/$', 
        views.delete, name='delete'),
    # /create
    url(r'^create/$', views.create, name='create'),
    # /store
    url(r'^store/$', views.store, name='store'),
]
