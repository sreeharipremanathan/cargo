from django.urls import path
from . import views

urlpatterns=[
    path('',views.cargo_home),
    path('login',views.cargo_login),
    path('register',views.register),
    path('logout',views.cargo_logout),
    path('admin_home',views.admin_home),
]