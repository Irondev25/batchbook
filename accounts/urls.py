from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    password_change, password_change_done, PasswordChangeView, PasswordChangeDoneView
) 


from .views import Login, logout_view

app_name = 'student'


password_urls = [
    path('change/', PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url=reverse_lazy('student:pw_change_done')
    ), name='pw_change'),
    path('done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='pw_change_done')
]



urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password/', include(password_urls))
]
