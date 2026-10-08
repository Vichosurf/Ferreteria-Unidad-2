from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import ConsultaCliente


class RegistroClienteForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirma la contraseña'


class ConsultaClienteForm(forms.ModelForm):
    class Meta:
        model = ConsultaCliente
        fields = ('producto', 'mensaje')
        labels = {
            'producto': 'Producto de interés (opcional)',
            'mensaje': 'Tu consulta',
        }
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }
