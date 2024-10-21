from django import forms
from .models import Plant,Tank
class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['id','name', 'plant_type', 'growth_phase', 'water_requirement', 'placement']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter the name', 'class': 'plant-selection-field name-input'}),
            'plant_type': forms.Select(attrs={'class': 'plant-selection-field plant-type-select'}),
            'growth_phase': forms.Select(attrs={'class': 'plant-selection-field growth-phase-select'}),
            'water_requirement': forms.Select(attrs={'class': 'plant-selection-field water-requirement-select'}),
            'placement': forms.Select(attrs={'class': 'plant-selection-field placement-select'}),
        }
class TankDepthForm(forms.Form):
    depth = forms.FloatField(label='Tank Depth')

class WateringOptionsForm(forms.Form):
    watering_options = forms.ChoiceField(
        choices=[('optimal', 'Optimal'), ('regular', 'Regular')],
        widget=forms.RadioSelect,
        
    )