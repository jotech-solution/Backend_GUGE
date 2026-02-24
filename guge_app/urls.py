from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schools/', views.school_list, name='school_list'),
    path('schools/add/', views.school_form, name='school_add'),
    path('provinces/', views.province_list, name='province_list'),
    path('divisions/', views.division_list, name='division_list'),
    path('subdivisions/', views.subdivision_list, name='subdivision_list'),
    path('cities/', views.city_list, name='city_list'),
    path('territories/', views.territory_list, name='territory_list'),
    path('questionnaires/', views.question_template_list, name='question_template_list'),
    path('questions/', views.question_list, name='question_list'),
    path('recoltes/<str:type_recolte>/', views.recolte_list, name='recolte_list'),
    path('recoltes/validate/<uuid:pk>/', views.recolte_validate, name='recolte_validate'),
    path('recoltes/reject/<uuid:pk>/', views.recolte_reject, name='recolte_reject'),

]

# router = DefaultRouter()
# router.register(r"schools", SchoolViewSet, basename="school")
# router.register(r"divisions", DivisionViewSet, basename="division")