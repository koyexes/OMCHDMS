from django.conf.urls import url
from . import views

app_name = "ACMS"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.index, name='login_index'),
    url(r'^password-changed/$', views.index, name='password'),
    url(r'^acms/homepage/$', views.homepage, name='homepage'),
    url(r'^acms/find-patient/$', views.find_patient, name='find_patient'),
    url(r'^acms/find-drug/$', views.find_drug, name='find_drug'),
    url(r'^acms/find-hmo/$', views.find_hmo, name='find_hmo'),
    url(r'^acms/workpage/$', views.workpage, name='workpage'),
    url(r'^acms/workpage/patient/$', views.patient_form_view, name = 'patient'),
    url(r'^acms/workpage/drug/$', views.drug_form_view, name = 'drug'),
    url(r'^acms/workpage/hmo/$', views.hmo_form_view, name = 'hmo'),
    url(r'^acms/change_password/$', views.changePassword, name = 'change_password'),



]
