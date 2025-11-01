"""
URL configuration for wallets_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from wallets.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('wallets.urls')),  # Предполагаю, что API под /api/v1/ — скорректируйте, если нужно
    path('', include('wallets.urls')),  # Это подключит все роуты из wallets/urls.py, включая index
]