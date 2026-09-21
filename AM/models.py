from django.core.validators import MinLengthValidator , MaxLengthValidator
from django.db import models
from django.utils import timezone

# Create your models here.

class Bus(models.Model):
    number = models.PositiveIntegerField( 
        unique= True, 
        validators= [MinLengthValidator(1000),MaxLengthValidator(9999)]) #Bus number validation

    class Meta:
        ordering = ["number"]
        verbose_name_plural = "buses"

    def __str__(self):
        return f"Bus {self.number}"


class BusStatus(models.Model):
    #related_name lets acess to records by calling i.e bus.statuses.all()
    #Forein key litterally calles the Bus class/model above^^^
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name= "statuses") #on delete means if bus column is deleted the whole row is deleted
    date = models.DateField(default = timezone.localdate)
    is_late = models.BooleanField(default= False) #If bus is late
    arrived_time = models.TimeField(null = True, blank= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        '''This class orders data by date and bus number ; Prevents duplicate bus number entries in same day'''
        verbose_name_plural = "bus statuses"
        ordering = ["date", "bus__number"]
        constraints = [
            models.UniqueConstraint(fields = ["bus", "date"], name = "Unique_bus_per_day")
        ]

    @property #lets this function acess class vars
    def arrived(self):
        return self.arrived_time is not None #Returns true if its not empty or Null/None

    @classmethod
    def status_for(cls ,bus, date = None):
        return cls.objects.filter(bus = bus, date = date or timezone.localdate()).first()


