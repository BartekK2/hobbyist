from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('posty.urls')),
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
]

handler404 = 'posty.views.error_404_view'