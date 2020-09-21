from django.db import models
import re
import bcrypt
from datetime import date

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your First Name should be more than 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your Last Name should be more than 2 characters!"
        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Password and Password confirm must match!"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            log_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['password'] = "Invalid login attempt"
        else:
            errors['password'] = "Invalid login attempt"
        return errors
    
class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['wish_name']) == 0:
            errors['wish_name_empty'] = "A Wish name must be provided!"
        elif len(postData['wish_name']) < 3:
            errors['wish_name'] = "Your Wish should be at least 3 characters!"
        if len(postData['description']) == 0:
            errors['description_empty'] = "A description must be provided!"
        elif len(postData['description']) < 3:
            errors['description'] = "Your description should be at least 3 characters!"
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.TextField()
    # wishes - the list of wishes associated with this user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Wish(models.Model):
    
    def __str__(self):
        return f"<Wish object: Wish Name: {self.wish_name}\nWish Description {self.description}\nWish Granted: {self.granted}\nWish Created by: {self.user.first_name} {self.user.last_name}\nWish number of likes: {self.likes}\nWho Liked the wish {self.liked_by.all()} >"
    
    wish_name = models.CharField(max_length = 45)
    description = models.CharField(max_length = 255)
    granted = models.BooleanField(default = False)
    user = models.ForeignKey(User, related_name = "wishes",  on_delete=models.CASCADE)
    likes = models.IntegerField()
    liked_by = models.ManyToManyField(User)
    date_granted = models.DateTimeField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()