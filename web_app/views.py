from django.shortcuts import render,redirect
from accounts.models import FoodDonation,ProfileDb
from django.contrib.auth.decorators import login_required
from.models import  Notification,ContactDb

from django.contrib.auth import logout
from django.utils import timezone

# Create your views here.

@login_required
def ngo_dashboard(request):
    profile = ProfileDb.objects.get(user=request.user)

    if profile.user_type.strip().lower() != "ngo":
        return redirect("donar_dashboard")  # block donor from NGO page

    latest_donations = FoodDonation.objects.all().order_by('-id')[:8]
    return render(request, 'ngo_dashboard.html', {'latest_donations': latest_donations})




def all_products(request):
    today = timezone.now().date()
    donations = FoodDonation.objects.filter(
        expiry_date__gte=today,
        status="Available"
    )
    return render(request, 'all_products.html', {'donations':donations},)
def single_product(request,donation_id):
    donations = FoodDonation.objects.get(id=donation_id)
    return render(request, 'single_product.html', {'donation':donations})
from .models import PickupRequest

from django.shortcuts import redirect, get_object_or_404
from .models import PickupRequest, FoodDonation
def send_request(request, donation_id):
    donation = FoodDonation.objects.get(id=donation_id)

    # Check donation is available
    if donation.status != "Available":
        return redirect("ngo_dashboard")

    PickupRequest.objects.create(
        donation=donation,
        ngo=request.user,
        donor=donation.donor
    )

    return redirect("ngo_dashboard")
def ngo_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Optional: mark notifications as read when opened
    notifications.update(is_read=True)

    return render(request, "ngo_notifications.html", {
        "notifications": notifications
    })
def ngo_logout(request):
    logout(request)
    return redirect('login')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def save_contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject= request.POST['subject']
        message = request.POST['message']

        obj = ContactDb(

            name=name,
            email=email,
            subject=subject,
            message=message)
        obj.save()

        return render(request,'contact.html')







