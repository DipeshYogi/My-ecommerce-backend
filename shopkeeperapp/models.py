from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return 'category/{filename}'.format(filename=filename)

class Category(models.Model):
    """Category model"""
    cat_name = models.CharField(max_length=50, primary_key=True)
    img = models.ImageField(_("Image"), upload_to=upload_to, default='default/category.jpg')
    desc = models.CharField(max_length=300, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.cat_name


class ShopProfile(models.Model):
    """Shopkeeper profile model"""
    id = models.AutoField(primary_key=True)
    shopid = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey("Category", to_field="cat_name", \
                                 on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    rating_choices = zip(range(1,6), range(1,6))
    ratings = models.IntegerField(choices = rating_choices, null=True)
    is_verified = models.BooleanField(default=False)
    free_delivery = models.BooleanField(default=False)   
    baggit_support = models.BooleanField(default=False)
    img = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shop Profiles'

    def __str__(self):
        return f"Shop profile for {self.shopid}"


class ShopItems(models.Model):
    shopid = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item_name = models.CharField(max_length=25)
    brand = models.CharField(max_length=20, blank=True)
    list_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    uom = models.CharField(max_length=25, verbose_name='Unit of Measure', \
                           null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    img = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shop Items'

    def __str__(self):
        return f"Shop item for {self.shopid}"