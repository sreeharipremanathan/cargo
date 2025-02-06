from django.urls import path
from . import views

urlpatterns=[
    path('',views.cargo_home),
    path('login',views.cargo_login),
    path('register',views.register),
    path('logout',views.cargo_logout),
    # -------admin----------
    path('admin_home',views.admin_home),
    path('add_product',views.add_product),
    path('add_category',views.add_category),
]