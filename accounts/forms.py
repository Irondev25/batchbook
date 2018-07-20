import logging

from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    AuthenticationForm, 
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm,
    PasswordChangeForm as BasePasswordChangeForm,
    UserCreationForm as BaseUserCreationForm
)

from .models import Student
from .utils import ActivationMailFormMixin


logger = logging.getLogger(__name__)


class UserCreationForm(ActivationMailFormMixin ,BaseUserCreationForm):
    mail_validation_error = ('User created. Could not send activation '
                             'email. Please try again later. (Sorry!)')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control'}
                                ))
    password2 = forms.CharField(label='Password Conformation',
                                widget=forms.PasswordInput(attrs={
                                    'class':'form-control'
                                }))

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'usn')
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college email'
            }),
            'usn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your USN'
            })
        }
    
    def clean_usn(self):
        usn = self.cleaned_data['usn']
        if usn is not None:
            return usn.upper()

    def clean_email(self):
        email = self.cleaned_data['email']
        email_domain = email.split('@')[1]
        if email_domain != 'bmsce.ac.in':
            raise forms.ValidationError(
                "Email domain must be 'bmsce.ac.in'"
            )
        return email
    
    def save(self, **kwargs):
        user = super().save(commit=False)
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        user.save()
        self.save_m2m()
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Student
        fields = ('email', 'usn', 'first_name', 'middle_name', 'last_name', 
                  'dob', 'batch', 'profile_img', 'year')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'required': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': True
    }))

    class Meta:
        widgets = {
            'username': {
                'class': 'form-control'
            },
            'password': {
                'class': 'form-control'
            }
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email_domain = email.split('@')[1]
        if email_domain != 'bmsce.ac.in':
            raise forms.ValidationError(
                "Email domain must be 'bmsce.ac.in'"
            )
        return email


    
class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(label="Email", max_length=256,
                            widget=forms.EmailInput(attrs={
                                'class':'form-control'
                            }))


class SetPasswordForm(BaseSetPasswordForm):
    error_messages = {
        'password_mismatch':"The two password fields didn't match.",
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
    )


class PasswordChangeForm(SetPasswordForm, BasePasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,
            'class':'form-control'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']


class ResendActivationEmailForm(ActivationMailFormMixin, forms.Form):
    email = forms.EmailField()

    mail_validation_error = (
        'Could not re-send activation email. '
        'Please try again later. (Sorry!)'
    )

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(
                email=self.cleaned_data['email']
            )
        except:
            logger.warning(
                'Resend Activation: No user with '
                'email: {}.'.format(
                    self.cleaned_data['email']
                )
            )
            return None    
        self.send_mail(user=user, **kwargs)
        return user
