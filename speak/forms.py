from django import forms
from .models import Age, Ethnic, Dialect, Gender

GENDER_CHOICES = (('L', 'Laki-Laki'),
                  ('P', 'Perempuan'), )

class GenderChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): return obj.category

class AgeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): return obj.category + " (" + obj.detail + ")"

class EthnicChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): return obj

class DialectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): return obj

class speakForm(forms.Form):
    name = forms.CharField(label="Name", max_length=256, required=False, initial="Unknown")
    gender = GenderChoiceField(queryset=Gender.objects.all())
    age = AgeChoiceField(queryset=Age.objects.all())
    ethnic = EthnicChoiceField(queryset=Ethnic.objects.all())
    dialect = DialectChoiceField(queryset=Dialect.objects.all())
    
    # for bootstrap styling
    def __init__(self, *args, **kwargs):
        super(speakForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if hasattr(visible.field.widget, 'input_type'):
                if visible.field.widget.input_type in ['radio', 'checkbox']:
                    visible.field.widget.attrs['class'] = 'form-check-input'
                else:
                    visible.field.widget.attrs['class'] = 'form-control'
