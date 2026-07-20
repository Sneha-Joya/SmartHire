"""
URL configuration for quicklance project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "QuickLance Administration"
admin.site.site_title = "QuickLance Admin"
admin.site.index_title = "Welcome to QuickLance Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),
    path('accounts/', include('accounts.urls')),
    path('messaging/', include('messaging.urls')),
    path('reviews/', include('reviews.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

