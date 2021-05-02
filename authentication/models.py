from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validation(self,first_name,last_name,email,password,confirm_pw):
        errors = {}
        if len(first_name) <2:
            errors['short_firstname'] = "First name must be atleast 2 characters"
        if len(last_name) <2:
            errors['short_lastname'] = "Last name must be atleast 2 characters"
        if not email:
            errors['empty_email'] = "User has to provide an email"
        if not EMAIL_REGEX.match(email):   
            errors['invalid_email'] = "Invalid Email address"
        users_with_email = User.objects.filter(email = email)
        if len(users_with_email) >= 1:
             errors['duplicate_email'] = "Email already exists"
        if len(password) < 5:
            errors['short_password'] = "Password must be atleast 5 characters"
        if password != confirm_pw:
            errors['password_match'] = "Password must match"
        
        return errors

class User(models.Model):
    """ Database model for User"""
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    alias = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()