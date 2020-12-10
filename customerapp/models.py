from django.db import models
from django.contrib.auth import get_user_model


class Addresses(models.Model):
    userid = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=8)
    phone = models.CharField(max_length=12)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.address1
