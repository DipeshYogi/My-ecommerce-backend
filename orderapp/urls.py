from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateOrder.as_view()),
    path('my-orders/', views.GetUserOrders.as_view())
]