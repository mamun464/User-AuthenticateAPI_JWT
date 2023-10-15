
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from  userApp.serializer import UserSerializer,UserRegistrationSerializer,UserLoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserView(APIView):
    def get(self, request):
        user=User.objects.all()
        user_serializer=UserSerializer(user, many=True)
        return Response(user_serializer.data)
    

class UserRegView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    
    def post(self, request):
        # IsAdminUser applited
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)

        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "user":{
                    'id': user.id,
                    'name': user.first_name+" "+user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'password': user.password,
                },
                "auth_token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                  
                  # Include the generated username
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SingleUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get(self, request,username):

        # IsAuthenticated applied
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

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
                # User is authenticated; generate JWT tokens
                 # User is authenticated; generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response({
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Login failed. Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)