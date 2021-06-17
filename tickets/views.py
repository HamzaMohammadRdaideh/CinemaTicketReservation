import json
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from tickets.models import *
from rest_framework.decorators import api_view
from tickets.serializers import *
from rest_framework import status, filters
# List = Get , Create = Post ,PK query = Get , Update = PUT , Delete or Destroy = Delete

# Extract JSON data without restframework and query model
def without_restframework(request):
    guests = [
        {
            'id':1,
            'name':'Ahmad',
            'mobile': 790790790,
        },
        {
            'id':2,
            'name':'Salah',
            'mobile': 880790790,
            }
    ]
    return JsonResponse(guests,safe=False)


# Extract JSON data without restframework but using model
def by_model(request):
    data = Guest.objects.all()
    response = {
        'guests':list(data.values())
    }
    return JsonResponse(response)


# Function Based View , Get Post @api_view() from rest_framework
@api_view(['GET' ,'POST'])
# Get and Post
def fbv_list(request):

    #Get
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerilaizer(guests,many=True)
        return Response(serializer.data)
    #Post
    elif request.method == 'POST':
        serializer = GuestSerilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)    