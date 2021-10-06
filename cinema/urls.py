from cinema.API.resourcers import *
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'hall', HallViewSet)
router.register(r'purchase', PurchaseViewSet)
router.register(r'session', SessionViewSet)
router.register(r'session_tommorow', TommorowSessionViewSet)
router.register(r'create_update_session', SessionCreateViewSet)
router.register(r'film', FilmViewSet)
router.register(r'buy_ticket', BuyTicketViewSet)
router.register(r'register', RegisterAPI)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SessionListView.as_view(), name='index'),
    path('tomorrow/', SessionTommorowListView.as_view(), name='tomorrow'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('hall/', HallListView.as_view(), name='hall'),
    path('create_hall/', HallCreateView.as_view(), name='create_hall'),
    path("hall/<int:pk>/", HallUpdateView.as_view(), name='update_hall'),
    path('create_session/', SessionCreateView.as_view(), name='create_session'),
    path("session/about/<int:pk>/", SessionAbout.as_view(), name="about"),
    path("session/buy/<int:pk>", BuyTicket.as_view(), name="buy_ticket"),
    path('create_film/', FilmCreateView.as_view(), name='create_film'),
    path('purcase/', PurchaseView.as_view(), name='purchase_user'),
    path('update_session/<int:pk>/', SessionUpdateView.as_view(), name='update_session'),
    path('api/', include(router.urls)),
    path('api-auth/', CustomAuthToken.as_view())
]