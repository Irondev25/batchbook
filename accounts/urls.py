from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    password_change, password_change_done
) 


from .views import Login, logout_view

app_name = 'student'


password_urls = [
    path(
        'change/', password_change,
        {
            'template_name': 'accounts/password_change_form.html',
            'post_change_redirect': reverse_lazy('student:pw_change_done')
        },
        name='pw_change'
    ),
    path(
        'change/done/', password_change_done, 
        {
            'template_name': 'accounts/password_change_done.html'
        },
        name='pw_change_done'
    ),
]



urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password/', include(password_urls))
]
