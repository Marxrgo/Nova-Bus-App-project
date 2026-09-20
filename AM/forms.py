from django import forms
from .models import Bus
from datetime import time

#TODO: Review data validation if no csv/model of all buses

def time_choices(start = (8,40), end_hour = 10, step = 5):
    '''Helper function for BusStatusForm class'''
    out = [("", "Pick a time…")]
    minutes = start[0] * 60 + start[1]
    while minutes <= end_hour * 60:
        h, m = divmod(minutes, 60)
        out.append((f"{h:02d}:{m:02d}", f"{h % 12 or 12}:{m:02d} {'AM' if h < 12 else 'PM'}"))
        minutes += step
    return out #Returns a list of possible times for admin input (for dropdown purposes)

class BusStatusForm(forms.Form):
    bus = forms.IntegerField(min_value= 1000, max_value= 9999) #bus num input
    is_late = forms.BooleanField(required=False) 

    #Time= Dropdown or typed
    preset = forms.ChoiceField(choices= time_choices(), required= False)
    typed = forms.TimeField(required= False, widget= forms.TimeInput(attrs={"type": "time"}))


    def clean(self):
        '''Builds on data validation'''
        data = super().clean()
        preset, typed = data.get("preset"), data.get("typed")
        if preset and typed: #can only be for clean data
            raise forms.ValidationError("Use the dropdown or the typed time, not both.")
        
        if preset:
            h, m = map(int, preset.split(":"))
            data["time"] = time(h, m)
        else:
            data["time"] = typed   # may be None

        return data


    def clean_bus(self):
        '''Builds on bus input validation'''
        number = self.cleaned_data["bus"]
        try:
            return Bus.objects.get(number = number) #Checks if bus is in csv
        except Bus.DoesNotExist:
            raise forms.ValidationError(f"Bus {number} isn't in the system.")
