from rest_framework import serializers
from authentication.models import User

#inheriting from serializers.ModelSerializer since our program contains models,
#this will enable django to predict some of our activities
class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(max_length=128,min_length=8,write_only=True)
    #enables us to add extra information to our serializer
    class Meta():
        model= User
        #enables us to define which data will be sent to the frontend
        fields= ('username','email','password',)
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password= serializers.CharField(max_length=128,min_length=8,write_only=True)

    class Meta():
        model= User
        fields= ('email','password','token',)
        read_only_fields=['token']