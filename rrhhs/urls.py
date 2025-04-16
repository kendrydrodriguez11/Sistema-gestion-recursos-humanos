"""rrhhs URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from apps.core.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.HomeTemplateView.as_view(),name="home"),
    path('modules/', home.ModuloTemplateView.as_view(),name="modules"),
    path('core/',include('apps.core.urls',namespace="core") ),
    path('personal_file/',include('apps.personal_file.urls',namespace="personal_file") ),
    path('security/',include('apps.security.urls',namespace="security") ),
    path('payment_role/',include('apps.payment_role.urls',namespace="payment_role") ),
    path('personal_training/',include('apps.personal_training.urls',namespace="personal_training") ),
    path('gestion_venta/',include('apps.gestion_venta.urls',namespace="gestion_venta") ),


  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

