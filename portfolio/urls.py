from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from core.views import configurar_admin_render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('configurar-admin-render/', configurar_admin_render),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
