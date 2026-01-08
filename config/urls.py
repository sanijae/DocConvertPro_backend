"""
URL configuration for DocConvertPro project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """API root endpoint."""
    return Response({
        'message': 'Welcome to DocConvertPro API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api-auth': '/api-auth/',
            'users': '/api/users/',
            'tools': '/api/tools/',
            'billing': '/api/billing/',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/tools/', include('apps.tools.urls')),
    path('api/billing/', include('apps.billing.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
