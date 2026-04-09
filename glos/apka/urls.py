from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('glosowania/', views.glosowania, name='glosowania'),
    path('vote/<int:choice_id>/', views.vote, name='vote'),
    path('dodaj/', views.dodaj_glosowanie, name='dodaj_glosowanie'),
    path('onas/', views.onas, name='onas'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]