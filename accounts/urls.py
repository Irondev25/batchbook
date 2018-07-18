from django.urls import path


from .views import Login, logout_view

app_name = 'student'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]