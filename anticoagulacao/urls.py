from django.urls import path
from . import views

app_name = 'ac'

urlpatterns = [
    path('', views.index, name='index'),
    path('pacientes/', views.gestao_pacientes, name='gestao_pacientes'),
    path('paciente/salvar/', views.salvar_paciente, name='salvar_paciente'),
    path('paciente/alta/<int:id>/', views.dar_alta_paciente, name='dar_alta_paciente'),

    path('atendimento/', views.atendimento, name='atendimento'),
    path('atendimento/registrar/', views.registrar_atendimento, name='registrar_atendimento'),
    path('dashboard/', views.linha_cuidado, name='linha_cuidado'),

    path('api/paciente/<int:id>/', views.api_paciente, name='api_paciente'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),

    path('admin-painel/', views.painel_admin, name='painel_admin'),
    path('admin-painel/pacientes/', views.gerenciar_pacientes_admin, name='gerenciar_pacientes_admin'),
]
