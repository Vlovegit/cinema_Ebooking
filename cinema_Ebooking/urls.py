from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
#  path('admin/', admin.site.urls),
#     #path('', include('home.urls')),
     path('', views.index, name="index"),
     path('login/',  views.login_user, name="login"),
     path('logout', views.logout, name="logout"),
     path('forgot-password/', views.forgot_password_view, name='forgot'),
     path('reset-password/', views.forgot_password_validation, name='rget'),
     path('password-reset-confirmation/', views.password_reset_confirmation, name='rget'),
#     path('admin', views.admin, name='admin'),
     path('edit_profile', views.edit_profile, name='edit'),
     path('registration', views.registration, name="registration"),
     path('regisconfirmation/<uidb64>/<token>', views.regisconfirmation, name='regisconfirmation'),
     path('edit_card', views.edit_card, name='editcard'),
#     path('changepassword', PasswordChangeView.as_view(
#             template_name='change_password.html',success_url="login"),
#         name='changepassword'),
#     path('orderSummary', views.orderSummary, name="orderSummary"),
#     path('orderHistory', views.orderHistory, name="orderHistory"),
#     path('addpromotion', views.addpromotion, name='addpromotion'),
#     path('addmovie', views.addmovie, name='addmovie'),
     path('checkout/', views.checkout, name='checkout'),
#     path('moviedetails', views.moviedetails, name='moviedetails'),
     path('seats/', views.seats, name='seats'),
#     path('fullcalendar', views.fullcalendar, name='fullcalendar'),
     path('orderconfirmation/<order>/', views.orderconfirmation, name='orderconfirmation'),
     path('summary', views.summary, name='summary'),
    # path('searchResults', views.searchResults, name='searchResults'),
    # path('categories', views.categories, name='categories'),
    # path('schedule', views.schedule, name='schedule'),
#     #path('schedulemovie', views.schedulemovie, name='schedulemovie'),
     path('bookmovie/', views.book_movie, name='bookmovie'),
     path('base', views.base, name='base'),
     path('accountSuccess/',views.account_success, name='accountSuccess'),
     path('accountVerify/',views.account_verify, name='accountVerify')
#     path('manage', views.manage, name='manage'),
#     path('managemovie', views.managemovie, name='managemovie')
]
