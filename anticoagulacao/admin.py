from django.contrib import admin
from .models import Paciente, Medicao

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'municipio', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'cpf']

@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'valor_inr', 'data_medicao']
    list_filter = ['intercorrencia']
