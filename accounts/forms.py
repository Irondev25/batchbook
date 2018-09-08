import logging

from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    ReadOnlyPasswordHashWidget,
    AuthenticationForm, 
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm,
    PasswordChangeForm as BasePasswordChangeForm,
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm
)

from django.urls import reverse

from .models import Student
from .utils import ActivationMailFormMixin


logger = logging.getLogger(__name__)
YEAR = (1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 
        1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 
        1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 
        1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 
        1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 
        1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 
        1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974,
        1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 
        1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 
        1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 
        2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 
        2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 
        2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 
        2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050)
MONTHS = {
    1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr',
    5: 'may', 6: 'jun', 7: 'jul', 8: 'aug',
    9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
}


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
        fields = ('email', 'usn', 'first_name', 'middle_name', 'last_name', 'department',
                    'dob', 'year', 'profile_img', 'batch')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college E-mail'
            }),
            'usn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college USN'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Not compulsory'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Not compulsory'
            }),
            'dob': forms.SelectDateWidget(years=YEAR, months=MONTHS)
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

    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=
            "Raw passwords are not stored, so there is no way to see this "
            "password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ,
    )
    class Meta:
        model = get_user_model()
        fields = ('email', 'usn', 'password','first_name', 'middle_name', 'last_name',
                  'profile_img', 'dob', 'department', 'year', 'batch')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'usn': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'dob': forms.SelectDateWidget(years=YEAR, months=MONTHS),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = self.fields['password'].help_text.format(
            reverse('student:pw_change'))
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

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
