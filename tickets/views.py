import json
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http.response import Http404, JsonResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from tickets.models import *
from rest_framework.decorators import api_view
from tickets.serializers import *
from rest_framework import status, filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import *

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


#Mixins List                                                             #Response by Api
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerilaizer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


#Mixins GET PUT DELETE
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerilaizer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


#Generics GET POST
class Genericslist(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerilaizer
    authentication_classes = [TokenAuthentication]

    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

#Generics GET PUT DELETE
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerilaizer
    authentication_classes = [TokenAuthentication]

    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

#ViewSets 
class View_sets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerilaizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class View_sets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerilaizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']


class View_sets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerilaizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['guest']

# *-----------------------------------------------*
#Using in Postman only
#Find Movie by fbv
@api_view(['GET'])
def find_movie(request):

    movies = Movie.objects.filter(
        movie_name = request.data['movie_name'], 
        hall = request.data['hall'],
        )
    serializer = MovieSerilaizer(movies, many = True)
    return Response(serializer.data)    

#Create new reservation
@api_view(['POST'])
def new_reservation(request):
    
    movie = Movie.objects.get(
        movie_name = request.data['movie_name'], 
        hall = request.data['hall'],
        )
    #New guest
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    
    serializer = GuestSerilaizer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

#Post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#JWT AUTH TOKEN  