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
]
