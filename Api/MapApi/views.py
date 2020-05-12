from rest_framework.decorators import api_view
import json
from .models import Maps
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import mysql.connector

mydb = mysql.connector.connect(
    user='root',
    password="12345",
    host="localhost",
    database='maps')
cursor = mydb.cursor()


@api_view(["GET"])
def show_all_maps(request):
    try:
        cursor.execute('SELECT graph FROM map')
        res = cursor.fetchall()
        cursor.close()
        s = []
        for row in res:
            s.append(row)
        return JsonResponse('Maps: ' + str(s), safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def put_new_graph(new_graph):
    try:
        g = json.load(new_graph)
        json_obj = g["graph"]
        string_data = json.dumps(json_obj)
        cursor.execute("SELECT * FROM map")
        res = cursor.fetchall()
        Id = len(res) + 1
        # "INSERT INTO map(id, graph) VALUES ("+  str(c) + "," + str(g1) +")"
        cursor.execute("INSERT INTO map(id, graph) VALUES (" + str(Id) + "," + str(string_data) + ")")
        mydb.commit()
        return JsonResponse("Done", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
