from django.db import models


class Map(models.Model):
    mapID = models.IntegerField(primary_key=True)
    numOfNodes = models.IntegerField()
    globalAvgSpeed = models.FloatField()

    class Meta:
        managed = False
        db_table = 'map'


class User(models.Model):
    userName = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'user'


class Edges(models.Model):
    edgeID = models.IntegerField(primary_key=True)
    firstNode = models.CharField(max_length=50)
    secondNode = models.CharField(max_length=50)
    distance = models.FloatField()
    width = models.FloatField()
    maxSpeed = models.FloatField()
    mapID = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'edges'


class Car(models.Model):
    carID = models.IntegerField(primary_key=True)
    curSpeed = models.FloatField()
    carModel = models.CharField(max_length=50)
    position = models.FloatField()
    userName = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    edgeID = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'car'


class EdgeEstimates(models.Model):
    id = models.AutoField(primary_key=True)
    periodStart = models.IntegerField()
    periodEnd = models.IntegerField()
    numOfCars = models.IntegerField()
    edgeID = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'edgeestimates'


class Trip(models.Model):
    tripID = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    isEnded = models.BooleanField()
    carID = models.IntegerField()
    routeDistance = models.FloatField()
    mapID = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trip'






class Route(models.Model):
    index = models.IntegerField(primary_key=True)
    tripID = models.IntegerField()
    edgeID = models.IntegerField()
    avgSpeed = models.FloatField()
    maxSpeed = models.FloatField()
    distance = models.FloatField()
    density = models.FloatField()
    time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'route'


class ActionValues(models.Model):
    actionValueID = models.IntegerField(primary_key=True)
    distance1 = models.FloatField()
    distance2 = models.FloatField()
    density1 = models.FloatField()
    density2 = models.FloatField()
    avgSpeed1 = models.FloatField()
    avgSpeed2 = models.FloatField()
    maxSpeed1 = models.FloatField()
    maxSpeed2 = models.FloatField()
    edgeValue = models.FloatField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'actionvalues'
