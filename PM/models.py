from django.db import models

# Create your models here.

#

class Looptype(models.TextChoices): #Does not go into DB ; just used for loop choices(either MUSIC or IB)
    MUSIC = 'MUSIC', 'Music Loop'
    IB = 'IB', 'IB Loop'

# Creates DB ; variable names are the columns ; column data validation is inheritated from djangos own database class
## This busSlot class is an extention of django's database class template.
class BusSlot(models.Model):
    loop = models.CharField(max_length=10,choices= Looptype.choices) 
    slot_number = models.PositiveIntegerField(help_text="Slot position, e.g 1 to 15") #TODO change this to correct slots when template is done

    bus_number = models.PositiveIntegerField( #e.g 2256
        null = True,
        blank = True,
        help_text= "Current bus number assigned to this slot.")

    last_updated = models.DateTimeField(auto_now=True)

    class Meta: #django specific formating for DB
        db_table = 'Bus_slot_tracking' #Database name
        verbose_name = 'bus_slot_tracking'
        verbose_name_plural = 'Bus Slot Tracking Database'

        ordering = ['loop','slot_number']
        unique_together = ('loop', 'slot_number')

    def __str__(self):
        bus = f"Bus #{self.bus_number}" if self.bus_number else "Empty"
        return f"Slot {self.slot_number}: {bus}"

    #
    