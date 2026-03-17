from django.db import models
from django.conf import settings
from django.utils import timezone


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cross = models.IntegerField(null=True, blank=True, unique=True)
    cpf = models.CharField(max_length=11, null=True, blank=True, unique=True)
    sexo = models.IntegerField(null=True, blank=True)
    data_nascimento = models.DateField()
    municipio = models.CharField(max_length=100, null=True, blank=True)
    indicacao = models.CharField(max_length=200, null=True, blank=True)
    medico = models.CharField(max_length=100, null=True, blank=True)
    meta = models.IntegerField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    data_insercao = models.DateTimeField(default=timezone.now)
    data_alta = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Paciente (Anticoagulação)'
        verbose_name_plural = 'Pacientes (Anticoagulação)'


class Medicao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='medicoes')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Profissional Responsável"
    )

    valor_inr = models.FloatField()
    data_medicao = models.DateTimeField(default=timezone.now)
    intercorrencia = models.BooleanField(default=False)
    intercorrencia_txt = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['-data_medicao']
        verbose_name = 'Medição INR'
        verbose_name_plural = 'Medições INR'

    def __str__(self):
        return f"{self.paciente.nome} - INR {self.valor_inr} em {self.data_medicao}"
