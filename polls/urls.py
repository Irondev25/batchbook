from django.urls import path, re_path

from . import views

app_name = 'poll'


urlpatterns = [
    path('', views.PollList.as_view(), name='poll_list'),
    path('create/', views.PollCreate.as_view(), name='poll_create'),
    path('<int:pk>/', views.PollDetail.as_view(), name='poll_detail'),
    path('<int:pk>/update/', views.edit_poll, name='poll_update'),
    path('<int:pk>/delete/', views.PollDelete.as_view(), name='poll_delete'),
    path('<int:pk>/result/', views.PollResult.as_view(), name='poll_result'),
    path('<int:poll_pk>/add/choice/', views.ChoiceCreate.as_view(), name='choice_create'),
]