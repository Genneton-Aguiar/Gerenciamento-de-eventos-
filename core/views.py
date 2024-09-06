from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
)
from django.utils import timezone
from .models import (Events, Users, Inscription)
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
        
        name=request.data.get('name')
        is_istaff=request.data.get('is_staff')
        is_creator=request.data.get('is_creator')
        is_visitor=request.data.get('is_visitor')
        
        user = Users.objects.create(
            name = name,
            is_staff = is_istaff,
            is_creator = is_creator,
            is_visitor = is_visitor
            )
        
        if is_istaff==True and is_creator==True and is_visitor==True:
            return JsonResponse(
                'Escolha apenas um tipo de usuario',
                status = HTTP_400_BAD_REQUEST
                )
            
        serializer = self.get_serializer(user)
        headers = self.get_success_headers(serializer.data)
        
        return JsonResponse(
            serializer.data,
            status=HTTP_201_CREATED,
            headers=headers
            )
        
        
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    
    def list(self, request, *args, **kwargs):
        
#exibir os detalhes completos de um evento,incluindo os inscritos e informações adicioanais.

        events = Events.objects.all() 
        for event in events:
            inscritos = Inscription.objects.filter(
                is_active = True, 
                event = event ).count() 
        
                
        serializer = EventsSerializer(events,inscritos,many = True)   
        return JsonResponse(serializer.data, status = HTTP_200_OK)
    
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

        name=request.data.get('name')
        date_event=request.data.get('date_event')
        time_event=request.data.get('time_event')
        max_quantity=request.data.get('max_quantity')

        events = Events.objects.create(
            name = name,
            date_event = date_event,
            time_event = time_event,
            max_quantity = max_quantity,
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
        
        events = Events.objects.get(pk=pk)
        events.delete()
       
        return JsonResponse([], status=HTTP_204_NO_CONTENT)
    
    
class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    
    def list(self, request, *args, **kwargs):
        
        visitor = Events.objects.filter(user_type = 'visitante')
        if not visitor:
            return JsonResponse(
                    'somente o participante do evento pode acessar a \
                     lista de eventos que esta inscrito', 
                    status = HTTP_204_NO_CONTENT
                    )
        
        insc = Inscription.objects.all()
        serializer = InscriptionSerializer(insc, many = True)
        
        return JsonResponse(serializer.data, status = HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        
        data = request.data
        if not data:
            return JsonResponse(
                'informe os dados do evento',
                status = HTTP_400_BAD_REQUEST
                )
            
#Endpoint para que os usuários possam se inscrever em eventos, respeitando a capacidade máxima do evento

        event = Events.objects.get(pk = data['event'])
        user = Users.objects.get(pk = data['user'])
        
        iscription=Inscription.objects.create(
            event = event,
            user = user
        )
        if event.max_capacity > Events.objects(max_capacity=0):
                event.max_capacity = event.max_capacity - 1
                event.save()
        else:
                return JsonResponse(
                    'Desculpe, o evento esta lotado no momento.',
                    status = HTTP_409_CONFLICT
                )
        
        serializer = self.get_serializer(iscription)
        headers = self.get_success_headers(serializer.data)
        
        return JsonResponse(serializer.data, status = HTTP_201_CREATED, headers=headers)

    def cancel(self,id_event,id_inscription):
        
#Endpoint para que os usuários possam cancelar suas inscrições em eventos, 
#liberando vagas para outros interessados. 
#O cancelamento só poderá ser feito em até 24h antes da data de realização do evento.

        insc = Inscription.objects.get(pk = id_inscription)
        insc.is_active = False
        
        event = Events.objects.get(pk = id_event)
        event.max_capacity = event.max_capacity + 1
        
        if event.date - timezone.now() < timezone.timedelta(hours=24):
            return JsonResponse({
                'O cancelamento só pode ser feito com pelo menos 24 horas de antecedência.'
            }, status= HTTP_409_CONFLICT)
        
        insc.save()
        event.save()
        
        return JsonResponse('inscrção cancelada', status = HTTP_200_OK)


        
        