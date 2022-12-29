from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
# Create your models here.
import datetime
class UserType(models.TextChoices):
    REQUESTER = 'Requester', _('Requester')
    RIDER = 'Rider', _('Rider')
    
class TravelMedium(models.TextChoices):
    BUS = 'BUS', _('Bus')
    CAR = 'CAR', _('Car')
    TRAIN = 'TRAIN', _('Train')

class AssetType(models.TextChoices):
    LAPTOP = 'LAPTOP', _('Laptop')
    TRAVEL_BAG = 'TRAVEL_BAG', _('Travel Bag')
    PACKAGE = 'PACKAGE', _('Package')

class AssetSenstivity(models.TextChoices):
    HIGHLY_SENSITIVE = 'HIGHLY_SENSITIVE', _('Highly Sensitive')
    SENSITIVE = 'SENSITIVE', _('Sensitive')
    NORMAL = 'NORMAL', _('Normal')

class AppStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    CONFIRMED = 'CONFIRMED', _('Confirmed')
    EXPIRED = 'EXPIRED', _('Expired')

class Requester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=False, default='1234567890')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15)
    USERNAME_FIELD = 'email'


    def __str__(self):
        return self.name

class Rider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=False, default='1234567890')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15)
    USERNAME_FIELD = 'email'


    def __str__ (self):
        return self.name
    

class AssetTransportationRequest(models.Model):
    from_location = models.CharField(max_length=200)
    to_location = models.CharField(max_length=200)
    date_time = models.DateTimeField(default=datetime.datetime.now(),)
    flexible_timings = models.BooleanField(default=False)
    travel_medium = models.CharField(max_length=100, choices=TravelMedium.choices, default=TravelMedium.BUS)
    assets_quanity = models.IntegerField(default=1)
    asset_type = models.CharField(max_length=100, choices=AssetType.choices, default=AssetType.PACKAGE, help_text="Select asset type")
    asset_sensitivity = models.CharField(max_length=100, choices=AssetSenstivity.choices, default=AssetSenstivity.NORMAL, help_text="Select sensitivity")
    whom_to_deliver = models.CharField(max_length=400, help_text="Name - Mobile Number")

    def __str__ (self):
        return self.whom_to_deliver

class RideTravelInfo(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=200)
    to_location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    flexible_timings = models.BooleanField(default=False)
    travel_medium = models.CharField(max_length=100, choices=TravelMedium.choices, default=TravelMedium.BUS)
    assets_quanity = models.IntegerField(default=1)

    def __str__ (self):
        return self.rider.name

class Application(models.Model):
    applicant = models.ForeignKey(Requester, on_delete=models.CASCADE)
    assetTransportationRequest = models.ForeignKey(AssetTransportationRequest, on_delete=models.CASCADE)
    ride_travel_info = models.ForeignKey(RideTravelInfo, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=AppStatus.choices, default=AppStatus.PENDING)


    def __str__ (self):
        return self.status
