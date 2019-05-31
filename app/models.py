"""
Definition of models.
"""

from datetime import datetime
from django.db import models
import bcrypt
import re
from django.core.exceptions import ObjectDoesNotExist

class UserManager(models.Manager):
    def registration_validator(self, postData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        firstname = postData['p_fname']
        lastname = postData['p_lname']
        email = postData['p_email']
        password = postData['p_pword']
        confirm = postData['p_confirm']

        errors = {}
        if (len(firstname) < 1):
            errors["firstname"] = "You must enter a first name."
        if (len(lastname) < 1):
            errors["lastname"] = "You must enter a last name."
        if not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid e-mail address."
        if User.objects.filter(email=email):
            errors["email"] = "E-mail already exists."
        if not password == confirm:
            errors["confirm"] = "Passwords must match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        email = postData['login-email']
        password = postData['login-pw']
        if (len(email) < 1):
            errors["login"] = "Login does not exist."
            return errors
        if (len(password) < 1):
            errors["login"] = "Login does not exist."
            return errors

        try:
            this_user = User.objects.filter(email = postData["login-email"], password = postData["login-pw"])
            if this_user:
                if bcrypt.checkpw(password.encode(), this_user.password.encode()):
                    errors["password"] = "Password is not correct."
        except this_user.DoesNotExist:
            errors["login"] = "Login does not exist."
        return errors


class WishManager(models.Manager):
    def wish_validator(self, postData):

        title = postData['title'].strip()
        description = postData['description'].strip()

        errors = {}
        if (len(title) < 3):
            errors['title'] = 'You must enter a title.'
        if (len(description) < 3):
            errors['description'] = 'You must have a description, otherwise it is not going to happen'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

    def __str__(self):
        context = self.first_name + " " + self.last_name
        return context

class Wish(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    granted = models.BooleanField(default=False)
    date_granted = models.DateField(auto_now=True)
    likes = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

    def __str__(self):
        context = self.title
        return context
