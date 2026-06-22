from django import forms
from .models import Tarefa


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'prioridade', 'concluida']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da tarefa'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição (opcional)'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'concluida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
