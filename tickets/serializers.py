# Views <=Serializer=> Models
# Convert Data from ORM to JSON

from rest_framework import serializers
from tickets.models import *

class MovieSerilaizer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'


class ReservationSerilaizer(serializers.ModelSerializer):
    
    class Meta:
        model = Reservation
        fields = '__all__'


class GuestSerilaizer(serializers.ModelSerializer):
    
    class Meta:
        model = Guest
        fields = '__all__'        