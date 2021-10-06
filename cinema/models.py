from django.contrib.auth.models import AbstractUser
from django.db import models

from cinema.exception import NotZeroCount, NotMuchCount, DateError, SessionError

from rest_framework.authtoken.models import Token


class Customer(AbstractUser):
    sum = models.IntegerField(default=0)


class Hall(models.Model):
    name = models.CharField(max_length=120)
    size = models.IntegerField()

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=120)
    date_start = models.DateField()
    date_finish = models.DateField()

    def __str__(self):
        return self.name


class Session(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='film')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='hall')
    time_start = models.TimeField()
    time_finish = models.TimeField()
    date = models.DateField()
    quantity = models.PositiveIntegerField(default=None)
    price = models.IntegerField()

    def save(self, *args, **kwargs):
        if not (self.date >= self.film.date_start and self.date <=self.film.date_finish):
            raise DateError()
        elif self.quantity == None or self.quantity >= self.hall.size:
            self.quantity = self.hall.size
            super(Session, self).save(*args, **kwargs)
        elif Session.objects.filter(hall=self.hall.pk, date=self.date, time_start__lte=self.time_start, time_finish__gte=self.time_start):
            if str(self.pk) in str(Session.objects.filter(hall=self.hall.pk, date=self.date, time_start__lte=self.time_start, time_finish__gte=self.time_start).values('id')):
                super(Session, self).save(*args, **kwargs)
            else:
                raise SessionError()
        else:
            super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.film} in {self.hall}, {self.date}, {self.time_start}"


class Purchase(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session')
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            raise NotZeroCount("Заказ должень иметь хотя-бы одну позицию")
        elif self.quantity > self.session.quantity or (self.session.quantity - self.quantity) < 0:
            raise NotMuchCount("У нас недостаточно мест")
        elif self.session.quantity >= self.quantity:
            self.user.sum += self.session.price * self.quantity
            self.user.save()
            self.session.quantity -= self.quantity
            self.session.save()
            super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.session.film} from {self.user}"


class SelfToken(Token):
    last_active = models.DateTimeField(null=True, blank=True)