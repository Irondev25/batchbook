from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm

from .models import Student


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control'}
                                ))
    password2 = forms.CharField(label='Password Conformation',
                                widget=forms.PasswordInput(attrs={
                                    'class':'form-control'
                                }))

    class Meta:
        model = Student
        fields = ('email', 'usn')
    
    def clean_password2(self):
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Password Doesn't match"
            )
        return password2
    
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
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
