from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .factories.addresses import UserFactory, AddressFactory
from customerapp.models import Addresses


class TestUserAddresses(TestCase):
  """ 
    test creating, retreiving, deleting and updating
    user addresses.
  """

  def setUp(self):
    self.client = APIClient()
    # data setup with factory_boy
    self.user = UserFactory()
    self.addr = AddressFactory(userid = self.user)

    # obtain JWT token for the user
    self.userdata = {
      "email": self.user.email,
      "password": "test@123"
    }
    response = self.client.post(reverse('token_obtain_pair'), self.userdata, \
                                  format='json')
    self.token = response.data['access']
       
  def test_adding_addresses(self):
    addr_data = {
      "address1": "test address",
      "address2": "test address2",
      "pincode": "98712",
      "phone": "9872712122"
    }
    inv_addr_data = {
      "address1": "test address",
      "address2": "test address2",
      "pincode": "98712",
    }

    # test without token data
    response = self.client.post(reverse('add_address'), addr_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, \
                     "failed with invalid token")
    
    # test with valid token but invalid data
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token}")
    response = self.client.post(reverse('add_address'), inv_addr_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, \
                     "failed with invalid data")  
 
    # test with valid token but invalid data
    response = self.client.post(reverse('add_address'), addr_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED, \
                     "failed with valid data") 

    # assert if the response is valid
    self.assertEqual(addr_data['address1'], response.data['address1'], 'inv addr1')
    self.assertEqual(addr_data['address2'], response.data['address2'], 'inv addr2')
    self.assertEqual(addr_data['pincode'], response.data['pincode'], 'inv pincode')
    self.assertEqual(addr_data['phone'], response.data['phone'], 'inv phone')

  def test_retreiving_addresses(self):
    # obtain token for new user
    userdata1 = {"email":self.user.email, "password":"test@123"}
    response = self.client.post(reverse('token_obtain_pair'), userdata1)
    token = response.data['access']
    
    # retreive the added address with no authentication
    response = self.client.get(reverse('get_address', kwargs={'id':self.addr.id}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, \
                     'Failed retreiving addresss with no auth')

    # retreive the added address with valid authentication but invalid user id
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {token}")
    response = self.client.get(reverse('get_address', kwargs={'id':100}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, \
                    'Failed retreiving addresss with invalid addr id')

    # retreive the added address with valid authentication and user id
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {token}")
    response = self.client.get(reverse('get_address', kwargs={'id':self.user.id}))
    self.assertEqual(response.status_code, status.HTTP_200_OK, \
                    'Failed retreiving addresss with invalid addr id')
    
    # assert if reponse values are correct
    self.assertEqual(self.addr.address1, response.data[0]['address1'], 'inv addr1')
    self.assertEqual(self.addr.address2, response.data[0]['address2'], 'inv addr2')
    self.assertEqual(self.addr.pincode, response.data[0]['pincode'], 'inv pincode')
    self.assertEqual(self.addr.phone, response.data[0]['phone'], 'inv phone')

  def test_updating_address(self):
    response = self.client.post(reverse('token_obtain_pair'), \
              {'email':self.user.email, 'password':'test@123'})
    token = response.data['access']

    addr_data = {
      'address2': 'updated addr'
    }

    # update address without token
    response = self.client.put(reverse('update_address', kwargs={'id':self.addr.id}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # update address with token but invalid data
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {token}")
    response = self.client.put(reverse('update_address', kwargs={'id':100}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # update address with token and valid data
    response = self.client.put(reverse('update_address', kwargs={'id':self.addr.id}), \
                               addr_data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # assert is data updated correctly
    self.assertEqual(addr_data['address2'], response.data['addr']['address2'])
  
  def test_deleting_address(self):
    response = self.client.post(reverse('token_obtain_pair'), \
              {'email':self.user.email, 'password':'test@123'})
    token = response.data['access']

    # delete address without token
    response = self.client.post(reverse('delete_address', kwargs={'addrId':self.addr.id}))
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # update address with token but invalid data
    self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {token}")
    response = self.client.post(reverse('delete_address', kwargs={'addrId':100}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # update address with token but valid data
    response = self.client.post(reverse('delete_address', kwargs={'addrId':self.addr.id}))
    self.assertEqual(response.status_code, status.HTTP_200_OK)