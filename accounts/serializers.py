from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile


class ProfileSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Profile
        fields = ['phone', 'birth_date', 'address', 'bio', 'avatar', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer ( serializers.ModelSerializer ) :
    profile = ProfileSerializer ( read_only=True )

    class Meta :
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer ( serializers.ModelSerializer ) :
    password = serializers.CharField ( write_only=True, required=True, validators=[validate_password] )
    password2 = serializers.CharField ( write_only=True, required=True )

    class Meta :
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
            'email' : {'required' : True}
        }

    def validate(self, attrs) :
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError ( {"password" : "Password fields didn't match."} )
        return attrs

    def create(self, validated_data) :
        validated_data.pop ( 'password2' )
        user = User.objects.create_user ( **validated_data )
        return user


class ChangePasswordSerializer ( serializers.Serializer ) :
    old_password = serializers.CharField ( required=True )
    new_password = serializers.CharField ( required=True, validators=[validate_password] )
    new_password2 = serializers.CharField ( required=True )

    def validate(self, attrs) :
        if attrs['new_password'] != attrs['new_password2'] :
            raise serializers.ValidationError ( {"new_password" : "Password fields didn't match."} )
        return attrs


class UpdateProfileSerializer ( serializers.ModelSerializer ) :
    username = serializers.CharField ( source='user.username', read_only=True )
    email = serializers.EmailField ( source='user.email', required=False )
    first_name = serializers.CharField ( source='user.first_name', required=False )
    last_name = serializers.CharField ( source='user.last_name', required=False )

    class Meta :
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name',
                  'phone', 'birth_date', 'address', 'bio', 'avatar']

    def update(self, instance, validated_data) :
        user_data = validated_data.pop ( 'user', {} )

        user = instance.user
        user.email = user_data.get ( 'email', user.email )
        user.first_name = user_data.get ( 'first_name', user.first_name )
        user.last_name = user_data.get ( 'last_name', user.last_name )
        user.save ()

        instance.phone = validated_data.get ( 'phone', instance.phone )
        instance.birth_date = validated_data.get ( 'birth_date', instance.birth_date )
        instance.address = validated_data.get ( 'address', instance.address )
        instance.bio = validated_data.get ( 'bio', instance.bio )
        if 'avatar' in validated_data :
            instance.avatar = validated_data.get ( 'avatar' )
        instance.save ()

        return instance