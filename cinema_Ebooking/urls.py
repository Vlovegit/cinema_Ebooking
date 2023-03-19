from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
     path('', views.index, name="index"),
     path('login/',  views.login_user, name="login"),
     path('logout', views.logout, name="logout"),
     path('forgot-password/', views.forgot_password_view, name='forgot'),
     path('reset-password/', views.forgot_password_validation, name='rget'),
     path('password-reset-confirmation/', views.password_reset_confirmation, name='rget'),
     path('edit_profile', views.edit_profile, name='edit'),
     path('registration', views.registration, name="registration"),
     path('regisconfirmation/<uidb64>/<token>', views.regisconfirmation, name='regisconfirmation'),
     path('edit_card', views.edit_card, name='editcard'),
     path('edit_password', views.edit_password, name='editpassword'),
     path('checkout/', views.checkout, name='checkout'),
     path('seats/', views.seats, name='seats'),
     path('orderconfirmation/<order>/', views.orderconfirmation, name='orderconfirmation'),
     path('summary', views.summary, name='summary'),
     path('bookmovie/', views.book_movie, name='bookmovie'),
     path('base', views.base, name='base'),
     path('accountSuccess/',views.account_success, name='accountSuccess'),
     path('accountVerify/',views.account_verify, name='accountVerify')
]
