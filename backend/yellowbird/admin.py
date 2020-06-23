from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department


class JudUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('info', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('info', 'department')}),)
    # fields = 
    # readonly_fields = ('password',)


class DepartmentAdmin(admin.ModelAdmin):
    sets = ('title', )
    list_display = sets
    list_display_links = sets


admin.site.register(User, JudUserAdmin)
admin.site.register(Department, DepartmentAdmin)
