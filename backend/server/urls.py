"""
URL Configuration for Forgotten Ruin MUD

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')),

    # Authentication
    path('auth/', include('accounts.urls')),

    # Game interface (if serving templates)
    # path('', include('game.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site configuration
admin.site.site_header = "Forgotten Ruin MUD Administration"
admin.site.site_title = "Forgotten Ruin Admin"
admin.site.index_title = "Game Management"
