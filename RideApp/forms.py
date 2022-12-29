from django.forms import ModelForm
from .models import AssetTransportationRequest, RideTravelInfo
from crispy_forms.helper import FormHelper
import datetime
from django import forms

from .models import UserType, AppStatus



class AssetTransportRequestForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetTransportRequestForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = AssetTransportationRequest
        fields = "__all__"
        widgets= {
            'date_time' : forms.DateTimeInput(format=('%Y-%m,%H:%M'), attrs={'class':'myDateClass', 'type': 'datetime-local','placeholder':'Select a date', 'min':datetime.datetime.now()}),
            'assets_quanity': forms.NumberInput( attrs={'min':1})
        }


class AddRideForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddRideForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = RideTravelInfo
        fields = "__all__"
        exclude = ('rider', )
        widgets= {
            'date_time' : forms.DateTimeInput(format=('%d-%m-%Y'), attrs={'class':'myDateClass', 'type': 'datetime-local','placeholder':'Select a date'}),
            'assets_quanity': forms.NumberInput( attrs={'min':1})
        }


class SignupForm(forms.Form):
    
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    # We should use a validator to make sure 
    # the user enters a valid number format
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=UserType.choices)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    # We should use a validator to make sure 
    # the user enters a valid number format

class ApplicationStatusUpdateForm(forms.Form):
    application_id = forms.CharField(widget=forms.HiddenInput, required=False)
    status = forms.ChoiceField(widget=forms.Select, choices=AppStatus.choices, required=False)

                                                    