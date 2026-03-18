from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    mudar_senha = models.BooleanField(default=False, verbose_name="Forçar Troca de Senha")
    email_verificado = models.BooleanField(default=False, verbose_name="Email Verificado")
    is_administrador = models.BooleanField(default=False, verbose_name="Administrador do Sistema")
    is_navegador = models.BooleanField(default=False, verbose_name="Navegador")

    TIPO_PROFISSIONAL_CHOICES = [
        ('MED', 'Médico'),
        ('ENF', 'Enfermeiro'),
        ('NUT', 'Nutricionista'),
        ('FAR', 'Farmacêutico'),
        ('ADM', 'Administrativo'),
    ]
    TIPO_REGISTRO_CHOICES = [
        ('CRM', 'CRM'),
        ('COREN', 'COREN'),
        ('CRN', 'CRN'),
        ('CRF', 'CRF'),
    ]
    tipo_profissional = models.CharField(max_length=3, choices=TIPO_PROFISSIONAL_CHOICES, null=True, blank=True)
    tipo_registro = models.CharField(max_length=10, choices=TIPO_REGISTRO_CHOICES, null=True, blank=True)
    registro_profissional = models.CharField(max_length=20, null=True, blank=True)
    drt = models.CharField(max_length=20, null=True, blank=True, verbose_name="DRT / Matrícula")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    @property
    def assinatura_completa(self):
        nome = self.get_full_name() or self.username
        detalhes = []
        if self.tipo_registro and self.registro_profissional:
            detalhes.append(f"{self.tipo_registro}: {self.registro_profissional}")
        if self.drt:
            detalhes.append(f"Matrícula: {self.drt}")
        if detalhes:
            return f"{nome} | {' - '.join(detalhes)}"
        return nome

    def __str__(self):
        return self.assinatura_completa
