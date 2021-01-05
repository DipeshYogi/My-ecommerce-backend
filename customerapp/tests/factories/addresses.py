import factory
from customerapp.models import Addresses
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = get_user_model()
  
  email = "test1@gmail.com"
  password = factory.PostGenerationMethodCall('set_password', 'test@123')
  name = "test1"
  phone = "9786273621"
  date_of_birth = "1994-10-11"
  user_type = "CUSTOMER"


class AddressFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Addresses
  
  userid = factory.SubFactory(UserFactory)
  address1 = "Test addr1"
  address2 ="Test addr2"
  pincode = "111222"
  phone = "9888888888"
