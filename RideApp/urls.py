from django.urls import path

from . import views
from .views import SignUpView
urlpatterns =[
    path('', views.index, name='index'),
    path('api2/', views.api, name='api'),
    path('search', views.search, name='search_ride'),

    ######################## USER MANAGEMENT #######################
    path('signup', views.signup, name="signup"),
    # path("signup", SignUpView.as_view(), name="signup"),

    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name='signout'),
    path('home/', views.home, name="home"),


    # RIDER
    path('add_ride/', views.addRide, name= 'add_ride' ),
    path('ride_list', views.rideList, name= 'ride_list' ),
    path("edit_ride/<int:ride_id>/", views.editRide, name="editRide"),
    path("all_applicants", views.allApplicants, name="allApplicants"),





    



    #  requester
    # path("requester_login/", views.requester_login, name="requester_login"),
    # path("signup/", views.signup, name="signup"),
    # path("requester_homepage/", views.requester_homepage, name="requester_homepage"),
    # path("logout/", views.Logout, name="logout"),
    # path("all_jobs/", views.all_jobs, name="all_jobs"),
    # path("job_detail/<int:myid>/", views.job_detail, name="job_detail"),
    path("ride_apply/<int:ride_id>/", views.ride_apply, name="ride_apply"),

    # # rider
    # path("rider_signup/", views.rider_signup, name="rider_signup"),
    # path("rider_login/", views.rider_login, name="rider_login"),
    # path("rider_homepage/", views.rider_homepage, name="rider_homepage"),
    # path("add_job/", views.add_job, name="add_job"),
    # path("job_list/", views.job_list, name="job_list"),
    # path("edit_job/<int:myid>/", views.edit_job, name="edit_job"),
    # path("rider_logo/<int:myid>/", views.rider_logo, name="rider_logo"),
    # path("all_applicants/", views.all_applicants, name="all_applicants"),

    # # admin
    # path("admin_login/", views.admin_login, name="admin_login"),
    # path("view_applicants/", views.view_applicants, name="view_applicants"),
    # path("delete_applicant/<int:myid>/", views.delete_applicant, name="delete_applicant"),
    # path("pending_companies/", views.pending_companies, name="pending_companies"),
    # path("accepted_companies/", views.accepted_companies, name="accepted_companies"),
    # path("rejected_companies/", views.rejected_companies, name="rejected_companies"),
    # path("all_companies/", views.all_companies, name="all_companies"),
    # path("change_status/<int:myid>/", views.change_status, name="change_status"),
    # path("delete_rider/<int:myid>/", views.delete_rider, name="delete_rider"),
]