"""
URL Configuration for euro_bakshish project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    """API root endpoint that returns available API endpoints."""
    return JsonResponse({
        'message': 'Euro Bakshish API',
        'version': '1.0',
        'endpoints': {
            'users': '/api/users/',
            'trips': '/api/trips/',
            'ratings': '/api/ratings/',
            'docs': '/api/docs/',
            'schema': '/api/schema/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/users/', include('apps.users.urls')),
    path('api/trips/', include('apps.trips.urls')),
    path('api/ratings/', include('apps.ratings.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
