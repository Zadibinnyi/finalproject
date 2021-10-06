from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib import messages

from datetime import date
from datetime import timedelta

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .forms import *


class SessionListView(ListView):
    model = Session
    queryset = Session.objects.filter(date=date.today())
    template_name = 'index.html'
    paginate_by = 2

    def get_success_url(self):
        return '/'.format(self.request.user.id)

    def get_ordering(self):
        sort_form = self.request.GET.get('sort_form')
        if sort_form == 'PriceLH':
            self.ordering = ['price']
        elif sort_form == 'PriceHL':
            self.ordering = ['-price']
        elif sort_form == "Time":
            print("I am here!")
            self.ordering = ['time_start']
        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = SortForm
        return context


class SessionTommorowListView(ListView):
    model = Session
    queryset = Session.objects.filter(date=date.today()+timedelta(1))
    template_name = 'tommorow.html'
    paginate_by = 2

    def get_success_url(self):
        return '/'.format(self.request.user.id)

    def get_ordering(self):
        sort_form = self.request.GET.get('sort_form')
        if sort_form == 'PriceLH':
            self.ordering = ['price']
        elif sort_form == 'PriceHL':
            self.ordering = ['-price']
        elif sort_form == "Time":
            print("I am here!")
            self.ordering = ['time_start']
        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = SortForm
        return context


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/'.format(self.request.user.id)


class Register(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class HallCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    form_class = HallCreateForm
    success_url = '/'
    template_name = 'create_hall.html'


class HallListView(ListView):
    model = Hall
    queryset = Hall.objects.all()
    template_name = 'hall.html'


class HallUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    template_name = 'update_hall.html'
    model = Hall
    fields = ['name', 'size']
    success_url = '/'


class SessionCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    form_class = SessionCreateForm
    success_url = '/'
    template_name = 'create_session.html'

    def form_valid(self, form):
        try:
            session = form.save(commit=False)
            session.save()
            return HttpResponseRedirect(self.get_success_url())
        except DateError:
            return messages.error(self.request, "Дата сеанса должна быть в рамках показа фильма")
        except SessionError:
            return messages.error(self.request, "В этом зале и на это время уже есть сеанс")
        finally:
            return redirect(f"/create_session/")

    def get_success_url(self):
        return "/".format(self.request.user.id)


class SessionAbout(DetailView):
    pk_url_kwarg = "pk"
    model = Session
    template_name = "session.html"
    extra_context = {"form": BuyForm}


class BuyTicket(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = BuyForm

    def form_valid(self, form):
        try:
            purchase = form.save(commit=False)
            purchase.user = self.request.user
            purchase.session = Session.objects.get(pk=self.kwargs["pk"])
            purchase.save()
            return HttpResponseRedirect(self.get_success_url())
        except NotZeroCount:
            return messages.error(self.request, "Заказ должень иметь хотя-бы один билет")
        except NotMuchCount:
            return messages.error(self.request, "В зале нет такого количества свободных мест")
        finally:
            return redirect(f"/session/about/{self.kwargs['pk']}")

    def get_success_url(self):
        return "/".format(self.request.user.id)


class FilmCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    form_class = FilmCreateForm
    success_url = '/'
    template_name = 'create_film.html'


class PurchaseView(ListView):
    model = Purchase
    template_name = 'purchase.html'


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    template_name = 'update_session.html'
    model = Session
    fields = ['film', 'hall', 'time_start', 'time_finish', 'date', 'price', ]
    success_url = '/'

    def form_valid(self, form):
        try:
            session = form.save(commit=False)
            session.save()
            return HttpResponseRedirect(self.get_success_url())
        except DateError:
            return messages.error(self.request, "Дата сеанса должна быть в рамках показа фильма")
        except SessionError:
            return messages.error(self.request, "В этом зале и на это время уже есть сеанс")
        finally:
            return redirect(f"/update_session/{self.kwargs['pk']}")

    def get_success_url(self):
        return "/".format(self.request.user.id)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = SelfToken.objects.get_or_create(user=user)
        return Response({'token': token.key})
