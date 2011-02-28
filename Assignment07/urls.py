from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^[E|e]vents*/', include('EventsCalendar.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/profile/$', 'EventsCalendar.views.index'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^accounts/register/$', 'EventsCalendar.views.register'),
)

from django.conf import settings
## debug stuff to serve static media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^event_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_FILES_ROOT}),
   )
