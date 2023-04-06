from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    # Route to the admin panel
    path('admin/', admin.site.urls),

    # Route to the test app
    path('api/', include('test.urls')),
]
