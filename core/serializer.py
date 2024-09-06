from rest_framework import serializers
from .models import * 

class UsersSerializer (serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'is_staff', 'is_visitor', 'is_criador')
        
class EventsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('name', 'date', 'local', 'max_capacity')

class InscriptionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ('event', 'user', 'is_active', 'reason')

