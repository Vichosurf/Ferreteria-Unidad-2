from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import AvisoGlobal, ConsultaCliente, Producto


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
        fields = ('nombre', 'correo', 'producto', 'mensaje')
        labels = {
            'nombre': 'Tu nombre',
            'correo': 'Tu correo electrónico',
            'producto': 'Producto de interés (opcional)',
            'mensaje': 'Tu consulta',
        }
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje'].strip()
        if len(mensaje) < 10:
            raise forms.ValidationError(
                'El mensaje debe tener al menos 10 caracteres.',
            )
        return mensaje


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'categoria', 'precio', 'stock')


class AvisoGlobalForm(forms.ModelForm):
    class Meta:
        model = AvisoGlobal
        fields = ('titulo', 'mensaje')
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4}),
        }
