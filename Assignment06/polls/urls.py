from django.conf.urls.defaults import *

urlpatterns = patterns('polls.views',
    (r'^$', 'index'),
    (r'^get_polls/$', 'get_polls'),
    (r'^api/$', 'api'),
    (r'^(?P<poll_id>\d+)/$', 'detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)

