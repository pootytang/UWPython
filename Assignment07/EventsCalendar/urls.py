from django.conf.urls.defaults import *

urlpatterns = patterns('EventsCalendar.views',
    (r'^$', 'index'),
    (r'^month/$', 'month'),
    (r'^year/$', 'year'),
    (r'^details/(?P<id>\d)/$', 'details'),
    (r'^search_results/$', 'search_results'),
    (r'^add/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)$', 'add_event'),
    (r'^add_location/$', 'add_location'),
)