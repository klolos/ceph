
from django.conf.urls import url
from . import views

app_name = 'demo'
urlpatterns = [
    # /auth/login/       (GET, POST)
    url(r'^auth/login/$', views.login, name='login'),
    # /auth/logout/      (GET)
    url(r'^auth/logout/$', views.logout, name='logout'),
    # /objects/          (GET, POST)
    url(r'^objects/$', views.object_container, name='container'),
    # /objects/myobject/ (GET, PUT, DELETE)
    url(r'^objects/(?P<object_name>[a-zA-Z0-9\-]+)/$', views.object_view, name='object'),
]
