from django.urls import path, include

from .views import CargoListCreateAPIView, CargoRetrieveUpdateDeleteAPIView, CarUpdateAPIView

urlpatterns = [
    path('cargo/', CargoListCreateAPIView.as_view()),
    path('cargo/<int:cargo_id>/', CargoRetrieveUpdateDeleteAPIView.as_view()),
    path('cars/<int:car_id>/', CarUpdateAPIView.as_view(), name='car-update'),
]

