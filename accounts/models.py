import random
import os

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from django.core.validators import RegexValidator


from batch.models import BatchModel
from .validators import email_validator
# Create your models here.

USN_REGEX = r'^1BM\d{2}[A-Z]{2,3}\d{3}$'





class StudentManager(BaseUserManager):
    def normalize_usn(self, value):
        return value.upper()

    def create_user(self, email, usn, password=None):
        """
        Creates and saves a User with the given email, usn and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not usn:
            raise ValueError('User must have USN.')
        
        user = self.model(
            email=self.normalize_email(email),
            usn=self.normalize_usn(usn),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, usn, password):
        """
        Creates and saves a superuser with the given email, usn and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not usn:
            raise ValueError('User must have USN.')

        user = self.create_user(
            email,
            usn,
            password=password
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user





def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,999999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile_pics/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Student(AbstractBaseUser, PermissionsMixin):
    INFORMATION_SCIENCE = 'ISE'
    COMPUTER_SCIENCE = 'CSE'
    DEPARTMENT = (
        (INFORMATION_SCIENCE, 'Information Science Engg.'),
        (COMPUTER_SCIENCE, 'Computer Science Engg.'),
    )
    YEAR_CHOICES = [(2015, 2015),(2016,2016),(2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)]

    email = models.EmailField(
        "College Email",
        validators = [email_validator,],
        unique=True
    )
    usn = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(
            regex=USN_REGEX,
            message='Please enter valid USN.(must be in capital letter)',  
            code='usn_err'
        ),]
    )
    first_name = models.CharField(max_length=30, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, null=True)
    dob = models.DateField("date of birth", null=True)
    department = models.CharField(
        max_length=3,
        choices = DEPARTMENT,
        null = True
    )
    profile_img = models.ImageField(
        upload_to=upload_image_path,
        default='profile_pics/default/default.jpg',
    )
    year = models.IntegerField(
        'Year',
        choices=YEAR_CHOICES,
        help_text="Year which you joined the college.",
        null= True
    )
    batch = models.ForeignKey(BatchModel, related_name='students', on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField('class representative',default=False)
    is_superuser = models.BooleanField('administrator',default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usn']

    class Meta:
        verbose_name='student'
        verbose_name_plural='students'

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name
    
    def get_full_name(self):
        if self.middle_name != None and self.last_name != None:
            return "{fn} {mn} {ln}".format(
                fn = self.first_name,
                mn = self.middle_name,
                ln = self.last_name
            )
        elif self.last_name != None:
            return "{fn} {ln}".format(
                fn=self.first_name,
                ln=self.last_name
            )
        else:
            return self.get_short_name()
    
    def get_email(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_absolute_url(self):
        return reverse('student:profile')
    
    def get_profile_edit_url(self):
        return reverse('student:profile_edit')
