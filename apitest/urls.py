from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'main.views.index'),
    (r'^pd/', include('polldaddy.urls'))
)
