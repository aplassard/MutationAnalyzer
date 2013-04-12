from django.conf.urls import patterns, url
from experiment import views

urlpatterns = patterns('',
        url(r'^new/$', views.new, name='new'),
        url(r'^$',views.index,name='index'),
        url(r'^(?P<experiment_id>\d+)/create/$',views.create,name='create'),
)
