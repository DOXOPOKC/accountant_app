from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department


class JudUserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'name', 'last_name', 'info',
              'department', 'is_superuser', 'is_staff')
    readonly_fields = ('password',)


class DepartmentAdmin(admin.ModelAdmin):
    sets = ('title', )
    list_display = sets
    list_display_links = sets


admin.site.register(User, JudUserAdmin)
admin.site.register(Department, DepartmentAdmin)
