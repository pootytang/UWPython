from django.conf.urls.defaults import *

urlpatterns = patterns('polldaddy.views',
    (r'^$', 'index'),
    (r'^create/$', 'create_poll'),
    (r'^edit/$', 'edit_poll'),
    (r'^delete/$', 'delete_poll'),
)