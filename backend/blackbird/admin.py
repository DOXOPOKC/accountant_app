from django.contrib import admin
from blackbird.models import Formula


class FormulaAdmin(admin.ModelAdmin):
    sets = ('id', '__str__', 'is_rough')
    list_display = sets
    list_display_links = sets

    def is_rough(self, obj):
        return f'{obj.is_rough}'


admin.site.register(Formula, FormulaAdmin)
