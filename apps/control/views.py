from rest_framework import views
from rest_framework.response import Response
from .models import *
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import os
from django.conf import settings


class CheckUpdate(views.APIView):

    def post(self, request):
        check_file = request.data

        files_download = []

        result = FileControl.objects.filter(enable=True, download_auto=True).values("ident", "download_link","file", "path_to", "version", "title", "type_file").order_by('download_order')

        for f in result:
            # если файла из базы нет в списке запрашиваемых файлах и если их версии отличаются
            if f["ident"] not in check_file or check_file[f["ident"]] != f["version"]:
                file_info = {
                    "ident": f["ident"],
                    "type_file": f["type_file"],
                    "org_name": os.path.basename(f["file"]),
                    "version": f["version"],
                    "path_to": f["path_to"].format(file_name=f["title"]),
                }

                if f["download_link"] is not None:
                    file_info["download_link"] = f["download_link"]
                else:
                    url_server = request._stream._current_scheme_host
                    if f["file"] is not None and f["file"] != '':
                        file_info["download_link"] = "{url_server}{media_url}{file}".format(media_url=settings.MEDIA_URL,url_server=url_server, file=f["file"])
                    else:
                        file_info["download_link"] = "{url_server}/file/{ident}".format(url_server=url_server, ident=f["ident"])

                files_download.append(file_info)

        return Response(files_download, status=200)


class GetFile(views.APIView):

    def get(self, request, ident):
        result = FileControl.objects.filter(ident=ident).values("file", "text_content", "type_file", "title")[0]

        if result['type_file'] not in ['bin', 'archive']:
            response = HttpResponse(result['text_content'] , content_type='Content-Type: text/html; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="%s"' % result['title']
        else:
            file_handle = os.path.join(settings.BASE_DIR, result['file'])

            document = open(file_handle, 'rb')

            response = HttpResponse(FileWrapper(document), content_type='Content-Type: text/html; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="%s"' % result['title']
            response['Content-Length'] = os.path.getsize(file_handle)

        return response

