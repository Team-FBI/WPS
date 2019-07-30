from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import MessageCreateView, ReservationViewSet

router = SimpleRouter()
router.register('', ReservationViewSet)

urlpatterns = [
    path('<int:pk>/message/', MessageCreateView.as_view()),
    path('', include(router.urls)),
]
