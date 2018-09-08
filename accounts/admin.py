from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Student
from .forms import UserChangeForm as BaseUserChangeForm, UserCreationForm

# Register your models here.


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        fields = '__all__'


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    actions = ['make_staff']
    list_display = ('full_name', 'email', 'is_staff', 'is_superuser')
    list_display_links = ('full_name', 'email')
    list_filter = ('department', 'year')
    fieldsets = (
        (
            None, {
                'fields': ('email', 'usn', 'password', 'department', 'year', 'batch')
            }
        ),
        ('Personal Info', {
            'fields': ('profile_img', 'first_name', 'middle_name', 'last_name', 'dob')
        }
        ),
        (
            'Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
            }
        ),
    )
    search_fields = ('email', 'usn', ' first_name', 'last_name')
    ordering = ('first_name', 'last_name')
    filter_horizontal = ('user_permissions', 'groups')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'usn', 'password1', 'password2')}
         ),
    )

    def full_name(self, user):
        return user.get_full_name()
    
    def make_staff(self, request, queryset):
        rows_updated = queryset.update(
            is_staff=True
        )
        if rows_updated == 1:
            message = '1 user was'
        else:
            message = '{} users were'.format(rows_updated)

        message += ' successfully made staff.'
        self.message_user(request, message)
    make_staff.short_description = (
        'Allow user to access Admin site.'
    )
