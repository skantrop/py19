from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email

    def validate(self, attrs: dict):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    
    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_email()


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exists')
        return email
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user =  User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs







