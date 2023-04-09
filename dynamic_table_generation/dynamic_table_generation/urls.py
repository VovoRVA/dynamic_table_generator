from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [

    # Route to the admin panel
    path('admin/', admin.site.urls),

    # Route to the test app
    path('api/', include('test.urls')),
    # path('api/docs/', schema_view)

]
