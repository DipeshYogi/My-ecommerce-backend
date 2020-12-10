from django.urls import path
from . import views


urlpatterns = [
    path('address/<int:id>/', views.GetUserAddress.as_view()),
    path('address/add/', views.AddUserAddress.as_view()),
    path('address/update/<int:id>/', views.EditUserAddress.as_view()),
    path('address/update/active/<int:addrId>/', views.UpdateActiveAddress.as_view()),
    path('address/delete/', views.DeleteUserAddress.as_view())
]