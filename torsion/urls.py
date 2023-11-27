from django.contrib import admin
from django.urls import path, include
from torsion.conf import ADMIN_SITE_URL


urlpatterns = [
    path(ADMIN_SITE_URL, admin.site.urls),
    path('api/', include('LuckySpinTracker.urls'))
]
