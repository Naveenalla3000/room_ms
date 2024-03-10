from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)
    class Meta:
        model = User
        fields = ['email',
                  'name',
                  'password',
                  'password2',
                  'tc']
        extra_kwargs = {
            'password': {
                'write_only': True
                }
            }
        
    # validate password and password2 match while registering
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password should match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'tc']
        
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,
                                     style={
                                         'input_type': 'password'
                                        },write_only=True)
    password2 = serializers.CharField(max_length=255,
                                      style={
                                          'input_type': 'password'
                                        },write_only=True)
    class Meta:
        model = User
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password should match")
        user.set_password(password)
        user.save()
        return attrs
    
    
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/'+uidb64+'/'+token
            body = 'Hi, \n\n Please click on the link to reset your password \n\n' + link
            body = {
                'email_body': body,
                'email_subject':'Reset your password',
                'to_email':user.email,
            }
            Util.send_email(body)
            return attrs
        else:
            raise serializers.ValidationError("User with this email does not exist")
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,
                                     style={
                                         'input_type': 'password'
                                        },write_only=True)
    password2 = serializers.CharField(max_length=255,
                                      style={
                                          'input_type': 'password'
                                        },write_only=True)
    class Meta:
        model = User
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uidb64 = self.context.get('uidb64')
            token = self.context.get('token')
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid, please request a new one")
            if password != password2:
                raise serializers.ValidationError("password and confirm password should match")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError("Token is not valid, please request a new one")