from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import datetime


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for Registration of User"""
    class Meta:
        model = get_user_model()
        fields = ("email", "name", "phone", "password", "date_of_birth", \
                  "user_type")

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data["email"],
                                            validated_data["name"],
                                            validated_data["phone"],
                                            validated_data["password"],
                                            validated_data["date_of_birth"],
                                            validated_data["user_type"])
        
        return user


class LoginUserSerializer(serializers.Serializer):
    """Serializer for User Login"""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user 
        raise serializers.ValidationError("Incorrect Credentials")


class UpdateUserSerializer(serializers.Serializer):
    """Serializer to update User information"""
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=50, required=False)
    phone = serializers.CharField(max_length=12, required=False)
    date_of_birth = serializers.DateField(format="%d/%m/%Y", \
                                          input_formats=['%d/%m/%Y'],
                                          required=False) 

    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth == None:
            return None 
        else:
            date_of_birth = datetime.datetime.strftime\
                            (date_of_birth, '%Y-%m-%d')
            return date_of_birth


    def update(self, instance, validated_data):
        """update user information"""
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)
        instance.phone = validated_data.get("phone", instance.phone) 
        instance.date_of_birth = validated_data.get("date_of_birth", \
                                 instance.date_of_birth)
        
        instance.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer to return user information"""
    class Meta:
        model = get_user_model()
        fields = '__all__'


    