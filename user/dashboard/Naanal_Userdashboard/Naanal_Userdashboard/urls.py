from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Naanal_Userdashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/','login.views.loginpage' ),
    url(r'^index/','login.views.index_page' ),
    url(r'^change/','login.views.change_password' ),
    url(r'^help/','login.views.help' ),
    url(r'^stop/','login.views.instance_stop' ),
)
