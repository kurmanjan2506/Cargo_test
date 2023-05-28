from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from geopy.distance import geodesic

from .models import Cargo, Location, Car
from .serializers import CargoSerializer, CarSerializer

class CargoListCreateAPIView(APIView):
    serializer_class = CargoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_location_by_zip(self, zip_code):
        '''Поиск локации по zip'''
        location = Location.objects.filter(zip=zip_code).first()
        if location:
            return f"{location.lat},{location.lng}"
        return None

    def get(self, request):
        cargos = Cargo.objects.all()
        serializer = self.serializer_class(cargos, many=True)
        cargo_data = serializer.data

        for cargo in cargo_data:
            pick_up_loc = cargo['pick_up_loc']
            delivery_loc = cargo['delivery_loc']
            nearby_cars_count = self.get_nearby_cars_count(pick_up_loc, delivery_loc)
            cargo['nearby_cars_count'] = nearby_cars_count

        return Response(cargo_data, status=status.HTTP_200_OK)

    def get_nearby_cars_count(self, pick_up_loc, delivery_loc):
        pick_up_lat, pick_up_lng = self.get_lat_lng_from_location(pick_up_loc)
        delivery_lat, delivery_lng = self.get_lat_lng_from_location(delivery_loc)

        nearby_cars = Car.objects.filter(curr_loc__isnull=False)
        nearby_cars_count = 0

        for car in nearby_cars:
            car_lat = float(car.curr_loc.lat)
            car_lng = float(car.curr_loc.lng)
            pick_up_distance = geodesic((pick_up_lat, pick_up_lng), (car_lat, car_lng)).miles
            delivery_distance = geodesic((delivery_lat, delivery_lng), (car_lat, car_lng)).miles

            if pick_up_distance <= 450 or delivery_distance <= 450:
                nearby_cars_count += 1

        return nearby_cars_count

    def get_lat_lng_from_location(self, location):
        loc = Location.objects.filter(zip=location).first()
        if loc:
            return float(loc.lat), float(loc.lng)
        return None, None

class CargoRetrieveUpdateDeleteAPIView(APIView):
    serializer_class = CargoSerializer

    def get(self, request, cargo_id):
        cargo = get_object_or_404(Cargo, id=cargo_id)
        serializer = self.serializer_class(cargo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, cargo_id):
        cargo = get_object_or_404(Cargo, id=cargo_id)
        serializer = self.serializer_class(cargo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cargo_id):
        cargo = get_object_or_404(Cargo, id=cargo_id)
        cargo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarUpdateAPIView(APIView):
    serializer_class = CarSerializer

    def put(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        serializer = self.serializer_class(car, data=request.data)
        if serializer.is_valid():
            zip_code = request.data.get('zip_code')
            location = self.get_location_by_zip(zip_code)
            if location:
                car.curr_loc = location
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_location_by_zip(self, zip_code):
        location = Location.objects.filter(zip=zip_code).first()
        return location
