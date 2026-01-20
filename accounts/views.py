from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
    ProfileSerializer
)
from .models import Profile


class RegisterView ( generics.CreateAPIView ) :
    queryset = User.objects.all ()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema (
        operation_description="Yangi user yaratish (Register)",
        responses={201 : UserSerializer ()}
    )
    def post(self, request, *args, **kwargs) :
        serializer = self.get_serializer ( data=request.data )
        serializer.is_valid ( raise_exception=True )
        user = serializer.save ()

        refresh = RefreshToken.for_user ( user )

        return Response ( {
            'user' : UserSerializer ( user ).data,
            'tokens' : {
                'refresh' : str ( refresh ),
                'access' : str ( refresh.access_token ),
            },
            'message' : 'User successfully registered!'
        }, status=status.HTTP_201_CREATED )


class ProfileView ( generics.RetrieveUpdateAPIView ) :
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) :
        return self.request.user.profile

    @swagger_auto_schema (
        operation_description="O'z profil ma'lumotlarini ko'rish",
        responses={200 : UpdateProfileSerializer ()}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Profil ma'lumotlarini yangilash",
        responses={200 : UpdateProfileSerializer ()}
    )
    def put(self, request, *args, **kwargs) :
        return super ().put ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Profil ma'lumotlarini qisman yangilash",
        responses={200 : UpdateProfileSerializer ()}
    )
    def patch(self, request, *args, **kwargs) :
        return super ().patch ( request, *args, **kwargs )


class ChangePasswordView ( APIView ) :
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema (
        operation_description="Parolni o'zgartirish",
        request_body=ChangePasswordSerializer,
        responses={
            200 : openapi.Response ( 'Password changed successfully' ),
            400 : 'Bad Request'
        }
    )
    def post(self, request) :
        serializer = ChangePasswordSerializer ( data=request.data )

        if serializer.is_valid () :
            user = request.user

            if not user.check_password ( serializer.validated_data['old_password'] ) :
                return Response (
                    {'old_password' : 'Wrong password.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password ( serializer.validated_data['new_password'] )
            user.save ()

            return Response (
                {'message' : 'Password changed successfully!'},
                status=status.HTTP_200_OK
            )

        return Response ( serializer.errors, status=status.HTTP_400_BAD_REQUEST )


class LogoutView ( APIView ) :
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema (
        operation_description="User logout qilish",
        request_body=openapi.Schema (
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh' : openapi.Schema ( type=openapi.TYPE_STRING, description='Refresh token' )
            }
        ),
        responses={
            205 : 'Logout successful',
            400 : 'Bad Request'
        }
    )
    def post(self, request) :
        try :
            refresh_token = request.data["refresh"]
            token = RefreshToken ( refresh_token )
            token.blacklist ()
            return Response (
                {'message' : 'Logout successful!'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e :
            return Response (
                {'error' : str ( e )},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailView ( generics.RetrieveAPIView ) :
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) :
        return self.request.user

    @swagger_auto_schema (
        operation_description="O'zingiz haqingizda to'liq ma'lumot",
        responses={200 : UserSerializer ()}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )