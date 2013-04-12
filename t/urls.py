from django.conf.urls import patterns, url
from t import views

urlpatterns = patterns('',
        url(r'^submit/$', views.submit,name='submit'),
        url(r'^$',views.index,name='index'),
)
