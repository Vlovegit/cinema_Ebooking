import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .forms import UserRegistrationForm
from .models import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from .settings import EMAIL_HOST, EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q


# Create your views here.

# def home(request):
#     return render(request, 'home.html')

# def adminpage(request):
#     return render(request, 'admin.html')

# def userprofile(request):
#     return render(request,'userprofile.html')

# def logout(request):
#     return render(request, logout.html)

def login_user(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        print(email)
        print(password)
        remember = request.POST.get('rememberme')

        # print(email)
        # print(password)

        mydata = User.objects.filter(email=email).values()
        print(mydata.exists())
        try:
            mydata1 = User.objects.get(email=email)  # get
        except:
            mydata1 = None
        print(type(mydata1))

        user = auth.authenticate(email=email, password=password)

        # print(user)

        if user is not None:
            if user.is_active:
                print('user active')
                auth.login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                if user.is_superuser:
                    return redirect("/admin")  # success
                else:
                    return redirect(index)
            # else:
            #     print('user inactive')
            #     messages.info(request,'Account Not verified', extra_tags='verify')

        else:
            print('user not in db')
            if mydata.exists():
                if mydata[0]['is_active'] == False:

                    messages.info(request, 'Account not verified', extra_tags='verify')
                    activateEmail(request, mydata1, email)  # email confirmation #resend
                    return redirect('accountNotVerified')
                else:
                    messages.info(request, 'invalid credentials', extra_tags='invalid')
                    return redirect('login')
            else:
                messages.info(request, 'account does not exist', extra_tags='exist')
                return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect(index)


def registration(request):
    if request.method == 'POST':
        print('success')
        #########################################receiving user detail##############################################
        first_name = request.POST['first_name']  # name in html
        last_name = request.POST['last_name']
        phone = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        is_promo = request.POST['promotion']

        ######################optional data#########################################
        addr = request.POST.get('address', None)
        aptn = request.POST.get('aptNumber', None)
        # city = request.POST.get('city', None)
        state = request.POST.get('state', None)
        country = request.POST.get('country', None)
        zip = request.POST.get('zip', None)

        cardHolderName = request.POST.get('cardHolderName', None)
        cardNum = request.POST.get('cardNum', None)
        print(cardNum)
        expiryDate = request.POST.get('expiryDate', None)
        last_four = cardNum[-4:]
        cardNum = request.POST.get('cardNum', None)
        print('Decryption')
        print(cardNum)
        print(last_four)
        print('Got Data')
        #############################################check if email is in use#####################################################
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email address is already in use', extra_tags='taken')
            return redirect('registration')
        # else:
        #     print('going to save')

        ####################################################save to db####################################################
        user = User.objects.create_user(password=password1, email=email, first_name=first_name, last_name=last_name)

        # print(type(user))
        if is_promo == "on":
            user.is_promo = True
        # if phone == '':
        #     user.phone = 0
        # else:
        #     user.phone = phone
        user.phone = phone
        user.address = addr
        user.apartNumber = aptn
        # user.city = city
        user.state = state
        user.country = country
        user.zip = zip
        # user.cardname = cname
        # user.ccnum = ccnum
        # user.valid = valid

        # if addr == '':
        #     addr = null
        # user.set_password(password1)
        print(user.is_active)
        user.is_active = False
        print(user.is_active)
        print(user.first_name)

        print('saving...')
        user.save()
        print('User created')
        print(user.first_name)

        card = Card.objects.create(cardHolderName=cardHolderName, expiryDate=expiryDate, user_id=user.id)
        card.cardHolderName = cardHolderName
        card.cardNum = encryption(cardNum)
        card.expiryDate = encryption(expiryDate)
        card.last_four = last_four
        print(cardNum)


        card.save()
        activateEmail(request, user, email)  # email confirmation
        return redirect('accountSuccess')  # success #register
    else:
        return render(request, 'registration.html');


def activateEmail(request, user, to_email):
    print(user.first_name + 'in activateEmail')
    fname = user.first_name
    print(fname + ' new var')
    mail_subject = 'Activate your user account.'
    message = render_to_string('activationmail.html', {
        'fname': fname,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.email)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    print(message)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.info(request, f'Dear {fname}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.',
                      extra_tags='verify')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def index(request):
    # new_movies = EbookingMovie.objects.filter(status="coming_soon")
    # present_movies = EbookingMovie.objects.filter(status="airing")

    movies = Movie.objects.values()
    moviesPlaying = movies.filter(status='Now Playing')
    moviesComingSoon = movies.filter(status='Coming Soon')

    context = {
        'moviesNow': moviesPlaying,
        'moviesSoon': moviesComingSoon
    }
    return render(request, 'index.html', context)


def movie_description(request):
    print('movie_description')
    name = request.GET.get('cinema_button')
    name = request.GET.get('cinema_button')
    movies = Movie.objects.filter(name=name).values()

    context = {
        'movies' : movies
    }
    #print(context)
    return render(request, 'movie_description.html', context)

def show_time(request):
    name = request.GET.get('movie_title')
    print(name)
    movies = Movie.objects.filter(name=name).values('id')
    movieId = movies[0].get('id')
    showTimes = ScheduleMovie.objects.filter(movie_id=movieId).values()
    list = []
    showDateSet = set()
    for s in showTimes.order_by('showDate'):
        showDateSet.add(s.get('showDate'))
    for s in showTimes.order_by('showDate'):
        if s.get('showDate') in showDateSet:
            thisdict = {}
            thisdict['theatreid'] = ShowRoom.objects.filter(id=s.get('theatre_id')).values('theatre')[0].get('theatre')
            thisdict['showDate']= (s.get('showDate')).strftime("%m-%d-%Y")
            i = 1
            for show in showTimes.order_by('showDate'):
                if s.get('theatre_id') == show.get('theatre_id') and s.get('showDate') == show.get('showDate'):
                    showtime = 'show'+str(i)
                    i = i+1
                    thisdict[showtime] = show.get('MovieTime')
            showDateSet.remove(s.get('showDate'))
            list.append(thisdict)

    context = {
        'movies' : list
    }
    print(context)
    # return showtime information as a JSON response
    return JsonResponse(context)

def base(request):
     
    results = []

    if request.method == 'GET':
        movie_category = request.GET.get('movie_category', None)
        movie_name = request.GET.get('movie_name', None)
        count = 0
        print(movie_category)
        print(movie_name)
        if movie_name == '' and movie_category == 'ALL':
            results = Movie.objects.all()
            count  = Movie.objects.all().count()
        elif movie_name != '' and movie_category != '':
            results = Movie.objects.filter(Q(name__icontains = movie_name)|Q(category1__icontains = movie_category)|Q(category2__icontains = movie_category)|Q(category3__icontains = movie_category))
            count = Movie.objects.filter(Q(name__icontains = movie_name)|Q(category1__icontains = movie_category)|Q(category2__icontains = movie_category)|Q(category3__icontains = movie_category)).count()
        elif movie_name != '':
            results = Movie.objects.filter(name = movie_name)
            count = Movie.objects.filter(name = movie_name).count()
        elif movie_category != '':
            results = Movie.objects.filter(Q(category1__icontains = movie_category)|Q(category2__icontains = movie_category)|Q(category3__icontains = movie_category))
            count = Movie.objects.filter(Q(category1__icontains = movie_category)|Q(category2__icontains = movie_category)|Q(category3__icontains = movie_category)).count()
        else:
            results = Movie.objects.all()
            count = Movie.objects.all().count()
    if len(results) == 0:
        messages.error(request, 'No movie exists for given title or category', extra_tags='exist')
        results = Movie.objects.all()
        moviesPlaying = results.filter(status='Now Playing')
        moviesComingSoon = results.filter(status='Coming Soon')
        context = {
            'moviesNow': moviesPlaying,
            'moviesSoon': moviesComingSoon
        }
        return render(request, 'index.html', context)
    moviesPlaying = results.filter(status='Now Playing')
    moviesComingSoon = results.filter(status='Coming Soon')

    context = {
        'moviesNow': moviesPlaying,
        'moviesSoon': moviesComingSoon
    }
    print(results)
    return render(request, 'index.html', context)


def regisconfirmation(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        print('verified')

        messages.info(request, 'Thank you for your email confirmation. Now you can login your account.',
                      extra_tags='activated')
        return redirect('accountVerify')  # login page
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('index')  # homepage


def forgot_password_view(request):
    return render(request, "forgot_password.html")


def account_success(request):
    return render(request, "accountSuccess.html")


def account_verify(request):
    return render(request, "accountVerify.html")



def forgot_password_validation(request):
    return render(request, "new_password.html")


def account_notverified(request):
    return render(request, "accountNotVerified.html")

def edit_profile(request):
    User = get_user_model()
    if request.method == 'GET':
        mydata = User.objects.filter(email=request.user).values()
        print(mydata)
        template = loader.get_template('edit_profile.html')
        context = {
            'profileable': mydata
        }
        return HttpResponse(template.render(context, request))
    else:
        email1 = request.POST.get("email")
        print(email1)
        try:
            user = User.objects.get(email=request.user)
            print(user.email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.phone = request.POST['phone_number']
            user.address = request.POST['streetAddressBilling']
            print(user.address)
            # user.first_name = request.POST.get("aptNumberBilling")

            user.state = request.POST['stateBilling']
            user.zip = request.POST['zipCodeBilling']
            user.apartNumber = request.POST['aptNumberBilling']
            user.country = request.POST['country']
            if request.POST.get('promotion') == 'on':
                user.is_promo = True
            else:
                user.is_promo = False
            print(user.is_promo)
            user.save()
            print('profile updated successfully')
            confirmEmailProfileUpdation(user)
            messages.info(request, 'Your profile has  been updated!!!', extra_tags='success')
            return redirect('/edit_profile')


def edit_password(request):
    if request.method == 'POST':
        currentPassword = request.POST.get("current_password")
        newPassword = request.POST.get("new_password")
        confirmPassword = request.POST.get("confirm_password")
        user = auth.authenticate(email=request.user, password=currentPassword)
        if user is not None:
            if newPassword == confirmPassword:
                currentUser = User.objects.get(email=request.user)
                currentUser.set_password(newPassword)
                currentUser.save()
                messages.info(request, 'Successfully changed password', extra_tags='success')
                print('Updated')
                confirmEmailPasswordUpdation(currentUser)
                # conf_Email(request, currentUser, request.user)
                return redirect('/login')
            else:
                messages.info(request, 'Password not matching', extra_tags='match')
                print('Password not matching')
                return render(request, 'new_password.html')
        else:
            if currentPassword is not None:
                messages.info(request, 'Failed to Authenticate, reset through email link', extra_tags='fail')
                print("Failed to Authenticate, reset through email link")
            return render(request, 'new_password.html')
    else:
        return render(request, "new_password.html")


def edit_card(request):
    
    if request.method == 'POST':
        print(request.user)
        user = User.objects.get(email=request.user)
        print(user.id)
        updated = False
        if user is not None :
            card_count = 0
            cards = []
            containsRecord = False
            for key, value in request.POST.items():
                if key.startswith('cardHolderName_'):
                   containsRecord = True
                   card_count = key.split("_")[1]
                   card = {}
                   card['cardHolderName'] = value
                   card['cardNum'] = encryption(request.POST.get(f'cardNum_{card_count}'))
                   card['expiryDate'] = encryption(request.POST.get(f'expiryDate_{card_count}'))
                   card['last_four'] = request.POST.get(f'cardNum_{card_count}')[-4:]
                   cards.append(card)
                   print("Adding")
            if containsRecord == True:
                print("Deleting record now")
                 # retrieve the record to be deleted
                card_to_delete = Card.objects.filter(user_id=request.user.id)
                # delete the record
                card_to_delete.delete()
            print(cards)
            for card in cards:
                # save each card object to the database
                obj, created = Card.objects.get_or_create(
                    user_id=user.id,
                    cardHolderName=card['cardHolderName'],
                    cardNum=card['cardNum'],
                    last_four=card['last_four'],
                    expiryDate=card['expiryDate']
                )
                if created:
                   updated = True
                   print('Record created')
                else:
                    print('Record Skipped')
            
            mydata = Card.objects.filter(user_id=user.id).values()
            for data in mydata:
                # modify values as needed
                data['cardNum'] = decryption(data['cardNum'])
                data['expiryDate'] = decryption(data['expiryDate'])
                data['last_four'] = decryption(data['last_four'])
                #data['cardHolderName'] = decryption(data['cardHolderName'])
            
            template = loader.get_template('edit_card.html')
            context = {
                'cards': mydata
            }
            if updated == True:
                messages.info(request, 'Successfully updated the payment details for the user.')
            return HttpResponse(template.render(context, request))
    
    print(request.user)
    user = User.objects.get(email=request.user)
    print(user.id)
    mydata = Card.objects.filter(user_id=user.id).values()
    template = loader.get_template('edit_card.html')
    context = {
        'cards': mydata
        }
            
    return HttpResponse(template.render(context, request))


def orderconfirmation(request, order):
    return render(request, "orderConfirmation.html")


def book_movie(request):
    return render(request, 'bookmovie.html')


def seats(request):
    return render(request, 'seats.html')


def summary(request):
    return render(request, 'summary.html')


def checkout(request):
    return render(request, 'checkout.html')


def password_reset_confirmation(request):
    return render(request, 'passwordresetconfirm.html')

def pwd_reset(request):
    if request.method == 'POST':
        email = request.POST['email']
        mydata = User.objects.filter(email=email).values()

        # print(mydata)
        if mydata.exists():
            mydata1 = User.objects.get(email = email)
            resetPwdEmail(request, mydata1, email) #reset function call
            #messages.info(request,'Password Reset link has been sent to your Email Id. Please click on \
            #received reset link to reset your password. Note: Check your spam folder.',extra_tags='exist')
            return render(request,"forgot_password.html")
        else:
            messages.info(request,'No account exists for provided Email Id. Please check it once and try sending the link again',extra_tags='exist')
            return render(request,"forgot_password.html")


    else:
        return render(request,"forgot_password.html")
    
def resetPwdEmail(request, user, to_email):
    # print(user.first_name + 'in resetEmail')
    firstname = user.first_name
    # print(fname + ' new var')
    mail_subject = 'Cinema EBooking Password Reset Link'
    message = render_to_string('pwdresetmail.html', {
        'firstname': firstname,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    print(message)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.info(request, f'Dear {firstname}, a password reset link is sent to your {to_email} inbox. Please click on \
            received reset link to reset your password. Note: Check your spam folder.')
    else:
        messages.error(request, f'Some issue with sending mail to {to_email}, check if you typed it correctly.')
        
def forgot_password_validation(request,  uidb64, token):  
    
    if request.method == 'POST':

        currentpassword = request.POST['current_password']
        newpassword1 = request.POST['new_password']
        newpassword2 = request.POST['new_password2']
        if newpassword1 == newpassword2:
            User = get_user_model()
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            
            user2 = auth.authenticate(email=user.email, password=currentpassword)
            if user2 is None:
                messages.info(request, 'Current password entered is incorrect. Please try again with the link sent to mail earlier.', extra_tags='invalid')
                return render(request, 'passwordresetconfirm.html')
            if user is not None and account_activation_token.check_token(user, token):
                user.set_password(newpassword1)
                print(user.password)
                user.save()
                messages.info(request,"Password is reset successfully. Please login with the new password.")
                return render(request, 'passwordresetconfirm.html') #success page

            else:
                messages.info(request, 'Reset link is invalid! Please check the link or resend a new link to you email.')
                return render(request, 'passwordresetconfirm.html') #success page
               
        else:
            messages.info(request, 'Passwords do not match, please try again with the link sent to email', extra_tags='match')
            return render(request, 'passwordresetconfirm.html')
       
    else:
        return render(request, "passwordreset.html")

def reset_password(request):
    return render(request, 'passwordreset.html')

def confirmEmailProfileUpdation(user):
    try:
        send_mail(
            subject='Profile Updated!!!',
            message='Dear {name},\nYour Profile has been updated successfully'.format(name=user.first_name),
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
    except:
        pass

def confirmEmailPasswordUpdation(user):
    try:
        send_mail(
            subject='Password Changed!!!',
            message='Dear {name},\nYour password has been changed successfully'.format(name=user.first_name),
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
    except:
        pass

def notifyPromo(request, promo_id):
    allUsers = User.objects.filter(is_promo=True)
    promo = get_object_or_404(Promotion,pk=promo_id)
    promooff = promo.discount
    code = promo.promo_code
    validuntil = promo.valid_upto
    mail_subject = 'New promotion, Avail Now'
    for user in allUsers:
        first_name = user.first_name
        to_email = user.email
        message = render_to_string('promomail.html', {
        'firstname': first_name,
        'promooff': promooff,
        'code': code,
        'validuntil': validuntil
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            print(f' User : {to_email} notified successfully')

def encryption(message):
    encrypted = ""
    for char in message:
        if char.isalpha():
            encrypted += chr(ord('a') + (ord(char) - ord('a') + 13) % 26) # replace characters with ROT13 shift
        elif char.isdigit():
            encrypted += str((int(char) + 5) % 10) # replace integers with +5 modulus 10
        else:
            encrypted += char
    return encrypted

def decryption(encrypted):
    decrypted = ""
    for char in encrypted:
        if char.isalpha():
            decrypted += chr(ord('a') + (ord(char) - ord('a') - 13) % 26) # reverse ROT13 shift for characters
        elif char.isdigit():
            decrypted += str((int(char) - 5) % 10) # reverse +5 modulus 10 for integers
        else:
            decrypted += char
    return decrypted

