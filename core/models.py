from django.db import models
from django.contrib.auth.models import User


class Users (User):
    
    is_creator = models.BooleanField(
        verbose_name = 'criador',
        default = False
    )
    is_visitor = models.BooleanField(
        verbose_name = 'visitante',
        default = False
    )
    
    
class Events (models.Model):  
    
    name = models.CharField(
        verbose_name = 'nome do evento',
        max_length = 100
    )
    description = models.CharField(
        verbose_name = 'descrição do evento',
        max_length = 200
    )
    date = models.DateTimeField(
        verbose_name = 'data do evento',
    )
    local = models.CharField(
        verbose_name = 'local do evento',
        max_length = 100
    )
    max_capacity = models.IntegerField(
        verbose_name = 'capacidade maxima',
    )
    
    def __str__(self):
        return self.name

    
class Inscription (models.Model):
    
    event = models.ForeignKey(
        Events, 
        verbose_name = 'evento',
        on_delete = models.DO_NOTHING,  
    ) 
    user = models.ForeignKey(
        Users, 
        verbose_name = 'usuario',
        on_delete = models.DO_NOTHING,
    )
    is_active  = models.BooleanField(
        verbose_name = 'Ativo',
        default = True
    )
    reason = models.CharField(
        verbose_name = 'motivo do cancelamento',
        max_length = 100,
        null = True,
        blank = True
    )
    
    def __str__(self):
        return self.event.name
    
