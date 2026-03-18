from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('trocar-senha/', views.trocar_senha, name='trocar_senha'),
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('usuarios/', views.gestao_usuarios, name='gestao_usuarios'),
    path('usuarios/excluir/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('api/usuario/<int:id>/', views.api_usuario, name='api_usuario'),
]
