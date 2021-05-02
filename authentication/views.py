from django.shortcuts import render
from .models import User
from rest_framework import exceptions
import bcrypt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import permissions
from .utils import generate_access_token,generate_refresh_token

class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self,request,format=None):
        data = self.request.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        confirm_pw = data['confirm_pw']

        ## Alternate way is just send ##
        ## User.objects.register_validation(data) ##
        ## If that then change register_validation too inside the model ##
        errors = User.objects.register_validation(first_name,last_name,email,password,confirm_pw)
        if len(errors)>0:
            return Response({"errors":errors})
        else:
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name=first_name,
                last_name=first_name,
                email=email,
                password=hash_pw
            )
            return Response({'success':'User created successfully'},status=201)

@method_decorator(ensure_csrf_cookie,name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self,request,format=None): 
        data = self.request.data
        email = data['email']
        response = Response()
        password = data['password']
        user = User.objects.filter(email = email)
       
        if user:
            logged_user = user[0]
            serialized_user = UserSerializer(logged_user).data
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                access_token = generate_access_token(logged_user)
                refresh_token = generate_refresh_token(logged_user)
                response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
                response.data = {
                    'access_token': access_token,
                    'user': serialized_user
                }
                return response
        return Response({'error':'Email or password are incorrect'})

        
 