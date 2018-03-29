from django import forms

class DropDownForm(forms.Form):
    quantity = forms.ChoiceField(label='Quantity', choices=[(x, x) for x in range(1, 4)])