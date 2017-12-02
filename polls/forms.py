from django.forms import ModelForm, Textarea
from .models import Label


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['label_text']
        widgets = {
            'label_text': Textarea(attrs={'cols': 40, 'rows': 15}),
        }