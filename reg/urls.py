from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name='reg'
urlpatterns = [
    path('signup/', views.user_signup, name = 'user_signup'),
    path('signup/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('profile/profile_pic_update/', views.user_profile_pic_update, name='user_profile_pic_update'),
    path('', views.index, name='index'),
]