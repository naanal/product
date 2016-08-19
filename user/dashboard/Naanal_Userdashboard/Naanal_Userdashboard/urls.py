from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^','login.views.loginpage' ),
    url(r'^index/','login.views.index_page' ),
    url(r'^change/','login.views.change_password' ),
    url(r'^help/','login.views.help' ),
    url(r'^login_help/','login.views.login_help' ),
    url(r'^browservm_help/','login.views.browservm_help' ),
    url(r'^RDP_help/','login.views.RDP_help' ),
    url(r'^changepswd_help/','login.views.changepswd_help' ),
    url(r'^stop/','login.views.instance_stop' ),
    url(r'^logout/','login.views.logout' ),
    url(r'^snap/','login.views.snapshot' ),
    url(r'^restore/','login.views.restore_from_snapshot' ),    
)
