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

class Movie(models.Model):
    name = models.CharField(max_length=100,default='')
    category = models.CharField(max_length=25, choices=[('Action','Action'), ('Adventure','Adventure'), ('Animation','Animation'),('Biography','Biography'), ('Comedy','Comedy'), ('Crime','Crime'),('Documentary','Documentary'), ('Drama','Drama'), ('Family','Family'),('Fantasy','Fantasy'), ('Filmnoir','Film-Noir'), ('Gameshow','Game-show'),('History','History'), ('Horror','Horror'), ('Music','Music'),('Musical','Musical'), ('Mystery','Mystery'), ('News','News'),('Realitytv','Reality-TV'), ('Romance','Romance'), ('Scifi','Sci-Fi'),('Sport','Sport'), ('Talkshow','Talk-Show'), ('Thriller','Thriller'),('War','War'), ('Western','Western')])
    category2 = models.CharField(max_length=25,default = '', choices=[('Action','Action'), ('Adventure','Adventure'), ('Animation','Animation'),('Biography','Biography'), ('Comedy','Comedy'), ('Crime','Crime'),('Documentary','Documentary'), ('Drama','Drama'), ('Family','Family'),('Fantasy','Fantasy'), ('Filmnoir','Film-Noir'), ('Gameshow','Game-show'),('History','History'), ('Horror','Horror'), ('Music','Music'),('Musical','Musical'), ('Mystery','Mystery'), ('News','News'),('Realitytv','Reality-TV'), ('Romance','Romance'), ('Scifi','Sci-Fi'),('Sport','Sport'), ('Talkshow','Talk-Show'), ('Thriller','Thriller'),('War','War'), ('Western','Western')])
    category3 = models.CharField(max_length=25,default = '', choices=[('Action','Action'), ('Adventure','Adventure'), ('Animation','Animation'),('Biography','Biography'), ('Comedy','Comedy'), ('Crime','Crime'),('Documentary','Documentary'), ('Drama','Drama'), ('Family','Family'),('Fantasy','Fantasy'), ('Filmnoir','Film-Noir'), ('Gameshow','Game-show'),('History','History'), ('Horror','Horror'), ('Music','Music'),('Musical','Musical'), ('Mystery','Mystery'), ('News','News'),('Realitytv','Reality-TV'), ('Romance','Romance'), ('Scifi','Sci-Fi'),('Sport','Sport'), ('Talkshow','Talk-Show'), ('Thriller','Thriller'),('War','War'), ('Western','Western')])
    description = models.TextField(max_length=300,default='')
    review = models.URLField(max_length=200,default='') 
    rating = models.CharField(max_length=100, choices = [('G','G General Audiences'),('PG','PG Parental Guidance Suggested'),('PG-13', 'PG-13 Parents Strongly Cautioned'),('R','R Restricted'),('NC-17', 'NC-17 Adults Only')],default='')
    status = models.CharField(max_length=50,default='', choices=[('Now Playing','Now Playing'),('Upcoming','Upcoming')])
    cast = models.CharField(max_length=200,default='')
    director = models.CharField(max_length=100,default='')
    producer = models.CharField(max_length=100,default='')
    poster = models.ImageField(upload_to='images/',default='')
    trailer = models.URLField(max_length=200,default='')
    releasedate = models.DateField(default=False,null=True,blank=True)
    archived = models.BooleanField(default=False,null=True,blank=True,help_text='If value is yes then it wont be visible on the booking portal')
    year = models.CharField(max_length=5,default = '')
    imdb = models.CharField(max_length=6,default='')
    def __str__(self):
        return self.name
