from django.shortcuts import render
from .models import User
import bcrypt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

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


