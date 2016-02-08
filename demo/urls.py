
from django.conf.urls import url
from . import views as ui_views
from . import api_views

app_name = 'demo'
urlpatterns = [
    # /auth/login/           (GET, POST)
    url(r'^auth/login/$', ui_views.login, name='login'),
    # /auth/logout/          (GET)
    url(r'^auth/logout/$', ui_views.logout, name='logout'),
    # /auth/tokens/ 
    url(r'^auth/tokens/$', api_views.tokens, name='tokens'),
    # /ui/objects/           (GET, POST)
    url(r'^ui/objects/$', ui_views.object_container, name='container'),
    # /ui/objects/myobject/  (GET, PUT, DELETE)
    url(r'^ui/objects/(?P<object_name>[a-zA-Z0-9\-\;]+)/$', ui_views.object_view, name='object'),
    # /api/objects/          (GET, POST)
    url(r'^api/objects/$', api_views.object_container, name='api-container'),
    # /api/objects/myobject/ (GET, PUT, DELETE)
    url(r'^api/objects/(?P<object_name>[a-zA-Z0-9\-\.]+)/$', api_views.object_view, name='api-object'),
]

