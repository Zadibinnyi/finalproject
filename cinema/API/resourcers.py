from django.db.models import QuerySet
from datetime import date
from datetime import timedelta
from django.contrib import messages

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


from cinema.API.serializers import *


class RegisterAPI(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = Customer.objects.all()
    serializer_class = RegisterSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class BuyTicketViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    serializer_class = BuySerializer
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        try:
            serializer.user = self.request.user
            serializer.save()
        except NotZeroCount:
            raise exceptions.ValidationError("Заказ должень иметь хотя-бы один билет")
        except NotMuchCount:
            raise exceptions.ValidationError("В зале нет такого количества свободных мест")


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser, ]


class HallViewSet(viewsets.ModelViewSet):
    serializer_class = HallSerializer
    queryset = Hall.objects.all()
    permission_classes = [IsAdminUser, ]


class FilmViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    queryset = Film.objects.all()
    permission_classes = [IsAdminUser, ]


class SessionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = SessionSerializer
    queryset = Session.objects.filter(date=date.today())

    def get_queryset(self):
        queryset = super().get_queryset()
        hall = self.request.query_params.get('hall')
        start = self.request.query_params.get('start')
        finish = self.request.query_params.get('finish')

        if start and finish and hall:
            queryset = queryset.filter(hall__name=hall, time_start__range=(start, finish))
        elif start and finish:
            queryset = queryset.filter(time_start__range=(start, finish))
        elif hall:
            queryset = queryset.filter(hall__name=hall)
        return queryset


class TommorowSessionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = SessionSerializer
    queryset = Session.objects.filter(date=date.today() + timedelta(1))

    def get_queryset(self):
        queryset = super().get_queryset()
        hall = self.request.query_params.get('hall')
        start = self.request.query_params.get('start')
        finish = self.request.query_params.get('finish')

        if start and finish and hall:
            queryset = queryset.filter(hall__name=hall, time_start__range=(start, finish))
        elif start and finish:
            queryset = queryset.filter(time_start__range=(start, finish))
        elif hall:
            queryset = queryset.filter(hall__name=hall)
        return queryset


class SessionCreateViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'put', 'patch']
    serializer_class = UpdateSessionSerializer
    queryset = Session.objects.all()
    permission_classes = [IsAdminUser, ]

    def perform_create(self, serializer):
        try:
            session = serializer.save()
            session.save()
        except DateError:
            raise exceptions.ValidationError('Дата сеанса должна быть в рамках показа фильма')
        except SessionError:
            raise exceptions.ValidationError('В этом зале и на это время уже есть сеанс')

    def perform_update(self, serializer):
        try:
            session = serializer.save()
            session.save()
        except DateError:
            raise exceptions.ValidationError('Дата сеанса должна быть в рамках показа фильма')
        except SessionError:
            raise exceptions.ValidationError('В этом зале и на это время уже есть сеанс')



