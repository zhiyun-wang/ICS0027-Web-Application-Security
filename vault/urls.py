from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.entry_list, name='vault'),

    path('vault/', views.entry_list, name='vault'),

    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='vault/login.html',
            redirect_authenticated_user=True,
            next_page='vault'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    path('vault/new/', views.entry_new, name='new'),

    path('vault/<int:pk>/', views.entry_detail, name='detail'),

    path('vault/<int:pk>/edit/', views.entry_edit, name='edit'),

    path('vault/<int:pk>/delete/', views.entry_delete, name='delete'),
]