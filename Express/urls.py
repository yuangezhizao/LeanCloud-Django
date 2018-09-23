from django.conf.urls import url

from . import views

app_name = 'Express'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^index/', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^confirm/$', views.user_confirm),
    url(r'^realname/$', views.realname, name='realname'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^edit/$', views.edit, name='edit'),

    url(r'^ground/$', views.ground, name='ground'),

    url(r'^detail/(?P<express_id>\d+)/$', views.detail, name='detail'),

    url(r'^detail/(?P<express_id>\d+)/receive$', views.detail_receive, name='detail_receive'),

    url(r'^detail/(?P<express_id>\d+)/finish', views.detail_finish, name='detail_finish'),
    url(r'^detail/(?P<express_id>\d+)/rate-receive', views.detail_rate_receive, name='rate-receive'),
    url(r'^detail/(?P<express_id>\d+)/rate-publish', views.detail_rate_publish, name='rate-publish'),

    url(r'^my/$', views.my, name='my'),
    url(r'^my_receive/$', views.my_receive, name='my_receive'),
    url(r'^my_send/$', views.my_publish, name='my_publish'),

    url(r'^user/(?P<user_id>\d+)/$', views.user, name='user'),
]
