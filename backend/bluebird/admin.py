from django.contrib import admin
from .models import (KLASS_TYPES, Contragent, NormativeCategory, Normative,
                     Contract, ContractNumberClass, DocumentsPackage, ActFile,
                     OtherFile)

from django.contrib.contenttypes.admin import GenericTabularInline


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


class ActInLine(GenericTabularInline):
    model = ActFile
    extra = 1
    ct_fk_field = 'object_id'
    ct_field = 'content_type'


class OtherFileInLine(GenericTabularInline):
    model = OtherFile
    extra = 1
    ct_fk_field = 'object_id'
    ct_field = 'content_type'


class DocumentsPackageAdmin(admin.ModelAdmin):
    inlines = [ActInLine, OtherFileInLine, ]


admin.site.register(Contragent, ContragentAdmin)
admin.site.register(NormativeCategory, NormativeCategoryAdmin)
admin.site.register(Normative, NormativeAdmin)
admin.site.register(Contract)
admin.site.register(ContractNumberClass)
admin.site.register(DocumentsPackage, DocumentsPackageAdmin)
