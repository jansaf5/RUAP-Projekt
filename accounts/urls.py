from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('', views.home, name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)