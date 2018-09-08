from django.urls import path, re_path

from .views import BatchDetailView, BatchList

app_name = 'batch'

urlpatterns = [
    re_path(r'^list', BatchList.as_view(), name='batch_list'),
    re_path(r'^(?P<department>[a-zA-z]{2,3})/'
            r'(?P<year>[0-9]{4})/'
            r'(?P<section>[a-zA-Z]{1})/detail/$', 
            BatchDetailView.as_view(), name='batch_detail')
]