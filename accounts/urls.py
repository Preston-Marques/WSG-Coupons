from django.conf.urls import include, url

from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    #ex: /accounts/login
    url(r'^login/$', auth_views.login, name='login'),
    #ex: /accounts/logout
    url(r'^logout/$', auth_views.logout, name='logout'),
    #ex: /accounts/password_change
    url(r'^password_change/$', auth_views.password_change, {'post_change_redirect':'accounts:password_change_done', }, name='password_change'),
    #ex: /accounts/password_change/done
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    #password reset for those wjo forgot their password
    #ex: /accounts/password_reset
    url(r'^password_reset/$', auth_views.password_reset, {'post_reset_redirect':'accounts:password_reset_done', }, name='password_reset'),
    #ex: /accounts/password_reset/done/
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #page to reset your password,sent by email
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'post_reset_redirect':'accounts:password_reset_complete', }, name='password_reset_confirm'),
    #ex: /accounts/reset/done/
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #ex: /accpunts/register
    url(r'^register/$', views.register, name='register'),
]
