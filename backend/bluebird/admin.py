from django.contrib import admin
from .models import (KLASS_TYPES, Contragent, NormativeCategory, Normative,
                     Contract, ContractNumberClass, CountUNGen, ActUNGen,
                     ActUN, CountUN)


class ContragentAdmin(admin.ModelAdmin):
    sets = ('pk', 'excell_name', 'inn', 'display_contragent')
    list_display = sets
    list_display_links = sets

    def display_contragent(self, obj):
        return (f'{KLASS_TYPES[int(obj.klass)][1]}')


class NormativeCategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('normative',)
    list_display = ('__str__',)


class NormativeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(Contragent, ContragentAdmin)
admin.site.register(NormativeCategory, NormativeCategoryAdmin)
admin.site.register(Normative, NormativeAdmin)
admin.site.register(Contract)
admin.site.register(ContractNumberClass)
admin.site.register(ActUN)
admin.site.register(ActUNGen)
admin.site.register(CountUN)
admin.site.register(CountUNGen)
