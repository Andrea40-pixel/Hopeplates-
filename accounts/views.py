from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ProfileDb
from django.contrib import messages
from datetime import datetime
from .models import FoodDonation
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from web_app.views import *
from web_app.models import Notification



def landing(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        phone = request.POST['phone']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        ProfileDb.objects.create(
            user=user,
            user_type=user_type,
            phone=phone
        )

        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            try:
                profile = ProfileDb.objects.get(user=user)

                user_type = profile.user_type.strip().lower()
                print("USER TYPE:", user_type)

                if user_type == "donor":
                    return redirect('donar_dashboard')

                elif user_type == "ngo":
                    return redirect('ngo_dashboard')

            except ProfileDb.DoesNotExist:
                messages.error(request, "Profile not found")

            return redirect("login")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

@login_required
def donar_dashboard(request):
    profile = ProfileDb.objects.get(user=request.user)

    if profile.user_type.strip().lower() != "donor":
        return redirect("ngo_dashboard")  # block NGO from donor page

    return render(request, "donar_dashboard.html")

def add_food(request):
    return render(request, "add_food.html")



def save_food(request):
    if request.method == "POST":
        donar_name = request.POST['donar_name']
        shop_name = request.POST['shop_name']
        food_name = request.POST.get('food_name')
        quantity = request.POST.get('quantity')
        description=request.POST.get('description')
        location = request.POST.get('location')
        expiry_date = request.POST.get('expiry_date')
        status = request.POST.get('status')

        image = request.FILES.get('image')

        obj = FoodDonation(
            donor=request.user,
            shop_name=shop_name,
            food_name=food_name,
            quantity=quantity,
            description=description,
            location=location,
            expiry_date=expiry_date,
            image=image,
            status= "Available"
        )

        obj.save()

        return redirect('donar_dashboard')
@login_required
def display_food(request):
    donations = FoodDonation.objects.filter(donor=request.user)
    today = timezone.now().date()

    return render(request, "display_food.html", {
        'donations': donations,
        'today': today
    })

def edit_food(request, food_id):
    data = FoodDonation.objects.get(id=food_id)
    return render(request, 'edit_food.html', {'data': data})
def update_food(request, food_id):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        food_name = request.POST.get('food_name')
        quantity = request.POST.get('quantity')
        description=request.POST.get('description')
        location = request.POST.get('location')
        expiry_date = request.POST.get('expiry_date')
        if not expiry_date:
            expiry_date = FoodDonation.objects.get(id=food_id).expiry_date
        status = request.POST.get('status')
        if not status:
            status = FoodDonation.objects.get(id=food_id).status

        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
        except MultiValueDictKeyError:
            file = FoodDonation.objects.get(id=food_id).image

        FoodDonation.objects.filter(id=food_id).update(
            shop_name=shop_name,
            food_name=food_name,
            quantity=quantity,
            description=description,
            location=location,
            expiry_date=expiry_date,
            status=status,
            image=file
        )

        return redirect('display_food')
def delete_food(request, food_id):
    delete_data = FoodDonation.objects.filter(id=food_id)
    delete_data.delete()
    return redirect('display_food')
def logout_view(request):
    logout(request)
    return redirect('login')
def view_requests(request):
    donations = FoodDonation.objects.filter(donor=request.user)

    requests = PickupRequest.objects.filter(
        donor=request.user,
        status="available"
    )

    return render(request, "view_requests.html", {
        "donations": donations,
        "requests": requests
    })
def accept_request(request, request_id):
    pickup = PickupRequest.objects.get(id=request_id)

    pickup.status = "Accepted"
    pickup.save()

    # Update donation status
    pickup.donation.status = "Accepted"
    pickup.donation.save()

    Notification.objects.create(
        user=pickup.ngo,
        message=(
            f"Your pickup request for {pickup.donation.food_name} was accepted! "
            f"Please collect your food within two hours of this confirmation!"
        ))

    return redirect("donar_dashboard")


def reject_request(request, request_id):
    pickup = PickupRequest.objects.get(id=request_id)

    pickup.status = "Rejected"
    pickup.save()

    messages.error(
        request,
        f"Your pickup request for {pickup.donation.food_name} was rejected."
    )

    return redirect("donar_dashboard")



















