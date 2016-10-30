from django.conf.urls import url
from . import views

app_name = "ACMS"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.index, name='login_index'),
    url(r'^password-changed/$', views.index, name='password'),
    url(r'^acms/homepage/$', views.homepage, name='homepage'),
    url(r'^acms/workpage/$', views.workpage, name='workpage'),
    url(r'^acms/workpage/patient/$', views.patient, name = 'patient'),
    url(r'^acms/workpage/drug/$', views.drug, name = 'drug'),
    url(r'^acms/workpage/hmo/$', views.hmo, name = 'hmo'),
    url(r'^acms/change_password/$', views.changePassword, name = 'change_password'),



]
