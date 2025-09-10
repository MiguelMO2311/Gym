from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_list, name='activities_list'),  # ← usa el nombre correcto de la función
    path('<int:id>/', views.activity_detail, name='activity_detail'),
    path('<int:id>/edit/', views.activity_edit, name='activity_edit')

]
