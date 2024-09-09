from rest_framework import serializers
from .models import * 

class UsersSerializer (serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','username', 'is_visitor', 'is_creator')
        
class EventsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id','name','description','start_date','end_date',
                  'local','max_capacity')
                  
class InscriptionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ('id','event', 'user', 'is_active')

