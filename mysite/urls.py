from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('administration/', include('administration.urls', namespace='administration')),
    path('scheduler/', include('scheduler.urls', namespace='scheduler')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
