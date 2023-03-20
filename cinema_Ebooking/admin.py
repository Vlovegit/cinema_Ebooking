from django.contrib import admin
from . models import User
from . models import Card
from . models import Movie
from django.contrib.auth.models import Group


# Register your models here.

admin.site.site_header = "Cinema E-Booking Admin"
admin.site.unregister(Group)
admin.site.site_url = ""

admin.site.register(User)
admin.site.register(Movie)
#admin.site.register(Card)