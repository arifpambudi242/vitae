from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('response/', views.response, name='response'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('forgot_check/', views.forgot_check, name='forgot-check'),
    path('forgot_verification/<uid>/', views.forgot_verification, name='forgot-verification'),
    


]
