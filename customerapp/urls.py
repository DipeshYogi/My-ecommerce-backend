from django.urls import path
from . import views


urlpatterns = [
    path('address/<int:id>/', views.GetUserAddress.as_view(), name ='get_address'),
    path('address/add/', views.AddUserAddress.as_view(), name ='add_address'),
    path('address/update/<int:id>/', views.EditUserAddress.as_view(), name ='update_address'),
    path('address/update/active/<int:addrId>/', views.UpdateActiveAddress.as_view()),
    path('address/delete/<int:addrId>/', views.DeleteUserAddress.as_view(), name='delete_address')
]