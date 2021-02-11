from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.serializers import serialize
from django.core import serializers
import json
from .models import Locations, NewsLetter, Quiz

#Account

            
def newsletter(request):
    if request.method =='POST':
        email = request.POST.get('email')
        print(email)
        nl = NewsLetter(email= email)
        nl.save()
        #email for sub
        template_locator = render_to_string('Email_templates/email_for_sub.html')
        email_locator = EmailMessage(
            'Thanks For Subscribing To Our Newsletter ~ SaniJunk',
            template_locator,
            settings.EMAIL_HOST_USER,
            [email],

            )
        email_locator.fail_silently = False
        email_locator.send()
       

        


    
    return HttpResponseRedirect('/')
# def signup_home(request):
    
    
#     return render(request,'signup.html')
def signup(request):
    context= {}
    if request.method =='POST':
        mail = request.POST.get('email','')
        username = request.POST.get('username','')
        name = request.POST.get('name','')
        password = request.POST.get('password','')
        conf_pass = request.POST.get('confirm_password','')

        #remove duplicate usernames:
        userCheck = User.objects.filter(username=username)
        if len(username) > 20:
            messages.warning(request,'Username Is Too Long')
            # return redirect('/signup')
            return render(request,'signup.html', context)
            
        if userCheck :
            messages.warning(request,'Choose Different Username')
            # return redirect('/signup')
            return render(request,'signup.html', context)
        
        if password == conf_pass:
            user_obj = User.objects.create_user(first_name = name, password = password, email= mail, username=username)
            user_obj.save()
            
            messages.success(request, 'Account Created Successfully')
            trick_btn = "button_toggle"
            context={
                'trick_btn':trick_btn,
            }
            return render(request,'signup.html', context)

        else:
            
            messages.warning(request, 'Passwords Do not Match')
            return render(request,'signup.html', context)
    else:
        return render(request,'signup.html', context)

            
    
    
def user_login(request):
    if request.method =='POST':
        user_name = request.POST.get('username', '')
        user_password = request.POST.get('password', '')

        user = authenticate(username=user_name, password= user_password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect('/signup')
            
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('/signup')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('/signup')


# Create your views here.
def home(request):
    locations_all = Locations.objects.all()
    locations_ex = Locations.objects.filter(sanitized="Yes")
    locations = locations_all.difference(locations_ex)
    context = {
        "locations":locations
    }
        
    return render(request, "index.html",context)
@login_required(login_url='/signup_home')
def add_location(request):
    locations_all = Locations.objects.all()
    locations_ex = Locations.objects.filter(sanitized="Yes")
    locations = locations_all.difference(locations_ex)
    context = {
        "locations":locations
    }
    if request.method =='POST':
        coordinates = request.POST.get('pos')
        name = request.POST.get('Name')
        email = request.POST.get('email')
        op = request.POST.get('gridRadios')
        sat = request.POST.get('saturation')
        
        print(coordinates)
        if coordinates:
            myList = coordinates.replace(')','').replace('(','').split(',')
        
            print(sat)
            

            print(name)
            print(op)
            #checking spam
            posts1 = Locations.objects.filter(locator_user= request.user)
            posts2 = Locations.objects.filter(time__day= timezone.now().day)
            nu = 0 
            if Locations.objects.filter(locator_user= request.user):
                if Locations.objects.filter(locator_user= request.user).order_by('-time')[0].time.month  == timezone.now().month and Locations.objects.filter(locator_user= request.user).order_by('-time')[0].time.year  == timezone.now().year :

                    posts = posts1.intersection(posts2)
                    nu = len(posts)
                print(nu)
                if nu <2:
                    inst = Locations(name = name,garbageType=op,coordinates_lat=myList[0], coordinates_lng=myList[1], saturation=sat, locator_mail=email, locator_user=request.user)
                    inst.save()
                    loc = Locations.objects.filter(name = name,garbageType=op,coordinates_lat=myList[0], coordinates_lng=myList[1], saturation=sat, locator_mail=email, locator_user=request.user)[0]
                    template_subs = render_to_string('Email_templates/email_to_subs.html', {'name':loc.name, 'email': loc.locator_mail,'Key':loc.pk })
                    list1 = []
                    for i in NewsLetter.objects.all():
                        if list1.__contains__(i.email):
                            pass
                        else:
                            list1.append(i.email)
                    print(list1)
                    email_subs = EmailMessage(
                    name + ' , Has Claimed to Locate',
                    template_subs,
                    settings.EMAIL_HOST_USER,
                    list1,

                    )
                    email_subs.fail_silently = False
                    email_subs.send()
                    messages.success(request,'Location Has Been Added ')
                else:
                    messages.warning(request,'Stop Spamming')
            else:

                inst = Locations(name = name,garbageType=op,coordinates_lat=myList[0], coordinates_lng=myList[1], saturation=sat, locator_mail=email, locator_user=request.user)
                inst.save()
                loc = Locations.objects.filter(name = name,garbageType=op,coordinates_lat=myList[0], coordinates_lng=myList[1], saturation=sat, locator_mail=email, locator_user=request.user)[0]
                template_subs = render_to_string('Email_templates/email_to_subs.html', {'name':loc.name, 'email': loc.locator_mail,'Key':loc.pk })
                list1 = []
                for i in NewsLetter.objects.all():
                    if list1.__contains__(i.email):
                        pass
                    else:
                        list1.append(i.email)
                print(list1)
                email_subs = EmailMessage(
                name + ' , Has Claimed to Locate',
                template_subs,
                settings.EMAIL_HOST_USER,
                list1,

                )
                email_subs.fail_silently = False
                email_subs.send()
                messages.success(request,'Location Has Been Added ')
                

            


            
        else:
            messages.warning(request,'Choose A Location From Map !!')


        
    return render(request, "add_location.html", context)
def details(request, pk):
    locations = Locations.objects.filter(pk=pk)
    satu = int(locations[0].saturation)
    context = {
        "locations":locations,
        "satu":satu
        
    }
    return render(request, "details.html", context)
def sanitize(request, pk):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('email')
        

        locations = Locations.objects.filter(pk=pk)[0]
        locations.sanitizer_mail = email
        locations.sanitized = "Under Sanitization"
        locations.save()
        #email to locator 
        template_locator = render_to_string('Email_templates/email_to_locator.html', {'name':name, 'email': email,'Key':locations.pk })
        email_locator = EmailMessage(
            name + ' , Has Claimed to Sanitize',
            template_locator,
            settings.EMAIL_HOST_USER,
            [locations.locator_mail],

            )
        email_locator.fail_silently = False
        email_locator.send()
        # satu = int(locations[0].saturation)
        context = {
        "locations":locations,
        # "satu":satu

        }
        return render(request, "sanitize.html", context)
    else:
        return HttpResponseRedirect('/')
    
@login_required(login_url='/signup_home')
def verify(request, pk):
    locations_ = Locations.objects.filter(pk=pk)
    satu = int(locations_[0].saturation)
    context = {
        "locations":locations_,
        "satu":satu
        
    }
    if request.user == locations_[0].locator_user:
        if request.method == 'POST':
            # name = request.POST.get('Name')
            # email = request.POST.get('email')
            verify_ = request.POST.get('verify_check')
            print(verify_)
            
            

            locations = Locations.objects.filter(pk=pk)[0]
            email= locations.sanitizer_mail
            if verify_ =="on":

                locations.sanitized = "Yes"
                locations.save()
                #email to locator 
                template_sanitizer = render_to_string('Email_templates/email_to_sanitizer.html', { 'email': email, })
                email_sanitizer = EmailMessage(
                    email + ' , Your Sanitization Has Been Verified',
                    template_sanitizer,
                    settings.EMAIL_HOST_USER,
                    [locations.sanitizer_mail],

                    )
                email_sanitizer.fail_silently = False
                email_sanitizer.send()
                tick = "Yep"
                context = {
                        "locations":locations_,
                        "satu":satu,
                        "tick":tick
                        
                        }
    else:
        messages.warning(request,'you are not Autherizedto Do This')

        
    return render(request, "verify.html", context)









def list(request):
    locations = Locations.objects.all().order_by("-time")
    context={
        "locations":locations

    }
    return render (request,'list_.html', context)

    
    
def founders(request):
    return render(request, "founders.html")
def quiz(request):
    quiz = Quiz.objects.all().order_by('-time')
    lt = []
    for i in quiz:
        # print(i.question)
        lt.append(
             '{' +
            '"' + 'question' +'"' + ':' +'"'+ i.question + '"'+','
            '"' +'opt1'+ '"' + ':' + '"'+i.opt1 + '"'+","
            '"'+'opt2' +'"'+ ':' + '"'+ i.opt2 +'"'+ ","
            '"' +'opt3'+'"' + ':' +'"'+ i.opt3 + '"'+","
            '"'+'Answer'+'"' + ':' +'"'+ i.answer +'"'+ ""
             + '}'
            
        )
    # print(lt)
    context = {
        'quiz':lt,
        'for_ans':quiz,
        
    }
    return render(request, "quiz.html", context)





    
