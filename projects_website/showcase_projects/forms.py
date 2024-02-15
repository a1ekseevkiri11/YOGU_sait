from django import forms

class ConfirmationForm(forms.Form):
    confirmation = forms.BooleanField(label='Вы уверены, что хотите присоединиться к проекту?', required=True)