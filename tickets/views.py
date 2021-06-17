import json
from django.shortcuts import render
from django.http.response import Http404, JsonResponse
from rest_framework.response import Response
from tickets.models import *
from rest_framework.decorators import api_view
from tickets.serializers import *
from rest_framework import status, filters
from rest_framework.views import APIView
from django.http import Http404
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


@api_view(['GET', 'PUT', 'DELETE'])
# GET PUT=UPDATE DELETE
def fbv_pk(request, pk):

    try:
        guest = Guest.objects.get(pk = pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #Get
    if request.method == 'GET':
        serializer = GuestSerilaizer(guest)
        return Response(serializer.data)

    #PUT
    elif request.method == 'PUT':
        serializer = GuestSerilaizer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    #Delete
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


#Class based view
# List and Create
class Cbv_List(APIView):
    
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerilaizer(guests, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerilaizer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


#Class based view
# GET PUT DELETE
class Cbv_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk =pk)
        except Guest.DoesNotExist:
            raise Http404    

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerilaizer(guest)
        return Response(serializer.data)

    def put(self, request, pk):    
        guest = self.get_object(pk)
        serializer = GuestSerilaizer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     

        
