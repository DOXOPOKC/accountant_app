from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import mark_safe
from .models import (KLASS_TYPES, Contragent, NormativeCategory, Normative,
                     Contract, ContractNumberClass, DocumentsPackage,
                     OtherFile, PackFile, SignUser, CityModel,
                     TemplateModel, DocumentTypeModel,
                     #  SingleFilesTemplate, PackFilesTemplate,
                     SingleFile, DocumentFileTemplate,
                     State, Event, Commentary,
                     DocumentStateEntity)

from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import (TemplateModelForm,
                    # PackFilesTemplateAdminForm,
                    # SingleFilesTemplateAdminForm, 
                    DocumentFileTemplateAdminForm,
                    DocumentStateEntityForm)

from itertools import zip_longest


class DuplicateElementsMixin:
    """"""

    def duplicate(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.save()
        return

    duplicate.short_description = 'Копировать выбранные елементы'


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


class NormativeCategoryAdmin(admin.ModelAdmin, DuplicateElementsMixin):
    filter_horizontal = ('normative',)
    list_display = ('__str__',)

    actions = ['duplicate', ]


class NormativeAdmin(admin.ModelAdmin, DuplicateElementsMixin):
    list_display = ('__str__',)

    actions = ['duplicate', ]


class SingleFileInLine(GenericTabularInline):
    model = SingleFile
    extra = 1
    ct_fk_field = 'object_id'
    ct_field = 'content_type'


class PackFileInLine(GenericTabularInline):
    model = PackFile
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
            'creation_date', 'package_state')
    list_display = sets
    list_display_links = sets
    inlines = [SingleFileInLine, PackFileInLine, OtherFileInLine, ]

    def contragent_name(self, obj):
        return str(obj.contragent.excell_name)

    actions = ["mark_not_active", "mark_active"]

    def mark_not_active(self, request, queryset):
        queryset.update(is_active=False)
    mark_not_active.short_description = "Пометить выбранные пакеты документов\
        как неактивные"

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Пометить выбранные пакеты документов как\
        активные"


class DocumentStateEntityInline(admin.StackedInline):
    form = DocumentStateEntityForm
    model = DocumentStateEntity
    filter_horizontal = ('documents',)
    extra = 1
    ct_fk_field = 'entity_id'
    ct_field = 'content_type'


# class SingleFilesTemplateAdmin(admin.ModelAdmin):
#     form = SingleFilesTemplateAdminForm
#     inlines = [DocumentStateEntityInline]
#     # filter_horizontal = ('documents',)
#     list_display_links = ('__str__', )
#     list_display = ('__str__', )

class DocumentFileTemplateAdmin(admin.ModelAdmin):
    form = DocumentFileTemplateAdminForm
    inlines = [DocumentStateEntityInline]
    # filter_horizontal = ('documents',)
    list_display_links = ('__str__', )
    list_display = ('__str__', )


# class PackFilesTemplateAdmin(admin.ModelAdmin):
#     form = PackFilesTemplateAdminForm
#     filter_horizontal = ('documents',)
#     list_display = ('__str__', )


class SignUserAdmin(admin.ModelAdmin, DuplicateElementsMixin):
    sets = ('pk', 'name', 'position', 'address', "is_sign")
    list_display = sets
    list_display_links = sets

    actions = ['duplicate', ]

    def is_sign(self, obj):
        return bool(obj.sign)

    is_sign.boolean = True


class CityModelAdmin(admin.ModelAdmin, DuplicateElementsMixin):
    sets = ('pk', 'name')
    list_display = sets
    list_display_links = sets

    actions = ['duplicate', ]


class DocumentTypeModelAdmin(admin.ModelAdmin, DuplicateElementsMixin):
    sets = ('pk', 'doc_type')
    list_display = sets
    list_display_links = sets

    actions = ['duplicate', ]


class TemplateModelAdmin(admin.ModelAdmin, DuplicateElementsMixin):
    form = TemplateModelForm
    sets = ('pk', 'document_type', 'contragent_type', 'city')
    list_display = sets
    list_display_links = sets

    actions = ['duplicate', ]


class StateAdmin(admin.ModelAdmin):
    sets = ('name_state', )
    list_display = sets
    list_display_links = sets
    filter_horizontal = ('departments',)
    readonly_fields = ['get_events', ]

    def get_events(self, obj):
        out_events = Event.objects.filter(from_state__id=obj.pk)
        in_events = Event.objects.filter(to_state__id=obj.pk)
        print(len(out_events), len(in_events))
        tmp_str = ''.join(
            [f'<tr><td>{t[0]}</td><td>{t[1]}</td></tr>' for t in list(
                zip_longest(out_events, in_events, fillvalue='-'))])
        display_text = f'<table><thead><th>Исходящие события</th><th>Входящие\
             события</th></thead><tbody>{tmp_str}</tbody></table>'
        if display_text:
            return mark_safe(display_text)
        return "-"


class EventAdmin(admin.ModelAdmin):
    sets = ('name_event', 'from_state', 'to_state')
    list_display = sets
    list_link_display = sets


admin.site.register(Contragent, ContragentAdmin)
admin.site.register(NormativeCategory, NormativeCategoryAdmin)
admin.site.register(Normative, NormativeAdmin)
admin.site.register(Contract)
admin.site.register(ContractNumberClass)
admin.site.register(DocumentsPackage, DocumentsPackageAdmin)
admin.site.register(SignUser, SignUserAdmin)
admin.site.register(CityModel, CityModelAdmin)
admin.site.register(DocumentTypeModel, DocumentTypeModelAdmin)
admin.site.register(TemplateModel, TemplateModelAdmin)
# admin.site.register(SingleFilesTemplate, SingleFilesTemplateAdmin)
# admin.site.register(PackFilesTemplate, PackFilesTemplateAdmin)
admin.site.register(DocumentFileTemplate, DocumentFileTemplateAdmin)
admin.site.register(PackFile)
admin.site.register(State, StateAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Commentary)
