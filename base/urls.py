from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.HomeView, name='home'),
    path('topic/<str:pk>', views.topicView, name='topic'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name = 'logout'),
]