from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users_home, name='users_home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.delete_profile, name='delete_profile'),
    path('panel/athlete/', views.athlete_panel, name='athlete_panel'),
    path('panel/coach/', views.coach_panel, name='coach_panel'),

]

