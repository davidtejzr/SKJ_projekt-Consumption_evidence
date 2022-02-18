"""tej0017_skj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from app import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vehicle/add/', views.vehicleAdd, name='vehicleAdd'),
    path('vehicle/add/getModel', views.vehicleAddGetModel, name='vehicleAddGetModel'),
    path('vehicle/add/submit', views.vehicleAddPost, name='vehicleAddPost'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/edit/$', views.vehicleEditPost, name='vehicleEditPost'),
    url(r'^vehicle/addTank/(?P<v_id>[0-9]+)/submit/$', views.vehicleAddTankPost, name='vehicleAddTankPost'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/records$', views.vehicleDetailRecords, name='vehicleDetailRecords'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/consumption$', views.vehicleDetailConsumption, name='vehicleDetailConsumption'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/refuel', views.vehicleDetailRefuel, name='vehicleDetailRefuel'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/edit$', views.vehicleDetailEdit, name='vehicleDetailEdit'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/consumptionCalc/$', views.vehicleConsumptionCalc, name='vehicleConsumptionCalc'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/recordDetail/(?P<r_id>[0-9]+)$', views.vehicleRecordDetail, name='vehicleRecordDetail'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/edit/delete$', views.vehicleEditRemove, name='vehicleEditRemove'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/recordDetail/(?P<r_id>[0-9]+)/delete$', views.vehicleRecordRemove, name='vehicleRecordRemove'),
    url(r'^vehicle/(?P<v_id>[0-9]+)/edit/uploadImage$', views.vehicleDetailEditUploadImg, name='vehicleDetailEditUploadImg'),
    path('vehicle/getTankStation', views.getTankStation, name='getTankStation'),
    path('vehicle/getTankStationMap', views.getTankStationMap, name='getTankStationMap'),
    path('vehicle/getTankStationMapRecordDetail', views.getTankStationMap, name='getTankStationMapRecordDetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
