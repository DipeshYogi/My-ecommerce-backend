from django.shortcuts import render
from .serializers import AddressSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Addresses
from  db_utils.connect import GetConnection


class GetUserAddress(APIView):
  """Get user addresses"""
  permission_classes = [permissions.IsAuthenticated,]

  def get(self, request, id, format=None):
    """get user addresses"""
    try:
        addresses = Addresses.objects.filter(userid = id)
        serializer = AddressSerializer(addresses, many = True)
        return Response(serializer.data)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
            

class AddUserAddress(APIView):
  """Add user addresses"""
  permission_classes = [ permissions.IsAuthenticated, ]

  def post(self, request, format=None):
    serializer = AddressSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save(userid=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserAddress(APIView):
  """Edit user address""" 
  def put(self, request, id, format=None):
    try:
      instance = Addresses.objects.get(pk=id)
    except Addresses.DoesNotExist:
      return Response({'msg':'No address found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AddressSerializer(instance, data = request.data, partial=True)
    if serializer.is_valid():
      addr = serializer.save()
      return Response({'addr': AddressSerializer(addr).data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAddress(APIView):
  """Delete user addresses"""
  permission_classes = [ permissions.IsAuthenticated, ]

  def post(self, request, format=None):
    serializer = AddressSerializer(data = request.data)
    if serializer.is_valid():
      userid = request.user.id
      # print("#########################")
      # print(userid.id)
      addr1 = serializer.data['address1']
      addr2 = serializer.data['address2']
      pincode = serializer.data['pincode']
      phone = serializer.data['phone']
      try:
        address = Addresses.objects.get(
                                          userid=userid,
                                          address1 = addr1,
                                          address2 = addr2,
                                          pincode = pincode,
                                          phone = phone )
        conn = GetConnection()
        con, cur = conn.obtain_connection()
        cur.execute('delete from customerapp_addresses where userid_id = %s \
                     and address1 = %s and address2 = %s and pincode = %s \
                     and phone = %s', (userid, addr1, addr2, pincode, phone))
        con.commit()
        # con.close()
        # cur.close()
        conn.close_connection(con, cur)
        return Response({'msg':'DELETED'}, status = status.HTTP_200_OK)
        
      except Addresses.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    else:
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UpdateActiveAddress(APIView):
      """Update active address of a user"""
      permission_classes = [ permissions.IsAuthenticated, ]
      
      def put(self, request, addrId, format=None):
            userid = request.user.id
            conn = GetConnection()
            con, cur = conn.obtain_connection()
            cur.execute('select * from customerapp_addresses where userid_id =\
                         %s',(userid,))
            addresses = cur.fetchall()
            for add in addresses:
              if add['is_active'] == True:
                cur.execute('update customerapp_addresses set is_active = %s \
                             where id = %s', (False, add['id']))
            cur.execute('update customerapp_addresses set is_active = %s where \
                         id = %s', (True, addrId))
            
            con.commit()
            conn.close_connection(con, cur)

            return Response({'msg':'Active address updated'}, status=status.HTTP_200_OK)


