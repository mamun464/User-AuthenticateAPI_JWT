from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'



def generateUserName (first_name,last_name,validated_data):
    baseUserName=f"{first_name.lower()}.{last_name.lower()}"
        # Check if a user with the same user_name already exists
    user_name = baseUserName
    count = 1
    
    while User.objects.filter(username=user_name).exists():
        user_name = f"{baseUserName}{count}"
        count += 1
        print(f"Inside: {user_name}")

         # Add the generated user_name to the validated data
    print(f"Outside: {user_name}")
    return user_name



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=['id', 'first_name', 'last_name', 'username' ,'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
              'style': {'input_type': 'password'}
            } 
            }


    def create(self,validated_data):

        validated_data['first_name'] = (validated_data['first_name']).title()
        validated_data['last_name'] = (validated_data['last_name']).title()

        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user_name=generateUserName(first_name, last_name,validated_data)
        validated_data['username'] = user_name

        
        is_active=True
        is_staff=False
        # validated_data['is_active'] = is_active
        # validated_data['is_staff'] = is_staff


        baseEmail=f"{first_name.title()}.{last_name.title()}@gmail.com"
        # Check if a user with the same Email already exists
        email = baseEmail
        count = 1
        while User.objects.filter(email=email).exists():
            split_email=baseEmail.split("@")[0]
            email = f"{split_email}{count}@gmail.com"
            count += 1

        validated_data['email'] = email

        # Create and return the Student object with the updated user_name
        user= User.objects.create(**validated_data)
        
        return user
    



class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # username = serializers.CharField()
    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # User is authenticated; you can perform additional actions here if needed.
            return user
        else:
            return None

        

