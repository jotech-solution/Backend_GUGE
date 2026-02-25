from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logIn, name='login'),
    path('logout-confirm/', views.ask_logout, name='ask_logout'),
    path('logout/', views.logOut, name='logout'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('profile/', views.profile, name='profile'),
    
    # Utilisateurs
    path('user-list/', views.user_list, name='user_list'),
    path('user-add/', views.user_add, name='user_add'),
    path('user-edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user-delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('user-toggle/<int:pk>/', views.user_toggle_status, name='user_toggle_status'),
    
    # Groupes
    path('group-list/', views.group_list, name='group_list'),
    path('group-add/', views.group_add, name='group_add'),
    path('group-edit/<int:pk>/', views.group_edit, name='group_edit'),
]