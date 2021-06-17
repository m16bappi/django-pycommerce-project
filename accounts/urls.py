from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('active/<uidb64>/<token>/', AccountActive, name='active'),
    path('forget-password/', forgetPassword, name='forget-password'),
    path('reset-password-valided/<uidb64>/<token>/', resetPasswordValided, name='reset-password-valided')
]
