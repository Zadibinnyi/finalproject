from django.contrib.auth.hashers import make_password

from cinema.models import *
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['username', 'password']

    def save(self, **kwargs):
        self.validated_data["password"] = make_password(self.validated_data["password"])
        return super().save()


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'session', 'quantity', ]


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['user', 'session', 'quantity', ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'sum', ]


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'size',]


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'name', 'date_start', 'date_finish',]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'film', 'hall', 'time_start', 'time_finish', 'date', 'quantity', 'price',]


class UpdateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['film', 'hall', 'time_start', 'time_finish', 'date', 'quantity', 'price',]

