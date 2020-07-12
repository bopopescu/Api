from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "pw", "carModel", "startPoint", "endPoint", "x", "y", "z", "pos", "car_carID")


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ("numOfNodes",)


class EdgeEstimatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeEstimates
        fields = ("periodStart", "periodEnd", "numOfCars")




class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("edgeID", "distance", "avgSpeed")


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edges
        fields = ("edgeID", "firstNode", "secondNode", "distance", "width", "maxSpeed")
