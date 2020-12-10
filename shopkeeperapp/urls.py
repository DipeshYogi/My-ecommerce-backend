from django.urls import path
from . import views

urlpatterns = [
    path('shop-profile/', views.ShopProfileList.as_view()),
    path('shop-profile-detail/<int:pk>/', views.ShopProfileDetail.as_view()),
    path('shop-profile/items/<int:shopid>', views.GetItemsByShop.as_view()),
    path('shop-profile/items/add/', views.AddItemsByShop.as_view()),
    path('shop-profile/items/update/<int:id>/<int:shopid>/', \
          views.UpdateItemByShop.as_view()),
    path('categories/', views.GetCategoryInfo.as_view()),
    path('categories/add/', views.AddCategory.as_view()),
    path('categories/shops/', views.GetShopsByCategory.as_view())
]