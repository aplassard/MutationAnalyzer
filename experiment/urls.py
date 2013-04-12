from django.conf.urls import patterns, url
from experiment import views

urlpatterns = patterns('',
        url(r'^new/$', views.new, name='new'),
        url(r'^$',views.index,name='index'),
)
