from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages

from django.template.response import TemplateResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.utils.encoding import smart_str
# Create your views here.

from .forms import AssetTransportRequestForm, SignupForm, LoginForm, AddRideForm, ApplicationStatusUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

import datetime


# Models

from .models import Requester, Rider, AssetTransportationRequest, RideTravelInfo, Application
from .models import UserType, AppStatus

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.decorators.csrf import csrf_exempt
     


### Session Related Info
class LoggedUser:
    USER = None
    TRANSPORTREQUEST = None
    TRANSPORTREQUEST_SAVED = False
    Paginator = None

    def __init__(self):
        self.USER = LoggedUser.USER

    def getUserName():
        return LoggedUser.USER.name

    def getUserEmail():
        return LoggedUser.USER.email

    def getUserType():
        return LoggedUser.USER.type
    

def isAuthorised(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    if LoggedUser.getUserType() != UserType.RIDER:
        return HttpResponse('Not authorised to access this page')

def index(request):

    # if request.user.is_authenticated:
    #     return redirect("home")
    # form = AssetTransportRequestForm()
    # # return HttpResponse("Hello, World!")
    # context = {'form':form, 'loggedin':LoggedUser.USER, 'title': 'Get Started'}

    # # print(context)

    # return render(request, 'base.html', context)

    return redirect('home')



def home(request):

    if LoggedUser.USER is None:
        return redirect('signout')
    # form = AssetTransportRequestForm()
    # return HttpResponse("Hello, World!")

    if not request.user.is_authenticated:
        return redirect("signin")

    page = request.GET.get('page', 1)


    form = ApplicationStatusUpdateForm(request.POST)

    if request.method=="POST":
        if form.is_valid():
            print("HomStatus update  form is valid")
            data = form.cleaned_data
            print(data['application_id'])
            application = Application.objects.get(id = int(data['application_id']))
            application.status = data['status']
            application.save()
            messages.success(request, "Status updated")
            # print(data)

    
   
    application_list = Application.objects.filter(applicant=LoggedUser.USER) if LoggedUser.getUserType() == UserType.REQUESTER  else Application.objects.all() 

    paginator = Paginator(application_list,1)

            



    # context = {'title': 'Home', 'name': LoggedUser.getUserName(), 'email': LoggedUser.getUserEmail(), 'type': LoggedUser.getUserType(), 'loggedin':LoggedUser.USER}
        

    print("paginator", paginator.num_pages, paginator.count)
    try:
        application_list = paginator.page(page)   
    except PageNotAnInteger:
        application_list = paginator.page(1)
    except EmptyPage:
        application_list = paginator.page(paginator.num_pages)


    context={'title':'Home', 'application_list':application_list, 'loggedin':LoggedUser.USER}
    if LoggedUser.getUserType() == UserType.RIDER:
        context['statusform'] = AppStatus.choices


    # return render(request, 'home.html', context=context)
  
    return HttpResponse(context)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


######################### Requester
def signup(request):

    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            print("Signup form is valid")
            data = form.cleaned_data

            print("Singup data", data)



            username = data['email']
            first_name, last_name = data['name'].split()
            password1 = data['password']
            confirm_password = data['confirm_password']

            user_type = data['type']

            if password1 != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('/signup')
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1)

            
            New_User_Class = Requester if user_type == UserType.REQUESTER else Rider
            new_user = New_User_Class.objects.create(user=user, email = username, name = data['name'], type = user_type)
            user.save()
            new_user.save()

            messages.success(request, f'{user_type} Signup successful !!')

            return redirect('signin')



            # return HttpResponse(f'Signup form is valid {data = }')
            
    
        
    return render(request, 'form.html', {'form': form, 'title': 'Sign Up'})




def signin(request):

    # logout(request)

    print("user authenticated",request.user.is_authenticated )

    if request.user.is_authenticated:
        return redirect("home")
    
    form = LoginForm(request.POST)

    if request.method == "POST":

        if form.is_valid():

            data = form.cleaned_data
            email = data['email']
            password = data['password']
            try:

                username = User.objects.get(username=email.lower()).username
                print("username",username)

            except Exception as e:
                messages.warning(request, f"Ohh no!! it seems you haven't registered with us, Please do register.")
                return redirect('signup')
            user = authenticate(username=email, password=password)
            if user is None:
                messages.warning(request, f'Hi {username}, please enter correct password')
                return redirect('signin')


            find_user = None
            try:
                find_user =  Requester.objects.get(user=user)
            except Exception as e:
                find_user = Rider.objects.get(user=user)
            if find_user is not None:
                LoggedUser.USER = find_user
                login(request, user)
                messages.success(request, f'Login Successful. Welcome, {find_user.name}')
                # return render(request, "home.html", {'name': find_user.name, 'type': find_user.type, 'email': find_user.email})  
                return redirect('home')  
                        
            


    # return render(request, 'form.html', {'title': 'Login', 'form': form})
    return HttpResponse("Login Please")

def signout(request):

    if not request.user.is_authenticated:
        return redirect("signin")
        
    LoggedUser.Paginator = None
    LoggedUser.USER = None
    logout(request)

    messages.info(request, 'Logout successful !!')

    return redirect("index")



def addRide(request):

    if LoggedUser.USER is None:
        return redirect('signout')

    if not request.user.is_authenticated:
        return redirect("login")

    # if LoggedUser.USER is None:
    #     LoggedUser.USER = Rider.objects.get(user= request.user)
    

    if LoggedUser.getUserType() != UserType.RIDER:
        return HttpResponse(f'Not authorised to access this page {request.user}')
        


    form = AddRideForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            rider = LoggedUser.USER
            data['rider'] = rider
            print("Add Ride form is valid", data)
            

            
            # from_location = data['from_location']
            # to_location = data['to_location']
            # date_time = data['date_time']
            # flexible_timings = data['flexible_timings']
            # travel_medium = data['travel_medium']
            # assets_quanity = data['assets_quanity']

            ride = RideTravelInfo.objects.create(**data)
            ride.save()

            messages.success(request, 'Ride Travel added successfully')




    context = {'title': 'Add Ride', 'form': form}

    # print(context)
    # return HttpResponse('Add a Ride Travel Info')

    return render(request, 'form.html', context)

    

def editRide(request, ride_id):

    if LoggedUser.USER is None:
        return redirect('signout')


    if not request.user.is_authenticated:
        return redirect("signin")

    if LoggedUser.getUserType() != UserType.RIDER:
        return HttpResponse('Not authorised to access this page')

    ride = None
    try:
        ride = RideTravelInfo.objects.get(id=ride_id)
    except Exception as e:
        messages.warning(request, 'Invalid id')
        return redirect('home')
    print("edit_ride", ride)
    # return HttpResponse(f'edit Ride Travel Info {ride}')
    initial_dict={
        "from_location": ride.from_location,
        "to_location": ride.to_location,
        "date_time": ride.date_time.strftime("%Y-%m-%d %H:%M:%S"),
        "flexible_timings": ride.flexible_timings,
        "travel_medium": ride.travel_medium,
        "assets_quanity": ride.assets_quanity
    }
    print(initial_dict)

    form = AddRideForm(request.POST or None, initial = initial_dict)

    if request.method == "POST":

        if form.is_valid():
            
            data = form.cleaned_data
            print("form is valid",form.cleaned_data)
            ride.from_location = data['from_location']
            ride.to_location = data['to_location']
            ride.date_time = data['date_time']
            ride.flexible_timings = data['flexible_timings']
            ride.travel_medium = data['travel_medium']
            ride.assets_quanity = data['assets_quanity']
            ride.save()

            messages.success(request, 'Updated successful')
    
        else:
            print("Edit form not valid")

    else:
        print("request method is GET")
   
    return render(request, 'form.html', {'form': form, 'title': 'Edit Ride'})

def rideList(request):

    if LoggedUser.USER is None:
        return redirect('signout')


    if not request.user.is_authenticated:
        return redirect("signin")

    if LoggedUser.getUserType() != UserType.RIDER:
        return HttpResponse('Not authorised to access this page')

    rides = RideTravelInfo.objects.filter(rider = LoggedUser.USER)
   
    # for ride in rides:
    #     print(ride)
    #     rides['applications'] = Application.objects.filter(ride_travel_info = ride)

    print("ride_list", rides)
    
    # return HttpResponse(f'Ride Travel List {rides}')


    content = TemplateResponse(request, 'ride_list.html', {'ride_list': rides})
    print('home content', content, content.render())


    return render(request, 'ride_list.html', {'ride_list': rides, 'title': 'Ride List', 'loggedin':LoggedUser.USER})

def allApplicants(request):
    if LoggedUser.USER is None:
        return redirect('signout')

    return HttpResponse('All Applicants')



def search(request):
    if LoggedUser.USER is None:
        return redirect('signout')

    page = request.GET.get('page', 1)
    form = AssetTransportRequestForm(request.POST)

    normal_form = render(request, 'form.html', {'form': form,  'title': 'Search', 'loggedin':LoggedUser.USER})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if form.is_valid():
            # print("valid form",form.cleaned_data)
            data = form.cleaned_data
            
            if data['date_time'] < datetime.datetime.now():
                messages.warning(request, 'Please provide a valid date and time')
                return normal_form

            LoggedUser.TRANSPORTREQUEST = data
            search_data = RideTravelInfo.objects.filter(from_location = data['from_location'], assets_quanity__gte=data['assets_quanity']).values()

            search_result = search_data
            # print("search data", search_data, len(search_data))

            applied_data = Application.objects.filter(applicant=LoggedUser.USER)
            
            # applied_ride_ids = [i.ride_travel_info.id for i in applied_data]

            apps = {}
            for i in applied_data:
                apps[i.ride_travel_info.id] = i.status
            

           
            # print("statuses", apps)
        

            for data1 in search_result:
                data1['date_time'] = data1['date_time'].strftime("%d/%m/%Y, %H:%M %p")
                data1['rider'] = Rider.objects.get(id=data1['rider_id'])
                data1['apply_status'] = apps[data1['id']] if data1['id'] in apps else 'Apply'
                data1['asset_type'] = data['asset_type']
                data1['asset_sensitivity'] = data['asset_sensitivity']
                data1['whom_to_deliver'] = data['whom_to_deliver']
#
            print("search result", search_result, "length", len(search_result))

            # print("data1", data1, "length ", len(data1))

            paginator = Paginator(search_result,page)

            LoggedUser.Paginator = paginator

            
        
    if request.GET.get('page') or request.method == 'POST':
        
        paginator = LoggedUser.Paginator

        print("paginator", paginator.num_pages, paginator.count)
        try:
            search_result = paginator.page(page)   
        except PageNotAnInteger:
            search_result = paginator.page(1)
        except EmptyPage:
            search_result = paginator.page(paginator.num_pages)

        return render(request, 'search_result.html', {'form': form,  'title': 'Search Result', 'matched_transportation_requests':search_result, 'loggedin':LoggedUser.USER})
   

    return normal_form


def ride_apply(request, ride_id):
    if LoggedUser.USER is None:
        return redirect('signout')
    if not request.user.is_authenticated:
        return redirect("signin")

    if LoggedUser.getUserType() != UserType.REQUESTER:
        return HttpResponse('Not authorised to access this page')
    

    ride = RideTravelInfo.objects.get(id=ride_id)
    applicant = Requester.objects.get(user=request.user)
    print(ride)
    if not LoggedUser.TRANSPORTREQUEST_SAVED:
        LoggedUser.TRANSPORTREQUEST = AssetTransportationRequest.objects.create(**LoggedUser.TRANSPORTREQUEST)
        LoggedUser.TRANSPORTREQUEST.save()
        LoggedUser.TRANSPORTREQUEST_SAVED = True
        messages.success(request, "Asset Transport Request form saved")
    
    LoggedUser.SearchList = None
    application = Application.objects.create(applicant=applicant, assetTransportationRequest= LoggedUser.TRANSPORTREQUEST, ride_travel_info= ride)
    application.save()

    messages.success(request, "Application successfully applied")
    return HttpResponse(f'Apply for Transportation Request {ride_id} {ride} {application}')

