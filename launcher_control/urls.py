"""launcher_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import  url, include
from django.conf.urls.static import static
from apps.control.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^check/$', CheckUpdate.as_view(), name='statistic'),
    url(r'^file/(?P<ident>[a-zA-Z\.0-9_]+)/$', GetFile.as_view(), name='statistic'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
