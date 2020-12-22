from django.shortcuts import render
from rest_framework.views import APIView
from .models import ShopProfile, ShopItems, Category
from .serializers import ShopProfileSerializer, ShopProfileUpdateSerializer, \
                         ShopItemSerializer, ShopItemDetailsSerializer, \
                         ShopItemUpdateSerializer, CategorySerializer, \
                         GetShopByCatSerializer, GetCategorySerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from db_utils.connect import GetConnection


class ShopProfileList(APIView):
    """
    API for getting all Shop Profiles and add new Shop Profiles
    """   
    serializer_class = ShopProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self,request,format=None):
        shop_prof = ShopProfile.objects.all()
        serializer = self.serializer_class(shop_prof, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(shopid=request.user)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopProfileDetail(APIView):
    """API for getting and updating Shop Profiles"""
    serializer_class = ShopProfileUpdateSerializer

    def get(self,request,format=None):
        try:
            shop_prof = ShopProfile.objects.get(shopid=request.user.id)
            return Response({"ShopInfo": ShopProfileSerializer(shop_prof).data})
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})

    def put(self, request, format=None):
        try:
            shop_prof = ShopProfile.objects.get(shopid=request.user.id)
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})
        serializer = self.serializer_class(shop_prof, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)


class GetItemsByShop(APIView):
    """Fetch Shop items by user"""
    def get(self, request, format=None):
            try:
                items = ShopItems.objects.filter(shopid=request.user)
                item_data = ShopItemDetailsSerializer(items, many=True)
                return Response(item_data.data)
            except:
                return Response({"status":status.HTTP_404_NOT_FOUND})

class GetItemsByShopId(APIView):
    """Fetch Shop items by shop id"""
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
        serializer = ShopItemDetailsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(shopid = request.user)
            return Response({
                "itemInfo": serializer.data,
                "status": status.HTTP_201_CREATED
            })
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UpdateItemByShop(APIView):
    """Update the item for a shop"""

    def put(self, request, id):
        try:
            item_instance = ShopItems.objects.get(id=id)
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})
        
        serializer = ShopItemUpdateSerializer(item_instance, \
                                              data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        conn = GetConnection()
        con, cur = conn.obtain_connection()
        cur.execute("select * from shopkeeperapp_shopitems where id = %s", (id,))
        if cur.rowcount == 1:
          cur.execute("delete from shopkeeperapp_shopitems where id = %s", (id,))
          con.commit()
          conn.close_connection(con, cur)
          return Response({"msg":"Deleted"}, status = status.HTTP_200_OK)
        else:
          conn.close_connection(con, cur)
          return Response({"msg":"Item not found"}, status = status.HTTP_404_NOT_FOUND)


class AddCategory(APIView):
    """Add new categories"""
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditCategory(APIView):
    """Edit categories"""
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request, cat, format=None):
      try:
        instance = Category.objects.get(cat_name=cat)
      except Category.DoesNotExist:
        return Response(state=status.HTTP_404_NOT_FOUND)

      serializer = CategorySerializer(instance, data = request.data, partial=True)
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


class GetTopDeals(APIView):
  """Get all top deals from the shops"""
  def get(self, request, format=None):
    conn = GetConnection()
    con, cur = conn.obtain_connection()

    cur.execute(""" select "shop_name", "shopid_id", "category_id" from shopkeeperapp_shopprofile """)
    deals = []
    for i in cur:
      shop_deals = {}
      con1, cur1 = conn.obtain_connection()
      cur1.execute(""" select "item_name", "list_price", "discount" from shopkeeperapp_shopitems \
                   where shopid_id=%s and discount!=%s order by discount desc """, (i['shopid_id'],\
                   0))
      if cur1.rowcount > 0:
        shop_deals['shop_id'] = i['shopid_id']
        shop_deals['shop_name'] = i['shop_name']
        itm = cur1.fetchone()
        shop_deals['item_name'] = itm['item_name']       
        shop_deals['list_price'] = itm['list_price']
        shop_deals['discount'] = itm['discount']
        image = Category.objects.get(cat_name = i['category_id'])
        shop_deals['img'] = image.img.url
        
        deals.append(shop_deals)
        
    return Response(deals, status = status.HTTP_200_OK)
