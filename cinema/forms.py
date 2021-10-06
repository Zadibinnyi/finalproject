from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class Registration(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class HallCreateForm(ModelForm):

    class Meta:
        model = Hall
        fields = ['name', 'size',]


class SessionCreateForm(ModelForm):

    class Meta:
        model = Session
        fields = ['film', 'hall', 'time_start', 'time_finish', 'date', 'price',]


class FilmCreateForm(ModelForm):

    class Meta:
        model = Film
        fields = ['name', 'date_start', 'date_finish',]


class BuyForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity',]


class SortForm(forms.Form):
    sort_form = forms.TypedChoiceField(label='Sorted ', choices=[('Time', 'By start time'), \
        ('PriceLH', 'Low to high'),('PriceHL', 'High to Low')])