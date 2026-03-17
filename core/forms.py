from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Senha")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'email', 'mudar_senha',
                  'drt', 'tipo_profissional', 'tipo_registro', 'registro_profissional', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
