from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def cargo_login(req):
    if 'admin' in req.session:
        # req.session.flush()
        return redirect(admin_home)
    else:
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['admin']=uname     #create
                    return redirect(admin_home)
                else:
                    req.session['user']=uname
                    return redirect(cargo_home)
            else:
                messages.warning(req,'invalid username or password')
                return redirect(cargo_login)
    return render(req,'login.html')

def cargo_logout(req):
    logout(req)
    req.session.flush()
    return redirect(cargo_login)

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        send_mail('Accout Registration', 'Your Sportix account registration is successfull', settings.EMAIL_HOST_USER, [email])
        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
        except:
            messages.warning(req,'user details already exists')
            return redirect(register)
        return redirect(cargo_login)
    else:
        return render(req,'register.html')






# --------admin-----------------------
def admin_home(req):
    if 'admin' in req.session:
        car=Car.objects.all()
        return render(req,'admin/admin_home.html',{'cars':car})
    else:
        return render(cargo_login)

def add_car(req):
    if req.method=='POST':
        name=req.POST['name']
        brand=req.POST['brand']
        fuel=req.POST['fuel']
        category=req.POST['category']
        seats=req.POST['num_of_seats']
        price=req.POST['price_per_day']
        status=req.POST['is_available']
        file=req.FILES['image']
        data=Car.objects.create(name=name,brand=brand,fuel=fuel,num_of_seats=seats,image=file,price_per_day=price,is_available=status,category=Category.objects.get(category=category))
        data.save()
    return render(req,'admin/add_car.html')

def add_category(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            category=req.POST['category']
            data=Category.objects.create(category=category)
            data.save()
            return redirect(add_category)
        else:
            data=Category.objects.all()
            return render(req,'admin/add_category.html',{'data':data})
    else:
         return redirect(cargo_home)


# ---------user-----------------------
def cargo_home(req):
    # if 'user' in req.session:
    #     return render(req,'user/user_home.html')
    # else:
    #     return render(cargo_login)
    return render(req,'user/user_home.html')