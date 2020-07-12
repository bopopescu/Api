from rest_framework.decorators import api_view
import json
from django.db.models import Sum, Avg
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import mysql.connector
from rest_framework import generics
from .models import *
from .serializers import *
import itertools




@api_view(["GET"])
def getEdgeAvgSpeed(data):
    try:
        edgeID = data.GET.get('edgeID')

        # "select avg(curSpeed) from car where edgeID = edgeID;"


        return JsonResponse("avgSpeed", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def updateGlobalAvgSpeed(data):
    try:
        newValue = int(data.GET.get('newSpeed'))
        num_of_trips = Trip.objects.all().count()
        tripid = int(data.GET.get('tripID'))
        tripData = Trip.objects.filter(tripID=tripid)
        mapid = tripData[0].mapID
        mapData = Map.objects.filter(mapID=mapid)
        oldspeed = mapData[0].globalAvgSpeed
        newspeed = (oldspeed * (1 - (1 / num_of_trips))) + (newValue * (1 / num_of_trips))
        #mapData[0].globalAvgSpeed = newspeed
        m = Map.objects.get(mapID=mapid)
        m.globalAvgSpeed = newspeed
        m.save()
        return JsonResponse("Done", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def getGlobalAvgSpeed(data):
    try:
        tripid = int(data.GET.get('tripID'))
        tripData = Trip.objects.filter(tripID=tripid)
        mapid = tripData[0].mapID
        globalavgSpeed = Map.objects.filter(mapID=mapid)[0].globalAvgSpeed


        return JsonResponse(globalavgSpeed, safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def updateTripRoute(data):
    try:
        delete = data.GET.get('delete')
        tripID = data.GET.get('tripID')
        add = data.GET.get('add')
        #t = delete['test']
        # "select avgSpeed, maxSpeed from route where tripID = tripID;"

        return JsonResponse(delete, str(type(delete)), safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def getTripRoute(data):
    try:
        tripid = int(data.GET.get('tripID'))
        edgeid = int(data.GET.get('edgeID'))
        routeData = Route.objects.filter(tripID=tripid, edgeID=edgeid)
        idx = routeData[0].index
        routeData2 = Route.objects.filter(index__gt=idx, tripID=tripid)
        serializer = RouteSerializer(routeData2, many=True)

        return JsonResponse(serializer.data, safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def getEdgeEstimates(data):
    try:
        edgeID = data.GET.get('edgeID')
        # "select periodStart, periodEnd, numOfCars from edgeestimates where edgeID = edgeID;"


        return JsonResponse("NOMAP", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def updateEdgeEstmates(data):
    try:
        EdgeEstmates = json.load(data)
        for i in EdgeEstmates:
            edgeid = int(i['edgeID'])
            pstart = int(i['periodStart'])
            pend = int(i['periodEnd'])
            value = int(i['addedValue'])
            estimateData = EdgeEstimates.objects.filter(edgeID=edgeid, periodStart=pstart, periodEnd=pend)
            if estimateData.count() > 0:
                estimateData2 = EdgeEstimates.objects.get(edgeID=edgeid, periodStart=pstart, periodEnd=pend)
                newvlue = estimateData2.numOfCars + value
                estimateData2.numOfCars = newvlue
                estimateData2.save()

        return JsonResponse("Done", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def put_new_graph(new_graph):
    try:
        x = new_graph.GET.get('mapJson', 'WrongKey')
        # x = request.['LoginData']
        if str(x).__eq__('WrongKey'):
            return JsonResponse('WrongKey', safe=False)
        else:


            return JsonResponse("Done", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def registration(data):
    try:
        x = data.GET.get('RegData')
        mapid = int(data.GET.get('mapID'))
        # x = request.['LoginData']
        j = json.loads(x)
        name = j["name"]
        pw = j["pw"]
        carmodel = j["carModel"]

        test = User.objects.filter(userName=name)
        if not (test.exists()):
            newUser = User(userName=name, password=pw)
            newUser.save()
            c = Car.objects.all()
            if c.count() == 0:
                oldid = 1
            else:
                oldid = c[0].carID + 1
            e = Edges.objects.get(firstNode='A', secondNode='B')

            edgeid = e.edgeID
            e.mapID = mapid
            newcar = Car(carID=oldid, curSpeed=0, carModel=carmodel, position=0, userName=name, x=125.1969,
                         y=3.293157e-06, z=-201.3321, edgeID=edgeid)
            newcar.save()

            res = {'carModel': carmodel,
                   'mapID': mapid,
                   'carInfo': {
                       'name': name,
                       'pw': pw,
                       "startPoint": e.firstNode,
                       "endPoint": e.secondNode,
                       "x": 125.1969,
                       "y": 3.293157e-06,
                       "z": -201.3321,
                       "pos": 0,
                   }}

            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("existed", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def trip_initiation(trip_data):
    try:
        carid = trip_data.GET.get('carID')
        destinat = trip_data.GET.get('destination')
        mapid = trip_data.GET.get('mapID')
        newTrip = Trip(carID=carid, destination=destinat, mapID=mapid, isEnded=False, routeDistance=0, time=None)
        newTrip.save()
        tripid = newTrip.tripID
        return JsonResponse(tripid, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getCarData(data):
    try:
        carID = data.GET.get('carID')
        curSpeed = data.GET.get('curSpeed')
        jsonParam = data.GET.get('jsonParam')
        j = json.loads(jsonParam)
        sp = j["startPoint"]
        ep = j["endPoint"]
        xp = j["x"]
        yp = j["y"]
        zp = j["z"]
        pos = j["pos"]



        return JsonResponse(to_json(), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def to_json():
            return {
                "velocity": "maxSpeed",
                "acceleration": 8
        }


@api_view(["GET"])
def login(request_data):
    try:
        x = request_data.GET.get('loginData')
        # x = request.['LoginData']
        j = json.loads(x)
        name = j["name"]
        pw = j["pw"]
        test = User.objects.filter(userName=name, password=pw)
        if test.exists():
            uName = test[0].userName
            p = test[0].password
            cardata = Car.objects.filter(userName=uName)
            x = cardata[0].x
            y = cardata[0].y
            z = cardata[0].z
            pos = cardata[0].position
            edgeid = cardata[0].edgeID
            carmodel = cardata[0].carModel
            mapid = Edges.objects.get(edgeID=edgeid).mapID
            edge = Edges.objects.filter(edgeID=edgeid)
            fnode = edge[0].firstNode
            snode = edge[0].secondNode
            res = {'carModel': carmodel,
                   'mapID': mapid,
                   'CarInfo': {
                       'name': uName,
                       'pw': p,
                       "startPoint": fnode,
                       "endPoint": snode,
                       "x": x,
                       "y": y,
                       "z": z,
                       "pos": pos,
                   }}

            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("wrongLoginInfo", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def car_information(data):
    try:
        update_data = json.load(data)
        first_end = update_data["first_end"]
        second_end = update_data["second_end"]
        car_id = update_data["car_id"]
        return JsonResponse("Done", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)




def instruction_update(data):
    try:
        update_data = json.load(data)
        first_end = update_data["first_end"]
        second_end = update_data["second_end"]
        trip_id = update_data["trip_id"]
        rout = ["A", "B", "C", "D"]
        return JsonResponse(rout, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


# return all maps
class ListMaps(generics.ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

def trip_report(data):
    try:
        update_data = json.load(data)
        trip_id = update_data["trip_id"]
        time = data["date"]
        return JsonResponse("Done", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


''' test of getRoute
        {
            "mapID":"re",
            "startPoint":"A",
            "endPoint":"G",
            "tripID":"12"
        }
        '''


@api_view(["GET"])
def get_route(data):
    try:
        d = json.load(data)
        mapid = d["mapID"]
        sp = d["startPoint"]
        ep = d["endPoint"]
        tid = d["tripID"]

        return JsonResponse(mapid + sp + ep + tid, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

        ''' test of update_action_value_car
        {
            "tripID":"12",
            "time":"12:00",
            "distance":"0.9",
            "density":"0.9"
        }
        '''


@api_view(["GET"])
def update_action_value_car(data):
    try:
        dens = float(data.GET.get("density"))
        dist = float(data.GET.get("distance"))
        time = data.GET.get("time")
        tid = int(data.GET.get("tripID"))
        isended = data.GET.get("isended")

        print(type(dist))
        return JsonResponse(dist, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST) @ api_view(["GET"])


''' test of add trip
{
    "mapID":"23",
    "CarID":"essam",
    "startPoint":12.0,
    "endPoint":13.0
}
'''

@api_view(["GET"])
def add_trip(data):
    try:
        mapid = int(data.GET.get("mapID"))
        carid = int(data.GET.get("carID"))
        trip = Trip(time="00:00", isEnded=False, carID=carid, routeDistance=0, mapID=mapid)
        trip.save()
        return JsonResponse(trip.tripID, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
''' test of get_map
{
    "mapID":"12"
}
'''



@api_view(["GET"])
def get_map(data):
    try:
        tripid = int(data.GET.get('tripID'))
        carid = int(data.GET.get('carID'))
        edgeid = Car.objects.get(carID=carid).edgeID
        position = Edges.objects.get(edgeID=edgeid).secondNode
        tripData = Trip.objects.get(tripID=tripid)
        mapid = tripData.mapID
        destination = tripData.destination
        map = Map.objects.filter(mapID=mapid)
        mapserializer = MapSerializer(map, many=True)
        mapserializer.data[0]['destination'] = destination
        mapserializer.data[0]['position'] = position
        edges = Edges.objects.filter(mapID=mapid)
        serializer = EdgeSerializer(edges, many=True)
        for i in serializer.data:
            eID = i['edgeID']
            edgesEstimates = EdgeEstimates.objects.filter(edgeID=eID)
            serializeredgeEstimate = EdgeEstimatesSerializer(edgesEstimates, many=True)
            print(serializeredgeEstimate.data)
            cars = Car.objects.filter(edgeID=eID)
            numOfCars = cars.count()
            avg = Car.objects.filter(edgeID=eID).aggregate(Avg('curSpeed'))['curSpeed__avg']
            distance = i['distance']
            width = i['width']
            density = float(numOfCars / (distance * width))
            i["density"] = density
            i["avgSpeed"] = avg
            print(serializeredgeEstimate.data)
            i["EdgeEstimates"] = serializeredgeEstimate.data
        mapserializer.data[0]["Edges"] = serializer.data
        return JsonResponse(mapserializer.data, safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def select_av_speed(data):
    try:
        edgeID = int(data.GET.get('edgeID'))
        return JsonResponse("av_speedx", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def update_av_speed(data):
    try:
        new_value = float(data.GET.get("newspeed"))

        return JsonResponse("Done" + str(new_value), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def select_action_value(data):
    try:
        density = float(data.GET.get("density"))
        distance = float(data.GET.get("distance"))
        av_speed = float(data.GET.get("avgSpeed"))
        max_speed = float(data.GET.get("maxSpeed"))
        actionValueData = ActionValues.objects.get(distance1__lte=distance, distance2__gte=distance,
                                                   density1__lte=density, density2__gte=density,
                                                   avgSpeed1__lte=av_speed, avgSpeed2__gte=av_speed,
                                                   maxSpeed1__lte=max_speed, maxSpeed2__gte=max_speed)

        if actionValueData is not None:
            return JsonResponse(actionValueData.edgeValue, safe=False)
        else:
            return JsonResponse(None, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


'''
{
    "distance":"12",
    "density":"2",
    "avspeed":"20",
    "maxspeed":"90"
}
'''
@api_view(["GET"])
def update_action_value_db(data):
    try:
        density = float(data.GET.get("density"))
        distance = float(data.GET.get("distance"))
        av_speed = float(data.GET.get("avgSpeed"))
        max_speed = float(data.GET.get("maxSpeed"))
        newvalue = float(data.GET.get("newValue"))
        actionValueData = ActionValues.objects.get(distance1__lte=distance, distance2__gte=distance, density1__lte=density, density2__gte=density, avgSpeed1__lte=av_speed, avgSpeed2__gte=av_speed, maxSpeed1__lte=max_speed, maxSpeed2__gte=max_speed)
        oldvalue = actionValueData.edgeValue
        n = actionValueData.count
        newValue = (oldvalue * (1 - (1 / n))) + (newvalue * (1 / n))
        actionValueData.edgeValue = newValue
        actionValueData.save()

        return JsonResponse("Done", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getEdgeInfo(data):
    try:
        tripid = int(data.GET.get('tripID'))
        fNode = data.GET.get('firstNode')
        sNode = data.GET.get('secondNode')
        time = int(data.GET.get('time'))
        edgeData = Edges.objects.get(firstNode=fNode, secondNode=sNode)
        edgeid = edgeData.edgeID
        routeData = Route.objects.get(tripID=tripid, edgeID=edgeid)

        routeData.time = time

        res= {
            "distance": routeData.distance,
            "density": routeData.density,
            "avgSpeed": routeData.avgSpeed,
            "maxSpeed": routeData.maxSpeed
        }
        routeData.save()
        return JsonResponse(res, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def getTripSpeed(data):
    try:
        tripid = int(data.GET.get('tripID'))
        distance = Route.objects.filter(tripID=tripid).aggregate(Sum('distance'))['distance__sum']
        time = Route.objects.filter(tripID=tripid).aggregate(Sum('time'))['time__sum']
        if distance is None:
            return JsonResponse("WrongTripID", safe=False)
        else:
            speed = float(distance) / float(time)
            return JsonResponse(speed, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def update_action_values_for_all_trip(data):
    try:
        tripid = int(data.GET.get('tripID'))
        newvalue = float(data.GET.get("newValue"))
        routeData = Route.objects.filter(tripID=tripid)
        print(routeData)
        for i in routeData:
            distance = i.distance
            density = i.density
            maxspeed = i.maxSpeed
            avgspeed = i.avgSpeed
            actionValueData = ActionValues.objects.get(distance1__lte=distance, distance2__gte=distance,
                                                       density1__lte=density, density2__gte=density,
                                                       avgSpeed1__lte=avgspeed, avgSpeed2__gte=avgspeed,
                                                       maxSpeed1__lte=maxspeed, maxSpeed2__gte=maxspeed)
            oldvalue = actionValueData.edgeValue
            n = actionValueData.count
            actionvalueid = actionValueData.actionValueID
            s = ActionValues.objects.get(actionValueID=actionvalueid)
            newValue = (oldvalue * (1 - (1 / n))) + (newvalue * (1 / n))
            s.edgeValue = newValue
            s.count += 1
            s.save()
        return JsonResponse("Done", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def insertedgeestimat(data):
    try:
        actionv = json.load(data)
        for i in actionv:
            aid = int(i['actionValueID'])
            d1 = float(i['distance1'])
            d2 = float(i['distance2'])
            de1 = float(i['density1'])
            de2 = float(i['density2'])
            av1 = float(i['avgSpeed1'])
            av2 = float(i['avgSpeed2'])
            m1 = float(i['maxSpeed1'])
            m2 = float(i['maxSpeed2'])
            n = float(i['count'])
            actionvlueData = ActionValues(actionValueID=aid, distance1=d1, distance2=d2, density1=de1, density2=de2,
                                          avgSpeed1=av1, avgSpeed2=av2, maxSpeed1=m1, maxSpeed2=m2,
                                          count=n)
            actionvlueData.save()

        return JsonResponse("Done", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def test(data):
    try:
        c = ActionValues.objects.all().count()
        return JsonResponse(c, safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def moveTOnode(data):
    try:
        carid = int(data.GET.get("carID"))
        carData = Car.objects.get(carID=carid)
        curspeed = float(data.GET.get("curSpeed"))
        carData.curSpeed = curspeed
        jsonParam = data.GET.get("jsonParam")
        js = json.loads(jsonParam)
        s = js[0]
        e = js[1]
        x = js[2]
        y = js[3]
        z = js[4]
        p = js[5]
        sp = s["startPoint"]
        ep = e["endPoint"]
        xp = x["x"]
        yp = y["y"]
        zp = z["z"]
        pos = p["pos"]
        carData.x = xp
        carData.y = yp
        carData.z = zp
        carData.position = pos
        edgeid = carData.edgeID
        edgeData = Edges.objects.get(edgeID=edgeid)
        edgeData.firstNode = sp
        edgeData.secondNode = ep
        carData.save()
        edgeData.save()
        res = {
            "velocity": edgeData.maxSpeed,
            "acceleration": 8
        }

        return JsonResponse(res, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def put_new_map(data):
    try:
        m_json = json.load(data)
        for i in m_json['graph']:
            fnode = i['node']
            neighbours = i['neighbours']
            for n in neighbours:
                eid = Edges.objects.all().count()
                snode = n['node']
                distance = float(n['weight'])
                edge = Edges(edgeID=eid+1, firstNode=fnode, secondNode=snode, distance=distance, maxSpeed=10, width=8, mapID=2)
                edge.save()

        return JsonResponse("Done", safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
