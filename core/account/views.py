from django.shortcuts import render,redirect
# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer, UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        # print(request.data)
        serializer = UserRegistrationSerializer(data=request.data) # serializer is a class
        #  if serializer.is_valid(raise_exception=True):
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        # print(user) user@gmail.com
        redirect('http://localhost:8000/login')
        response =  Response(
            {
                'token': token,
                'msg': 'Registration success',
            },
            status=status.HTTP_201_CREATED)
        return render(request, 'login.html', {'response':response})
    
        # print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        def get(self, request, format=None):
            return render(request, 'register.html')
    

class UserLoginView(APIView):
    print("called....")
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        # print(request.data)
        serializer = UserLoginSerializer(data=request.data) # serializer is a class
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        # print(email, password)
        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user is not None:
            token = get_tokens_for_user(authenticated_user)
            response = Response(
                {
                    'token':token,
                    'msg': 'Login success',
                },
                status=status.HTTP_200_OK)
            # response.set_cookie('access_token', token['access'], httponly=True,secure=True)
            # response.set_cookie('refresh_token', token['refresh'], httponly=True,secure=True)
            return render(request, 'designs.html', {'response':response})
        else:
            return Response(
                {
                    'errors': {
                            'non_field_errors':['Email or password is invalid']
                        },
                },
                status=status.HTTP_404_NOT_FOUND)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # print(request.user) 
        # make sure that you are including barer token in request
        serializer = UserProfileSerializer(request.user)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserChagePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, formate=None):
        serializer = UserChangePasswordSerializer(
                                                data=request.data,
                                                context={
                                                    'user':request.user
                                                    }
                                                )
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        # print(request.data)
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'msg':'Password Reset link send. Please check your Email'},
            status=status.HTTP_200_OK,
        )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uidb64, token, format=None):
        # print(token,uidb64)
        serializer = UserPasswordResetSerializer(data=request.data, context={
            'uidb64':uidb64,
            'token':token,
        })
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def logout(request):
    return render(request, 'login.html')
    
