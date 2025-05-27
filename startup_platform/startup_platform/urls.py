from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
def home(request):
    return HttpResponse("You are on wrong place bache")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/auth/', include('accounts.urls')),
    path('api/startups/', include('startups.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
