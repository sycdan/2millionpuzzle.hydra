"""
URL configuration for hydra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import logging

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

logger = logging.getLogger(__name__)

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    # Catch annoying errors related to both autoreload and autosave being enabled
    import core.views
    urlpatterns += [
        path('', core.views.index),
    ]
except Exception:
    logger.exception("Failed to load core views")
