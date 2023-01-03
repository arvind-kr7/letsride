from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Forms

from .forms import AssetTransportRequestForm, SignupForm, LoginForm, AddRideForm, ApplicationStatusUpdateForm


# Models

from .models import Requester, Rider, AssetTransportationRequest, RideTravelInfo, Application
from .models import UserType, AppStatus


### Session's user Related Info

def loggeduser(user):


    find_user= None
    try:
        find_user =  Requester.objects.get(user=user)
    except Exception as e:
        find_user = Rider.objects.get(user=user)

    return find_user



def isAuthorised(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    if loggeduser(request.user).type != UserType.RIDER:
        return HttpResponse('Not authorised to access this page')


def api(request):

    return JsonResponse({"message":"hello Api"})

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

    print("request.user.is_anonymous", request.user.is_anonymous)

    if not request.session.get('loggedin', False):
        return redirect('signout')
    # form = AssetTransportRequestForm()
    # return HttpResponse("Hello, World!")

    if not request.user.is_authenticated:
        return redirect("signin")

    user = loggeduser(request.user)

    if user.type == UserType.REQUESTER: 
        context = {'title': 'Home', 'loggedin':user, 'search_requests':AssetTransportationRequest.objects.filter(requester=user)}
        return render(request, 'req_home.html', context=context)



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

    
  
    application_list = Application.objects.filter(ride_travel_info__rider=user).order_by('assetTransportationRequest__date_time')

    paginator = Paginator(application_list, 1)
    try:
        application_list = paginator.page(page)   
    except PageNotAnInteger:
        application_list = paginator.page(1)
    except EmptyPage:
        application_list = paginator.page(paginator.num_pages)


    context={'title':'Home', 'application_list':application_list, 'loggedin':user, 'statusform': AppStatus.choices}


    return render(request, 'rider_home.html', context=context)
    # return HttpResponse(content.render())





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
            
    
        
    return render(request, 'form.html', context= {'form': form, 'title': 'Sign Up'})




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
                
                login(request, user)

                request.session['loggedin']=True
                messages.success(request, f'Login Successful. Welcome, {find_user.name}')
                # return render(request, "home.html", {'name': find_user.name, 'type': find_user.type, 'email': find_user.email})  
                return redirect('home')          
            


    return render(request, 'form.html', {'title': 'Login', 'form': form})

def signout(request):

    if not request.user.is_authenticated:
        return redirect("signin")
        
    logout(request)
    try:
        del request.session['loggedin']
    except KeyError:
        pass

    messages.info(request, 'Logout successful !!')

    return redirect("index")



def addRide(request):

    if not request.session.get('loggedin', False):
        return redirect('signout')

    if not request.user.is_authenticated:
        return redirect("login")

    # if LoggedUser.USER is None:
    #     LoggedUser.USER = Rider.objects.get(user= request.user)
    
    user = loggeduser(request.user)
    if user.type != UserType.RIDER:
        return HttpResponse(f'Not authorised to access this page {request.user}')
        


    form = AddRideForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
           
            data['rider'] = user
            print("Add Ride form is valid", data)
    

            ride = RideTravelInfo.objects.create(**data)
            ride.save()

            messages.success(request, 'Ride Travel added successfully')

            return redirect('home')


    context = {'title': 'Add Ride', 'form': form, 'loggedin': user}

    # print(context)
    # return HttpResponse('Add a Ride Travel Info')

    return render(request, 'form.html', context)

    

def editRide(request, ride_id):

    if not request.session.get('loggedin', False):
        return redirect('signout')


    if not request.user.is_authenticated:
        return redirect("signin")

    if loggeduser(request.user).type != UserType.RIDER:
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

  

    if not request.session.get('loggedin', False):
        return redirect('signout')


    if not request.user.is_authenticated:
        return redirect("signin")

    rider = loggeduser(request.user)
    if loggeduser(request.user).type != UserType.RIDER:
        return HttpResponse('Not authorised to access this page')

    rides = RideTravelInfo.objects.filter(rider = rider)
   
    # for ride in rides:
    #     print(ride)
    #     rides['applications'] = Application.objects.filter(ride_travel_info = ride)

    print("ride_list", rides)
    
    # return HttpResponse(f'Ride Travel List {rides}')


    content = TemplateResponse(request, 'ride_list.html', {'ride_list': rides})
    print('home content', content, content.render())


    return render(request, 'ride_list.html', {'ride_list': rides, 'title': 'Ride List', 'loggedin':rider})

def allApplicants(request):
    if not request.session.get('loggedin', False):
        return redirect('signout')

    return HttpResponse('All Applicants')



def search(request):

    print("request.user.is_anonymous", request.user.is_anonymous)
    if not request.session.get('loggedin', False):
        return redirect('signout')
    form = AssetTransportRequestForm(request.POST)


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            data['requester'] = Requester.objects.get(user=request.user)
            print("valid form",data)

            search_request = AssetTransportationRequest.objects.create(**data)
            search_request.save()

            print("search_request", search_request.id)



            # print("search request saved", search_request)


            return redirect('match_rides', search_request.id)
        

    return render(request, 'form.html', {'form': form,  'title': 'Search', 'loggedin':loggeduser(request.user)})
def match_rides(request, request_id):


    if request.user.is_anonymous:
        return redirect('signout')
    if not request.user.is_authenticated:
        return redirect("signin")


    if loggeduser(request.user).type != UserType.REQUESTER:
        return HttpResponse('Not authorised to access this page')


    request_data = AssetTransportationRequest.objects.get(id=request_id)

    


    search_data = RideTravelInfo.objects.filter(from_location = request_data.from_location, assets_quanity__gte= request_data.assets_quanity).values()
    search_result = search_data
    print("search_data", search_data)


    applied_data = Application.objects.filter(applicant=Requester.objects.get(user=request.user))


    apps = {}
    for i in applied_data:
        apps[i.ride_travel_info.id] = i.status
    


    for data1 in search_result:
        data1['date_time'] = data1['date_time'].strftime("%d/%m/%Y, %H:%M %p")
        data1['rider'] = Rider.objects.get(id=data1['rider_id'])
        data1['apply_status'] = apps[data1['id']] if data1['id'] in apps else 'Apply'
        data1['asset_type'] = request_data.asset_type
        data1['asset_sensitivity'] = request_data.asset_sensitivity
        data1['whom_to_deliver'] = request_data.whom_to_deliver
        

    print("search result", search_result, "length", len(search_result))

            # print("data1", data1, "length ", len(data1))

    paginator = Paginator(search_result,1)
    # fetching the page no from url query parameter
    page = request.GET.get('page', 1)
    try:
        search_result = paginator.page(page)   
    except PageNotAnInteger:
        search_result = paginator.page(1)
    except EmptyPage:
        search_result = paginator.page(paginator.num_pages)

    

    # return HttpResponse(f'match rides {request_id}')

    return render(request, 'matched_rides.html', { 'title': 'Matched Rides', 'matched_transportation_requests':search_result, 'loggedin':loggeduser(request.user), 'request_id':request_id})



def ride_apply(request, ride_id):

    if not request.session.get('loggedin', False):
        return redirect('signout')
    if not request.user.is_authenticated:
        return redirect("signin")

    if loggeduser(request.user).type != UserType.REQUESTER:
        return HttpResponse('Not authorised to access this page')
    
    request_id = request.GET.get('request_id', 0)

    print("ride_apply: request_id", request_id)
    ride = RideTravelInfo.objects.get(id=ride_id)
    applicant = Requester.objects.get(user=request.user)
    print(ride)
    
    messages.success(request, "Asset Transport Request form saved")
    if request_id:
        application = Application.objects.create(applicant=applicant, assetTransportationRequest= AssetTransportationRequest.objects.get(id=request_id), ride_travel_info= ride)
        application.save()

        messages.success(request, "Application successfully applied")
    else:
        messages.warning(request, "Invalid request id")


    # return HttpResponse(f'Apply for Transportation Request {ride_id} {ride} {application}')
    return redirect('home')

