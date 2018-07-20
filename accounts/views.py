from django.shortcuts import render, redirect

from django.conf import settings

from django.core.validators import ValidationError

from django.contrib.auth import (
    authenticate, login, logout,
    get_user
)

from django.contrib.messages import error, success

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, get_user_model, logout
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.decorators import 


from django.template.response import TemplateResponse

from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from django.urls import reverse_lazy

from django.views.generic import View
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


from .forms import LoginForm, UserCreationForm, ResendActivationEmailForm
from .utils import MailContextViewMixin

# Create your views here.

# @sensitive_post_parameters('password')
# def login_view(request):
#     form = LoginForm(request.POST or None)
#     context = {'form':form}
#     next = request.GET.get('next')
#     print(next)
#     if form.is_valid():
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return (redirect(next) or "/")
#         else:
#             context['non_field_errors'] = "login creadentials didn't match."
#     return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    next = request.GET.get('next')
    return redirect(next)

class Login(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm


class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'accounts/user_confirm_delete.html'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name
        )
    
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request):
        user = get_user(request)
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout(request)
        return redirect(self.success_url)


class CreateAccount(MailContextViewMixin, View):
    form_class = UserCreationForm
    success_url = reverse_lazy(
        'student:create_done')
    template_name = 'accounts/user_create.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters(
        'password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            # not catching returned user
            bound_form.save(
                **self.get_save_kwargs(request))
            if bound_form.mail_sent:  # mail sent?
                return redirect(self.success_url)
            else:
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                return redirect('student:resend_activation')
        return TemplateResponse(
            request,
            self.template_name,
            {'form': bound_form})

class ActivateAccount(View):
    success_url = reverse_lazy('student:login')
    template_name = 'accounts/user_activate.html'

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(
                urlsafe_base64_decode(uidb64)
            )
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError,
               OverflowError, User.DoesNotExist):
               user = None
        if(user is not None and token_generator.check_token(user, token)):
            user.is_active = True
            user.save()
            success(
                request,
                'User Activated '
                'You may now login.'
            )
            return redirect(self.success_url)
        else:
            return TemplateResponse(
                request,
                self.template_name
            )
        
class ResendActivationEmail(MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('student:login')
    template_name = 'accounts/resend_activation.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {
                'form': self.form_class()
            }
        )
    
    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(
                **self.get_save_kwargs(request)
            )
            if(user is not None and not bound_form.mail_sent):
                errs = (
                    bound_form.non_field_errors()
                )
                for err in errs:
                    error(request, err)
                if errs:
                    bound_form.errors.pop('__all__')
                return TemplateResponse(
                    request, self.template_name,
                    {'form':bound_form}
                )
        success(
            request,
            'Activation Email sent!'
        )
        return redirect(self.success_url)


