
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from  userApp.serializer import UserSerializer,UserRegistrationSerializer,UserLoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate

class UserView(APIView):
    def get(self, request):
        user=User.objects.all()
        user_serializer=UserSerializer(user, many=True)
        return Response(user_serializer.data)
    

class UserRegView(APIView):
    def post(self, request):
        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            response_data = {
                'id': user.id,
                'name': user.first_name+" "+user.last_name,
                
                'email': user.email,
                'username': user.username,  # Include the generated username
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SingleUserView(APIView):
    def get(self, request,username):
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
        
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)
    
class UserLoginView(APIView):
    def post(self, request):
        login_serializer = UserLoginSerializer(data=request.data)
        if login_serializer.is_valid():
            username = login_serializer.validated_data['username']
            password = login_serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # User is authenticated; you can perform additional actions here if needed.
                return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Login failed. Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)