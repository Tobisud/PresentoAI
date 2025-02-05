"""
URL configuration for presentoapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from presento import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('list-static/', views.list_static_files, name='list-static'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
    path('upload/', views.upload_file, name='upload_file'),
    path('run_script/<str:process_id>/', views.run_python_script, name='run_python_script'),
    path('check_status/<str:process_id>/', views.check_status, name='check_status'),
    path('<uuid:pk>/download/', views.download_file, name='download_file'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)