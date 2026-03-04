from django.urls import path
from . import views

urlpatterns = [path('ngo_dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
               path('all_products/', views.all_products, name='all_products'),
               path('single_product/<int:donation_id>/', views.single_product, name='single_product'),
path("send-request/<int:donation_id>/", views.send_request, name="send_request"),
path('ngo/notifications/', views.ngo_notifications, name='ngo_notifications'),
path('ngo/logout/', views.ngo_logout, name='ngo_logout'),
               path('about/',views.about,name='about'),
               path('contact/', views.contact, name='contact'),
               path('save_contact',views.save_contact,name='save_contact')
              ]