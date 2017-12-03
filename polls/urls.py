from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^download/$', views.downl, name='downl'),
    url(r'^login/$', auth_views.login, {'template_name': 'polls/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'polls/logged_out.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
]
