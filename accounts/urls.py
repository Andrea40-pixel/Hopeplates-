from django.urls import path
from . import views

urlpatterns = [
    path('landing/',views.landing,name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('donar_dashboard/', views.donar_dashboard, name='donar_dashboard'),
    path('add_food/', views.add_food, name='add_food'),
    path('save_food/', views.save_food, name='save_food'),
    path('display_food/', views.display_food, name='display_food'),
path('edit_food/<int:food_id>/', views.edit_food, name='edit_food'),
path('update_food/<int:food_id>/', views.update_food, name='update_food'),
path('delete_food/<int:food_id>/', views.delete_food, name='delete_food'),
path('logout_view/', views.logout_view, name='logout_view'),
    path('view-requests/', views.view_requests, name='view_requests'),
path("accept-request/<int:request_id>/", views.accept_request, name="accept_request"),
path("reject-request/<int:request_id>/", views.reject_request, name="reject_request"),
path('donor-food-status/', views.donor_food_status, name='donor_food_status')


]