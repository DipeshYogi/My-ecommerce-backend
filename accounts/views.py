from django.shortcuts import render
from .serializers import RegisterUserSerializer, LoginUserSerializer, \
                         UserInfoSerializer, UpdateUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterUserView(APIView):
    """Register BoboApe users"""
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user":UserInfoSerializer(user).data,
                "token":AuthToken.objects.create(user)[1]
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """Login BoboApe users"""
    serializer_class = LoginUserSerializer

    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
             "user": UserInfoSerializer(user).data,
             "token": AuthToken.objects.create(user)[1] 
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    """Update User Information"""

    def put(self, request, id,  format=None):
        try:
            instance = get_user_model().objects.get(pk=id)
        except:
            return Response({"status":status.HTTP_404_NOT_FOUND})

        serializer = UpdateUserSerializer(instance, data=request.data,\
                                          partial=True)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"userdata": UserInfoSerializer(user).data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Extra responses
        userdata={}
        userdata['id'] = self.user.id
        userdata['name'] = self.user.name
        userdata['email'] = self.user.email
        userdata['phone'] = self.user.phone
        userdata['date_of_birth'] = self.user.date_of_birth

        data['userdata'] = userdata
        
        return data


class ModTokenObtainPairView(TokenObtainPairView):
    serializer_class = ModTokenObtainPairSerializer