from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import datetime

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
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        
        try:
            # Validate password strength
            validate_password(password)
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.warning(req, 'User with this email already exists.')
                return redirect(register)

            # Create user if valid
            user = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            user.save()

            # Send registration success email
            send_mail(
                'Account Registration',
                'Your Cargo account registration was successful.',
                settings.EMAIL_HOST_USER,
                [email]
            )

            messages.success(req, 'Registration successful. Please log in.')
            return redirect(cargo_login)

        except ValidationError as e:
            messages.error(req, ', '.join(e))  # Show password validation errors
            return redirect(register)
        
    return render(req, 'register.html')






# --------admin-----------------------
def admin_home(req):
    if 'admin' in req.session:
        car=Car.objects.all()
        return render(req,'admin/admin_home.html',{'cars':car})
    else:
        return render(cargo_login)

def add_car(req):
    if 'admin' in req.session:
        if req.method=='POST':
            name=req.POST['name']
            brand=req.POST['brand']
            fuel=req.POST['fuel']
            categoryy=req.POST['category']
            seats=req.POST['num_of_seats']
            price=req.POST['price_per_day']
            status = req.POST.get('is_available') == 'on'
            file=req.FILES['image']
            data=Car.objects.create(name=name,brand=brand,image=file,fuel=fuel,category=Category.objects.get(category=categoryy),
                                    num_of_seats=seats,price_per_day=price,
                                    is_available=status
                                    )
            data.save()
        else:
            data=Category.objects.all()
            return render(req,'admin/add_car.html',{'data':data})
    return render(req,'admin/add_car.html')

def edit_car(req, id):
    if req.method == 'POST':
        name = req.POST['name']
        brand = req.POST['brand']
        img = req.FILES.get('image') 
        fuel = req.POST['fuel']
        seats = req.POST['num_of_seats']
        price = req.POST['price_per_day']
        status = req.POST.get('is_available') == 'on'

        if img:
            Car.objects.filter(pk=id).update(
                name=name, brand=brand, image=img, fuel=fuel,
                num_of_seats=seats, price_per_day=price,
                is_available=status
            )
            data = Car.objects.get(pk=id)
            data.image = img
            data.save()
        else:
            Car.objects.filter(pk=id).update(
                name=name, brand=brand, fuel=fuel,
                num_of_seats=seats, price_per_day=price,
                is_available=status
            )

        return redirect(admin_home)
    else:
        data = Car.objects.get(pk=id)
        return render(req, 'admin/edit_car.html', {'data': data})


def delete_car(req,id):
    data=Car.objects.get(pk=id)
    url=data.image.url
    url=url.split('/')[-1]
    os.remove('media/'+url)
    data.delete()
    return redirect(admin_home)

def delete_category(req,id):
    data=Category.objects.get(pk=id)
    data.delete()
    return redirect(add_category)

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


def manage_rentals(request):
    rentals = Rental.objects.all().order_by("-id")
    return render(request, "admin/manage_rentals.html", {"rentals": rentals})

def update_rental_status(request, rental_id, status):
    rental = get_object_or_404(Rental, id=rental_id)

    if status in ["Approved", "Rejected", "Completed"]:
        rental.status = status
        rental.save()
        
        if status == "Approved":
            subject = "Your Car Rental Request Has Been Approved!"
            message = f"Hello {rental.user.username},\n\nYour car rental request for {rental.car.name} has been approved.\n\nStart Date: {rental.start_date}\nEnd Date: {rental.end_date}\nTotal Price: ₹{rental.total_price}\n\nThank you for using our service!\n\nBest Regards,\nDrive Your Way! \nCarGo Rental Team"
            recipient_email = rental.user.email
            sender_email = settings.EMAIL_HOST_USER

            send_mail(subject, message, sender_email, [recipient_email])

        elif status == "Completed":
            subject = "Your Car Rental Has Been Completed!"
            message = f"Hello {rental.user.username},\n\nYour car rental for {rental.car.name} has been Completed.\n\nStart Date: {rental.start_date}\nEnd Date: {rental.end_date}\nTotal Price: ₹{rental.total_price}\n\nThank you for using our service!\n\nBest Regards,\nDrive Your Way! \nCarGo Rental Team"
            recipient_email = rental.user.email
            sender_email = settings.EMAIL_HOST_USER

            send_mail(subject, message, sender_email, [recipient_email]) 

        messages.success(request, f"Rental status updated to {status}")
    else:
        messages.error(request, "Invalid status update")

    return redirect("manage_rentals")



# ---------user-----------------------
def cargo_home(req):
    data=Car.objects.all()
    cat=Category.objects.all()
    return render(req,'user/user_home.html',{'data':data,"cat":cat})

def view_car(req,id):
    data=Car.objects.get(pk=id)
    cat=Category.objects.all()
    return render(req,'user/view_car.html',{'data':data,"cat":cat})

def contact(req):
    cat=Category.objects.all()
    if req.method == "POST":
        name = req.POST["name"]
        email = req.POST["email"]
        message = req.POST["message"]

        # Send email (Optional: Set up Django email settings)
        send_mail(
            subject=f"New Contact Form Submission from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=email,
            recipient_list=["yourbusiness@email.com"],  # Replace with your email
            fail_silently=True,
        )

        messages.success(req, "Your message has been sent successfully!")
        return redirect("contact_us")  
    return render(req,'user/contact.html',{"cat":cat})

def rent_car(request, id):
    cat=Category.objects.all()
    car = get_object_or_404(Car, pk=id)

    if not car.is_available:
        messages.error(request, "Sorry, this car is not available for rent.")
        return redirect(view_car, id=car.pk)

    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date >= end_date:
                messages.error(request, "End date must be after start date.")
                return redirect(rent_car, id=car.pk)

            existing_rental = Rental.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date,
                status__in=["Pending", "Approved"]
            ).exists()

            if existing_rental:
                messages.error(request, "This car is already booked for the selected dates.")
                return redirect(rent_car, id=car.pk)

            num_days = (end_date - start_date).days
            total_price = num_days * car.price_per_day

            rental = Rental.objects.create(
                user=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
                num_days=num_days,
                total_price=total_price,
                status="Pending",  
            )

            messages.success(request, "Your rental request has been submitted successfully!")
            return redirect(rent_car, id=car.pk)

    return render(request, "user/rent_car.html", {"car": car,"cat":cat})

def view_category(req,id):
    category = Category.objects.get(pk=id)
    cat=Category.objects.all()
    car = Car.objects.filter(category=category)
    print(car)
    print(category)
    return render(req, 'user/category.html', {'category': category,'car': car,"cat":cat})

def user_profile(req):
    cat=Category.objects.all()
    rentals = Rental.objects.filter(user=req.user).order_by("-id")
    return render(req,'user/user_profile.html',{'rentals':rentals,'cat':cat})

def update_username(request):
    cat=Category.objects.all()
    if request.method == "POST":
        new_first_name = request.POST.get("username")
        if new_first_name:
            request.user.first_name = new_first_name
            request.user.save()
            messages.success(request, "Username updated successfully!")
        else:
            messages.error(request, "Username cannot be empty.")
    return redirect(user_profile)