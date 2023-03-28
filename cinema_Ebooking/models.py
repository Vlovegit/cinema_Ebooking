from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.db.models.functions import Now


# Create your models here.
class User(AbstractUser):
    phone = models.TextField(blank=True, null=True)
    is_promo = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    apartNumber = models.TextField(blank=True, null=True)
    # city = models.TextField(blank = True, null = True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Card(models.Model):
    cardHolderName = models.CharField(max_length=1000, blank=True, null=True)
    cardNum = models.CharField(max_length=1000, blank=True, null=True)
    expiryDate = models.TextField(blank=True, null=True)
    last_four = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Movie(models.Model):
    name = models.CharField(max_length=100, default='')
    category1 = models.CharField(max_length=25,
                                choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
                                         ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                         ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                         ('Fantasy', 'Fantasy'), ('Filmnoir', 'Film-Noir'), ('Gameshow', 'Game-show'),
                                         ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'),
                                         ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('News', 'News'),
                                         ('Realitytv', 'Reality-TV'), ('Romance', 'Romance'), ('Scifi', 'Sci-Fi'),
                                         ('Sport', 'Sport'), ('Talkshow', 'Talk-Show'), ('Thriller', 'Thriller'),
                                         ('War', 'War'), ('Western', 'Western')])
    category2 = models.CharField(max_length=25, default='',
                                 choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
                                          ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                          ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                          ('Fantasy', 'Fantasy'), ('Filmnoir', 'Film-Noir'), ('Gameshow', 'Game-show'),
                                          ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'),
                                          ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('News', 'News'),
                                          ('Realitytv', 'Reality-TV'), ('Romance', 'Romance'), ('Scifi', 'Sci-Fi'),
                                          ('Sport', 'Sport'), ('Talkshow', 'Talk-Show'), ('Thriller', 'Thriller'),
                                          ('War', 'War'), ('Western', 'Western')])
    category3 = models.CharField(max_length=25, default='',
                                 choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'),
                                          ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'),
                                          ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Family', 'Family'),
                                          ('Fantasy', 'Fantasy'), ('Filmnoir', 'Film-Noir'), ('Gameshow', 'Game-show'),
                                          ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'),
                                          ('Musical', 'Musical'), ('Mystery', 'Mystery'), ('News', 'News'),
                                          ('Realitytv', 'Reality-TV'), ('Romance', 'Romance'), ('Scifi', 'Sci-Fi'),
                                          ('Sport', 'Sport'), ('Talkshow', 'Talk-Show'), ('Thriller', 'Thriller'),
                                          ('War', 'War'), ('Western', 'Western')])
    sypnopsis = models.TextField(max_length=1000, default='')
    review = models.URLField(max_length=200, default='')
    rating = models.CharField(max_length=100,
                              choices=[('G', 'G General Audiences'), ('PG', 'PG Parental Guidance Suggested'),
                                       ('PG-13', 'PG-13 Parents Strongly Cautioned'), ('R', 'R Restricted'),
                                       ('NC-17', 'NC-17 Adults Only')], default='')
    status = models.CharField(max_length=50, default='',
                              choices=[('Now Playing', 'Now Playing'), ('Coming Soon', 'Coming Soon')])
    director = models.CharField(max_length=100, default='')
    cast = models.CharField(max_length=400, default='')
    producer = models.CharField(max_length=100, default='')
    poster = models.URLField(max_length=300, default='')
    trailer = models.URLField(max_length=200, default='')
    releasedate = models.DateField(default=False, null=True, blank=True)
    archived = models.BooleanField(default=False, null=True, blank=True)
    year = models.CharField(max_length=5, default='')
    imdb = models.CharField(max_length=6, default='')

    def __str__(self):
        return self.name

class MovieTime(models.Model):
    showDateTime = models.DateField()
    def __str__(self):
        return str(self.showDateTime)
    
class ShowRoom(models.Model):
    theatre = models.CharField(max_length=50,unique=True)
    seatNum = models.IntegerField(default=50)
    def __str__(self):
        return self.showroom

class MovieShowTime(models.Model):
    showTimes = models.TimeField()
    def __str__(self):
        return str(self.showTimes)
        
class Scheduler(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(PlayingOn__gte=Now())

class ScheduleMovie(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    showDate = models.DateField(db_index=True)
    MovieTime = models.TextField(max_length=10,choices=[('10:00AM','10:00AM'),('13:00PM','13:00PM'),('16:00PM','16:00PM'),('19:00PM','19:00PM'),('22:00PM','22:00PM')])
    theatre = models.ForeignKey(ShowRoom,on_delete=models.CASCADE)
    child_cost=models.FloatField(default=5.99)
    adult_cost=models.FloatField(default=9.99)
    senior_cost=models.FloatField(default=6.99)
    booked_seats=models.IntegerField(default=0, validators=[MaxValueValidator(50), MinValueValidator(0)])
    def remaining_seats(self):
        return self.showroom.seatNum - self.booked_seats #numSeats
    objects = Scheduler()
    class Meta:
        unique_together = ('theatre','showDate', 'MovieTime')
    def __str__(self):
        return self.movie.name

class Promotion(models.Model):
    discount = models.IntegerField()
    user_notified = models.BooleanField(default=False, editable=False)
    promo_code = models.CharField(max_length=10, unique=True)
    valid_upto = models.DateField()
    def __str__(self):
        return self.promo_code
    def get_discount(self):
        return (1-(self.discount/100))

class Seat(models.Model):
    seat_status = (["seat","seat"],["seat selected","seat selected"],["seat occupied","seat occupied"])
    seat_01 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_02 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_03 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_04 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_05 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_06 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_07 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_08 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_09 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_10 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_11 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_12 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_13 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_14 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_15 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_16 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_17 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_18 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_19 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_20 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_21 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_22 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_23 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_24 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_25 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_26 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_27 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_28 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_29 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_30 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_31 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_32 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_33 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_34 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_35 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_36 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_37 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_38 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_39 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_40 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_41 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_42 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_43 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_44 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_45 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_46 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_47 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_48 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_49 = models.CharField(default="seat",max_length=15,choices=seat_status)
    seat_50 = models.CharField(default="seat",max_length=15,choices=seat_status)

    show = models.OneToOneField(ScheduleMovie, on_delete=models.CASCADE)

    def __str__(self):
        return f'%s on %s at %s' % (self.show.movie.title,self.show.showDate,self.show.MovieTime)
