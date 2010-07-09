from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dj_test/', include('dj_test.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^makler/json', 'dj_test.makler.views.json'),
    (r'^makler/test/$', 'dj_test.makler.views.test'),
    (r'^makler/$', 'dj_test.makler.views.index'),
    (r'^makler/(?P<adv_id>\d+)/$', 'dj_test.makler.views.detail'),
    (r'^makler/addAdv/$', 'dj_test.makler.views.addAdv'),
    (r'^admin/', include(admin.site.urls)),
)
