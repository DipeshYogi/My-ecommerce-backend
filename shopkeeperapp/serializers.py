from rest_framework import serializers
from .models import ShopProfile, ShopItems, Category


class ShopProfileSerializer(serializers.ModelSerializer):
    """Serializer for Shop Profile"""
    class Meta:
        model = ShopProfile
        fields = '__all__'
    
    def create(self, validated_data):
        """Create a new Shop Profile"""
        return ShopProfile.objects.create(**validated_data)


class ShopProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Shop Profile"""
    class Meta:
        model = ShopProfile
        exclude = ['shopid']

    def update(self, instance, validated_data):
        """Update the existing Shop profile"""
        instance.category = validated_data.get('category', instance.category)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longtude = validated_data.get('longitude', instance.longitude)
        instance.ratings = validated_data.get('ratings', instance.ratings)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.free_delivery = validated_data.get('free_delivery', instance.free_delivery)
        instance.baggit_support = validated_data.get('baggit_support', instance.baggit_support)
        instance.img = validated_data.get('img', instance.img)
        instance.save()
        return instance


class ShopItemSerializer(serializers.Serializer):
    """Serializer for Shop Items"""
    shopid = serializers.IntegerField()


class ShopItemDetailsSerializer(serializers.ModelSerializer):
    """Serializer for adding Shop Items"""
    class Meta:
        model = ShopItems
        fields = '__all__'

    def create(self, validated_data):
        """add shop items"""
        return ShopItems.objects.create(**validated_data)


class ShopItemUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing items"""
    class Meta:
        model = ShopItems
        exclude = ["shopid", "id"]

    def update(self, instance, validated_data):
        """update an existing item"""
        instance.item_name = validated_data.get('item_name', instance.item_name)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.list_price = validated_data.get('list_price', instance.list_price)
        instance.uom = validated_data.get('uom', instance.uom)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.img = validated_data.get('img', instance.img)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    """Serializr for categories"""
    class Meta:
        model = Category
        fields = '__all__'


class GetCategorySerializer(serializers.ModelSerializer):
    """Serializr for categories"""
    img_url = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('cat_name', 'img', 'img_url')

    def get_img_url(self, cat):
        request = self.context.get('request')
        img_url = cat.img.url
        return request.build_absolute_uri(img_url)

class GetShopByCatSerializer(serializers.Serializer):
    cat_name = serializers.CharField(max_length=25)



    