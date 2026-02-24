"""
URL configuration for backend_guge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from backend_guge import settings
from guge_app.views import home
from django.conf.urls.static import static
from guge_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('manage_guge/', include('guge_app.urls')),
    path('users/', include('mng_users.urls')),
    # APIS
    path('api/schools/', views.SchoolViewSet.as_view({'get': 'list', 'post': 'create'}), name='school_api_list'),
    path('api/question-templates/', views.QuestionTemplateViewSet.as_view({'get': 'list'}), name='question_template_api_list'),
    # TOKENS
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


