from django.urls import path
from . import views

app_name="expense_tracker"

urlpatterns = [
    path('', views.user_home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('passwordchange/', views.user_passwordchange, name='passwordchange'),
    path('addexpense/', views.addexpense, name='addexpense'),
    path('displayexpense/', views.displayexpense, name='displayexpense'),
]

 