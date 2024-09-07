from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
)

from django.utils import timezone
from .models import *
from .serializer import *


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def list(self, request, *args, **kwargs):
        
        user = Users.objects.all()
        serializer = UsersSerializer(user, many = True)
           
        return JsonResponse(serializer.data, status = HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        
#Implementar um cadastro de usuários básico, o usuário deve escolher entre usuário comum ou criador de eventos.
        data = request.data
        if not data:
            return JsonResponse(
                'informe os dados para criação do usuario',
                status = HTTP_400_BAD_REQUEST
                )
        
        name = request.data.get('name')
        is_creator = request.data.get('is_creator')
        is_visitor = request.data.get('is_visitor')
        
        if  is_creator == True and is_visitor == True:
            return JsonResponse(
                'Desculpe, o usuario pode ter apenas um unico tipo',
                status = HTTP_400_BAD_REQUEST
                )
            
        user = Users.objects.create(
            username = name,
            is_creator = is_creator,
            is_visitor = is_visitor
            )

        serializer = self.get_serializer(user)
        headers = self.get_success_headers(serializer.data)
        
        return JsonResponse(
            serializer.data,
            status = HTTP_201_CREATED,
            headers = headers
            )
        
        
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    
    def list(self, request, *args, **kwargs):
        
# exibir os detalhes completos de um evento,incluindo os inscritos e informações adicioanais.

        events = Events.objects.all()
        event_data = []
        
        for event in events:
            inscritos = Inscription.objects.filter(
                is_active=True, 
                event=event
                ).count()
            
            id= event.id

            event_data.append({
                'id': id,
                'name': event.name,
                'date': event.date,
                'local': event.local,
                'max_capacity': event.max_capacity,
                'is_active': inscritos,
                })

        serializer = EventsSerializer(event_data, many=True)
        return JsonResponse(serializer.data, status=HTTP_200_OK)
    
    def create(self, request, *args, **kwargs): 
        
        # ESTUDAR O DECORATOR 
        # METODO DE AUTENTICACAO JWT
        # SOMENTE O USUARIO CRIADOR PODE CRIAR O ENVENTO...
        
        
        data = request.data 
        if not data:
            return JsonResponse(
                'informe os dados do evento', 
                status = HTTP_400_BAD_REQUEST 
                )

        name_event = request.data.get('name')
        date_event = request.data.get('date')
        local_event = request.data.get('local')
        max_capacity = request.data.get('max_capacity')

        events = Events.objects.create(
            name = name_event,
            date = date_event,
            local= local_event,
            max_capacity = max_capacity,
        )
        
        serializer = self.get_serializer(events)
        headers = self.get_success_headers(serializer.data)
        
        return JsonResponse(serializer.data, status = HTTP_201_CREATED, headers=headers)
        
    def partial_update(self, request, pk): 
        
        try:
            events = Events.objects.get(pk=pk)
            data = request.data
            
            serializer = EventsSerializer(events, data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
                
        except Exception as e:
            return JsonResponse(e, status=400)
        
    def destroy(self, request, pk):    
        
        event = self.get_object()
        event.delete()
        
        return JsonResponse([], status=HTTP_204_NO_CONTENT)
    
    
class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    
    def list(self, request, *args, **kwargs):
        
        visitor = Users.objects.filter(is_visitor = True).first()
        if not visitor:
            return JsonResponse(
                    'somente o participante do evento pode acessar a \
                     lista de eventos que esta inscrito', 
                    status = HTTP_204_NO_CONTENT
                    )
        
        insc = Inscription.objects.all()
        serializer = InscriptionSerializer(insc, many = True)
        
        return JsonResponse(serializer.data, status = HTTP_200_OK)

    def create(self, request, ):
        
        data = request.data
        if not data:
            return JsonResponse(
                'informe os dados do evento',
                status = HTTP_400_BAD_REQUEST
                )
            
#Endpoint para que os usuários possam se inscrever em eventos, respeitando a capacidade máxima do evento

        events = Events.objects.get(pk = data['event'])
        users = Users.objects.get(pk = data['user'])
        
        #usuario inscrito no mesmo evento 
        same_insc = Inscription.objects.filter(event=events, user=users).first()
        if same_insc:
            return JsonResponse(
                'Você já está inscrito nesse evento.', 
                status = HTTP_400_BAD_REQUEST
                )
        
        #verificar se o evento ainda tem vagas
        if  events.max_capacity > 0:
            events.max_capacity -= 1
            events.save()
                
            iscription = Inscription.objects.create(
            event = events,
            user = users
            )
        
            serializer = self.get_serializer(iscription)
            headers = self.get_success_headers(serializer.data)
                
            return JsonResponse(
                'Inscrição realizada.',
                status = HTTP_201_CREATED,
                headers=headers
                )
        else:
                return JsonResponse(
                    'Desculpe, o evento esta lotado no momento.',
                    status = HTTP_409_CONFLICT
                )          
                
                
    def cancel (self,request, id_event,id_inscription):
        
#Endpoint para que os usuários possam cancelar suas inscrições em eventos, 
#liberando vagas para outros interessados. 
#O cancelamento só poderá ser feito em até 24h antes da data de realização do evento.
        
        inscription = Inscription.objects.get(pk = id_inscription)
        event = Events.objects.get(pk = id_event)
       
        limit = timezone.timedelta( hours = 24 )
        
        if event.date - timezone.now() < limit:
            return JsonResponse(
                'O cancelamento só pode ser feito com pelo menos\
                    24 horas de antecedência.', status=HTTP_409_CONFLICT)
            
        inscription.is_active = False
        event.max_capacity = event.max_capacity + 1
         
        inscription.save()
        event.save()
        
        return JsonResponse('Sua inscrção foi cancelada', status = HTTP_200_OK)
   

        
        