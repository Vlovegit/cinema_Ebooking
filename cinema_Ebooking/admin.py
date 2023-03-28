from django.contrib import admin
from . models import User,Card,Movie,MovieShowTime,MovieTime,ScheduleMovie,Promotion,ShowRoom
from django.contrib.auth.models import Group
from django.db.models.functions import Now
from .views import notifyPromo


# Register your models here.

admin.site.site_header = "Cinema E-Booking Admin"
admin.site.unregister(Group)
admin.site.site_url = ""


def Archive(modeladmin, request, queryset):
    for movie in queryset:
        queryset.update(archived=True)
    Archive.short_description = "Archive selected movies"


def Unarchive(modeladmin, request, queryset):
    for movie in queryset:
        queryset.update(archived=False)
    Unarchive.short_description = "Unarchive selected movies"


class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", 'last_name', 'email', 'is_promo', 'is_active', 'is_staff')
    list_filter = ('is_promo', 'is_staff')
    search_fields = ('first_name', 'email')


admin.site.register(User, UserAdmin)


def send_promo_mail(modeladmin, request, queryset):
    for promouser in queryset:
        queryset.update(user_notified=True)
        notifyPromo(request, promouser.id)
    send_promo_mail.short_description = "Send the selected promotions"


def auto_delete_promo_expired(modeladmin, request, queryset):
    Promotion._base_manager.filter(promo_validity__lte=Now()).delete()
    auto_delete_promo_expired.short_description = 'Delete Expired Promotions'


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'valid_upto', 'user_notified', 'discount')
    Promotion._base_manager.filter(valid_upto=Now()).delete()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['promo_code', 'valid_upto', 'discount']
        else:
            return []

    actions = [send_promo_mail, auto_delete_promo_expired]


admin.site.register(Promotion, PromotionAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'archived', 'category1', 'rating')
    ordering = ('archived',)
    actions = [Archive, Unarchive]
    list_filter = ('status', 'category1')
    search_fields = ('name', 'status', 'category1')


admin.site.register(Movie, MovieAdmin)


class ScheduleMovieAdmin(admin.ModelAdmin):
    model = ScheduleMovie
    ordering = ('showDate',)
    movie = Movie.objects.filter(archived=False)
    list_display = ('movie', 'showDate', 'MovieTime', 'theatre', 'booked_seats', 'seats_left')
    readonly_fields = ('booked_seats', 'seats_left')
    ScheduleMovie._base_manager.filter(showDate__lte=Now()).delete()

    def seats_left(self, obj):
        return obj.showroom.seatNum - obj.booked_seats  # numSeats


class ShowroomAdmin(admin.ModelAdmin):
    readonly_fields = ('seatNum',)  # numSeats
    list_display = ('theatre', 'seatNum')  # numseats


admin.site.register(ScheduleMovie, ScheduleMovieAdmin)
admin.site.register(ShowRoom, ShowroomAdmin)
admin.site.register(MovieShowTime)

#admin.site.register(Card)