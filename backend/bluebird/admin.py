from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import mark_safe
from .models import (KLASS_TYPES, Contragent, NormativeCategory, Normative,
                     Contract, ContractNumberClass, DocumentsPackage, ActFile,
                     OtherFile, CountFile, CountFactFile, SignUser)

from django.contrib.contenttypes.admin import GenericTabularInline


class ContragentAdmin(admin.ModelAdmin):
    sets = ('pk', 'excell_name', 'inn', 'display_contragent')
    list_display = sets
    list_display_links = sets
    readonly_fields = ['get_package', ]

    def display_contragent(self, obj):
        return (f'{KLASS_TYPES[int(obj.klass)][1]}')

    def get_package(self, obj):
        style_active = ['active', '']
        display_text = ", ".join([
            '<a style="' + style_active[child.is_active]
            + '" href={}>{}</a>'.format(
                    reverse('admin:{}_{}_change'.format(
                        child._meta.app_label,
                        child._meta.model_name),
                            args=(child.pk,)), f'Пакет {child.name_uuid}')
            for child in DocumentsPackage.objects.filter(contragent__id=obj.pk)
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"


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


class CountInLine(GenericTabularInline):
    model = CountFile
    extra = 1
    ct_fk_field = 'object_id'
    ct_field = 'content_type'


class CountFactInLine(GenericTabularInline):
    model = CountFactFile
    extra = 1
    ct_fk_field = 'object_id'
    ct_field = 'content_type'


class OtherFileInLine(GenericTabularInline):
    model = OtherFile
    extra = 1
    ct_fk_field = 'object_id'
    ct_field = 'content_type'


class DocumentsPackageAdmin(admin.ModelAdmin):
    sets = ('pk', 'name_uuid', 'contragent_name', 'is_active',
            'creation_date')
    list_display = sets
    list_display_links = sets
    inlines = [ActInLine, CountInLine, CountFactInLine, OtherFileInLine, ]

    def contragent_name(self, obj):
        return str(obj.contragent.excell_name)


class SignUserAdmin(admin.ModelAdmin):
    sets = ('pk', 'name', 'position', 'address')
    list_display = sets
    list_display_links = sets


admin.site.register(Contragent, ContragentAdmin)
admin.site.register(NormativeCategory, NormativeCategoryAdmin)
admin.site.register(Normative, NormativeAdmin)
admin.site.register(Contract)
admin.site.register(ContractNumberClass)
admin.site.register(DocumentsPackage, DocumentsPackageAdmin)
admin.site.register(SignUser, SignUserAdmin)
