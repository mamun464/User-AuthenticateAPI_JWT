

from django.contrib import admin
from django.urls import path
from userApp import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user',views.UserView.as_view(), name="user-view"),
    path('signup',views.UserRegView.as_view(), name="user-signup"),
    path('user/<str:username>', views.SingleUserView.as_view(), name="user-search"),
    path('login', views.UserLoginView.as_view(), name="user-login"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/',TokenVerifyView.as_view(), name="token-verify"),
]
