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

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GUCE API",
        default_version="v1",
        description="API Documentation du système scolaire",
        contact=openapi.Contact(email="admin@epst.com"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('manage_guge/', include('guge_app.urls')),
    path('users/', include('mng_users.urls')),
    # APIS
    path(
        "api/schools/sync-by-codes/",
        views.sync_schools_by_codes,
        name="sync_schools_by_codes"
    ),
    path('api/me/', views.get_current_user, name='get_current_user'),
    path('api/schools/', views.SchoolViewSet.as_view({'get': 'list', 'post': 'create'}), name='school_api_list'),
    path('api/schools-sync/', views.SchoolSyncViewSet.as_view({'get': 'list'}), name='school_sync_api_list'),
    path('api/recoltes/', views.RecolteViewSet.as_view({'get': 'list', 'post': 'create'}), name='recolte_api_list'),
    path('api/recoltes/<uuid:pk>/', views.RecolteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='recolte_api_detail'),
    path('api/question-templates/', views.QuestionTemplateViewSet.as_view({'get': 'list'}), name='question_template_api_list'),
    # TOKENS
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    # DOCUMENTATION
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


