from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy, re_path
from django.views.generic import RedirectView



from .views import Login, logout_view
from .forms import AuthenticationForm

app_name = 'student'


password_urls = [
    path('change/', auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url=reverse_lazy('student:pw_change_done')
    ), name='pw_change'),
    path('done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='pw_change_done'),
    path(
        'reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            email_template_name='accounts/password_reset_email.txt',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url=reverse_lazy('student:pw_reset_sent')
        ),
        name='pw_reset_start'
    ),
    path(
        'reset/sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_sent.html'
        ),
        name='pw_reset_sent'
    ),
    re_path(
        r'^reset/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('student:pw_reset_complete')
        ),
        name='pw_reset_confirm'
    ),
    re_path(
        r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html',
            extra_context={'form': AuthenticationForm}
        ),
        name='pw_reset_complete'
    ),
]



urlpatterns = [
    path(
        '', RedirectView.as_view(
            pattern_name='student:login',
            permanent=False
        )
    ),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password/', include(password_urls))
]
