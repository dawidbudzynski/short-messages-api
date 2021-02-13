from django.contrib import admin
from django.urls import include, path

from message.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/message/', include('message.urls')),
]
