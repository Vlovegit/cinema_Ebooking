from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
    phone = models.TextField(blank = True, null = True)
    is_promo = models.BooleanField(default=False)
    address = models.TextField(blank= True, null = True)
    apartNumber = models.TextField(blank = True, null = True)
    #city = models.TextField(blank = True, null = True)
    state = models.TextField(blank = True, null = True)
    country = models.TextField(blank = True, null = True)
    zip = models.TextField(blank = True, null = True)
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
class Card(models.Model):
    #cardname = models.CharField(max_length= 100,blank= True, null = True)
    ccnum = models.CharField(max_length=150, blank = True, null = True)
    valid = models.TextField(blank=True, null= True)
    last_four = models.CharField(max_length = 4,blank =True, null = True)
    cvc = models.TextField(blank =True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

