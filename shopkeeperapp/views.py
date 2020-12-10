from django.shortcuts import render
from rest_framework.views import APIView
from .models import ShopProfile, ShopItems, Category
from .serializers import ShopProfileSerializer, ShopProfileUpdateSerializer, \
                         ShopItemSerializer, ShopItemDetailsSerializer, \
                         ShopItemUpdateSerializer, CategorySerializer, \
                         GetShopByCatSerializer, GetCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class ShopProfileList(APIView):
    """
    API for getting all Shop Profiles and add new Shop Profiles
    """   
    serializer_class = ShopProfileSerializer

    def get(self,request,format=None):
        shop_prof = ShopProfile.objects.all()
        serializer = self.serializer_class(shop_prof, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopProfileDetail(APIView):
    """API for getting and updating Shop Profiles"""
    serializer_class = ShopProfileUpdateSerializer

    def get(self,request,pk,format=None):
        try:
            shop_prof = ShopProfile.objects.get(id=pk)
            return Response({
                "ShopInfo": ShopProfileSerializer(shop_prof).data})
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})

    def put(self,request,pk , format=None):
        try:
            shop_prof = ShopProfile.objects.get(id=pk)
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})
        serializer = self.serializer_class(shop_prof, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)


class GetItemsByShop(APIView):
    """Fetch Shop items by Shop Id"""
    # serializer_class = ShopItemSerializer

    # def get(self, request, shopid, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         try:
    #             shopid = serializer.data['shopid']
    #             items = ShopItems.objects.filter(shopid=shopid)
    #             item_data = ShopItemDetailsSerializer(items, many=True)
    #             return Response(item_data.data)
    #         except:
    #             return Response({"status":status.HTTP_404_NOT_FOUND})
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, shopid, format=None):
            try:
                items = ShopItems.objects.filter(shopid=shopid)
                item_data = ShopItemDetailsSerializer(items, many=True)
                return Response(item_data.data)
            except:
                return Response({"status":status.HTTP_404_NOT_FOUND})
        
            

class AddItemsByShop(APIView):
    """Add new items for shops"""

    def post(self, request, format=None):
        serializer = ShopItemDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "itemInfo": serializer.data,
                "status": status.HTTP_201_CREATED
            })
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UpdateItemByShop(APIView):
    """Update the item for a shop"""

    def put(self, request, id, shopid):
        try:
            item_instance = ShopItems.objects.get(id=id, shopid=shopid)
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})
        
        serializer = ShopItemUpdateSerializer(item_instance, \
                                              data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCategory(APIView):
    """Add new categories"""
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetCategoryInfo(APIView):
    """Retreive category information"""

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = GetCategorySerializer(categories, many=True, context={"request": request})

        return Response(serializer.data)


class GetShopsByCategory(APIView):
    """Get all shops by category"""

    def post(self, request, format=None):
        serializer = GetShopByCatSerializer(data=request.data)
        if serializer.is_valid():
            cat = serializer.data['cat_name']
            shops = ShopProfile.objects.filter(category=cat)
            shop_ser = ShopProfileSerializer(shops, many=True)

            return Response(shop_ser.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
