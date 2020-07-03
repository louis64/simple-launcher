from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class FileControl(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=255)
    ident = models.CharField(verbose_name=_("ident"), max_length=255, unique=True)
    comment_dev = models.TextField(verbose_name=_("comment_dev"))

    enable = models.BooleanField(default=True, verbose_name=_("enable"))
    created = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name=_("created"))
    changed = models.DateTimeField(auto_created=True, auto_now_add=True,verbose_name=_("changed"))

    version = models.CharField(max_length=32, verbose_name=_("version"))

    download_auto = models.BooleanField(default=True, verbose_name=_("download_auto"), help_text =_("help_text"))

    download_order = models.SmallIntegerField(default=0, verbose_name=_("download_order"), help_text=_("download_order"))

    download_link = models.CharField(max_length=4000, null=True, blank=True, default=None, verbose_name=_("download_link"), help_text=_("download_link"))

    type_files = (
        ("archive", "archive"),
        ("batchfile", "batchfile"),
        ("bin", "bin"),
        ("html", "html"),
        ("ini", "ini"),
        ("javascript", "javascript"),
        ("json", "json"),
        ("powershell", "powershell"),
        ("python", "python"),
        ("out_link", "out_link"),
        ("sh", "bash"),
        ("sql", "sql"),
        ("text", "text"),
        ("vbscript", "vbscript"),
        ("xml", "xml"),
    )
    out_link = models.CharField(default=None, null=True, max_length=500)

    type_file = models.CharField(choices=type_files, default="bin", max_length=10, verbose_name=_("type_file"))
    text_content = models.TextField(verbose_name=_("text_content"))

    file = models.FileField(upload_to='media/last/', verbose_name=_("file"), default=None, null=True, blank=True)
    is_archive = models.BooleanField(default=False,verbose_name=_("is_archive"), help_text=_("is_archive_help"))
    path_to = models.CharField(max_length=255, verbose_name=_("path_to"), default='{{install_dir}}/{file_name}')

    def __str__(self):
        return "%s: %s" % (self.title, self.ident)

    class Meta:
        verbose_name_plural = _("verbose_name_plural")
        verbose_name = _("verbose_name")
