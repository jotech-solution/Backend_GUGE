from django.urls import path
from . import views

# new view for bulk adding questions

urlpatterns = [
    path('', views.home, name='home'),
    path('schools/', views.school_list, name='school_list'),
    path('schools/map/', views.school_map, name='school_map'),
    path('schools/add/', views.school_form, name='school_add'),
    path('schools/<int:pk>/', views.school_detail, name='school_detail'),
    path('schools/<int:pk>/edit/', views.school_edit, name='school_edit'),
    path('schools/<int:pk>/delete/', views.school_delete, name='school_delete'),
    path('provinces/', views.province_list, name='province_list'),
    path('divisions/', views.division_list, name='division_list'),
    path('subdivisions/', views.subdivision_list, name='subdivision_list'),
    path('cities/', views.city_list, name='city_list'),
    path('territories/', views.territory_list, name='territory_list'),
    path('questionnaires/', views.question_template_list, name='question_template_list'),
    path('questionnaires/<uuid:pk>/', views.question_template_detail, name='question_template_detail'),
    path('questionnaires/<uuid:pk>/edit/', views.question_template_edit, name='question_template_edit'),
    path('questionnaires/<uuid:pk>/delete/', views.question_template_delete, name='question_template_delete'),
    path('questionnaires/<uuid:template_id>/add-questions/', views.question_add_multiple, name='question_add_multiple'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/<uuid:pk>/edit/', views.question_edit, name='question_edit'),
    path('questions/<uuid:pk>/delete/', views.question_delete, name='question_delete'),
    path('groupes/', views.groupe_list, name='groupe_list'),
    path('groupes/<uuid:pk>/edit/', views.groupe_edit, name='groupe_edit'),
    path('groupes/<uuid:pk>/delete/', views.groupe_delete, name='groupe_delete'),
    path('campagnes/', views.campaign_list, name='campaign_list'),
    path('campagnes/<uuid:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campagnes/<uuid:pk>/edit/', views.campaign_edit, name='campaign_edit'),
    path('campagnes/<uuid:pk>/delete/', views.campaign_delete, name='campaign_delete'),
    path('recoltes/<str:type_recolte>/', views.recolte_list, name='recolte_list'),
    path('recoltes/<uuid:pk>/view/', views.recolte_detail, name='recolte_detail'),
    path('recoltes/validate/<uuid:pk>/', views.recolte_validate, name='recolte_validate'),
    path('recoltes/reject/<uuid:pk>/', views.recolte_reject, name='recolte_reject'),

]

# router = DefaultRouter()
# router.register(r"schools", SchoolViewSet, basename="school")
# router.register(r"divisions", DivisionViewSet, basename="division")