from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from core.views import criar_admin_temporario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("criar-admin-temporario/", criar_admin_temporario),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)