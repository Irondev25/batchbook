from django.shortcuts import render, redirect

from django.core.validators import ValidationError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView

from django.views.decorators.debug import sensitive_post_parameters


from .forms import LoginForm

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
