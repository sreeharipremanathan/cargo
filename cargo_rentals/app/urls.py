from django.urls import path
from . import views

urlpatterns=[
    path('',views.cargo_home),
    path('login',views.cargo_login),
    path('register',views.register),
    path('logout',views.cargo_logout),
    # -------admin----------
    path('admin_home',views.admin_home),
    path('add_car',views.add_car),
    path('edit_car/<id>',views.edit_car),
    path('add_category',views.add_category),
    path('delete_car/<id>',views.delete_car),
    path('delete_category/<id>',views.delete_category),
    # ------user------------
    path('view_car/<id>',views.view_car),
    path('contact',views.contact),
    path('rent_car/<id>',views.rent_car),
    path('view_category/<id>',views.view_category)
]