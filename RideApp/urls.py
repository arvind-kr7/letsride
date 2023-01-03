from django.urls import path

from . import views
urlpatterns =[
    path('', views.index, name='index'),
    path('search', views.search, name='search_ride'),

    ######################## USER MANAGEMENT #######################
    path('signup', views.signup, name="signup"),
    # path("signup", SignUpView.as_view(), name="signup"),

    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name='signout'),
    path('home/', views.home, name="home"),

    # REQUESTER
    path('match_rides/<int:request_id>', views.match_rides, name="match_rides"),
    path("ride_apply/<int:ride_id>/", views.ride_apply, name="ride_apply"),

    # RIDER
    path('add_ride/', views.addRide, name= 'add_ride' ),
    path('ride_list', views.rideList, name= 'ride_list' ),
    path("edit_ride/<int:ride_id>/", views.editRide, name="editRide"),
    path("all_applicants", views.allApplicants, name="allApplicants"),
    path("applications_received/<int:ride_id>/", views.applications_received, name="applications_received"),

]