from django.contrib import admin
from blackbird.models import Formula, Tariff


class FormulaAdmin(admin.ModelAdmin):
    sets = ('id', '__str__', 'is_rough')
    list_display = sets
    list_display_links = sets

    def is_rough(self, obj):
        return f'{obj.is_rough}'


class TariffAdmin(admin.ModelAdmin):
    sets = ('id', '__str__')
    list_display = sets
    list_display_links = sets


admin.site.register(Formula, FormulaAdmin)
admin.site.register(Tariff, TariffAdmin)
