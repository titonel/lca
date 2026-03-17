from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('hipertensao/', include('hipertensao.urls')),
    path('anticoagulacao/', include('anticoagulacao.urls')),
]
