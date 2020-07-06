from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _
from django import forms
from django_ace import AceWidget
import os,hashlib,datetime

from django.conf import settings

class FileControlAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if "instance" in kwargs \
                and kwargs["instance"] is not None \
                and kwargs["instance"].type_file not in ['bin', 'archive']:
            type_file = kwargs["instance"].type_file

            self.base_fields['text_content'].widget = AceWidget(mode=type_file, width="100%", toolbar=True)

        super(FileControlAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        #if cleaned_data["type_file"] not in ["bin", "archive"]:
        #    del cleaned_data["file"]

        return cleaned_data
    class Meta:
        model = FileControl
        fields = '__all__'


def md5(path_to_file):
    md5_hash = hashlib.md5()

    with open(path_to_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


@admin.register(FileControl)
class FileControlAdmin(admin.ModelAdmin):

    list_display = ["title", "type_file",  "enable", "created", "changed", "download_order", "download_auto", "path_to", "file"]
    search_fields = ["title", "ident", "comment_dev", "path_to", "text_content"]
    readonly_fields = ("created", "changed", "version")
    list_filter = ["type_file",  "enable", "download_auto"]

    form = FileControlAdminForm

    def save_model(self, request, obj, form, change):
        obj.changed = datetime.datetime.now()

        super().save_model(request, obj, form, change)

        obj = FileControl.objects.filter(id=obj.id)[0]

        md5_hash = None
        if obj.download_auto is not None:
            timestamp = str(datetime.datetime.now().timestamp())
            md5_hash = hashlib.md5(timestamp.encode()).hexdigest()

        if md5_hash is None and obj.type_file in ['bin', 'archive'] and str(obj.file) != '':
            path_sub = str(obj.file)
            path_full = os.path.join(settings.BASE_DIR, path_sub)
            md5_hash = md5(path_full)
        elif md5_hash is None and obj.type_file not in ['bin', 'archive']:
            md5_hash = hashlib.md5(obj.text_content.encode()).hexdigest()

        if md5_hash:
           FileControl.objects.filter(id=obj.id).update(version=md5_hash)

    #
    def get_fieldsets(self, request, obj=None):
        fieldsets = []
        if obj is None:
            fieldsets = (
                ("О файле", {
                          'fields': (("title", "ident"), ("type_file"), "comment_dev"),
                }),
            )

        # binary file
        if obj is not None and obj.type_file in ['bin', 'archive']:
            if obj.download_link is None: # with file
                fieldsets = (
                    ("Информация", {
                        'fields': ("created", "changed", "version")
                    }),
                    ("О файле", {
                        'fields': (("title", "ident"), "download_link", ("type_file", "file",), "download_auto", "download_order", "comment_dev")
                    }),
                    ("Параметры на стороне клиента", {
                        'fields': ("path_to", )
                    }),
                )
            else: # without file
                fieldsets = (
                    ("Информация", {
                        'fields': ("created", "changed", "version")
                    }),
                    ("О файле", {
                        'fields': (
                        ("title", "ident"), "download_link", ("type_file", "download_auto", "download_order"),
                        "comment_dev")
                    }),
                    ("Параметры на стороне клиента", {
                        'fields': ("path_to",)
                    }),
                )

        # text file
        if obj is not None and obj.type_file not in ['bin', 'archive']:
            fieldsets = (
                ("Информация", {
                    'classes': ('collapse',),
                    'fields': ("created", "changed", "version")
                }),
                ("О файле", {
                    'fields': (("title", "ident"), ("type_file", "enable", "download_auto"), "comment_dev")
                }),
                ("Файл", {
                    'fields': ("text_content", )
                }),
                ("Параметры на стороне клиента", {
                    'fields': ("path_to", )
                }),
            )

        return  fieldsets
