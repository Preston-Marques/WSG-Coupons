from django.conf.urls import url

from . import views

app_name = 'coupons'
urlpatterns = [
    # ex: /coupons/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /coupons/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /coupons/5/claim/
    url(r'^(?P<coupon_id>[0-9]+)/claim/$', views.claim, name='claim'),
    # ex: /coupons/5/result/
    url(r'^(?P<pk>[0-9]+)/result/$', views.ResultView.as_view(), name='result'),
    #ex: /coupons/create
    url(r'^create/$', views.createcoupon, name='createcoupon'),
]
