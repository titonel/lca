from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Usuario
from .decorators import admin_only
from .forms import UsuarioForm, PerfilForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, 'Usuário inativo. Contate a administração.')
            else:
                login(request, user)
                if user.mudar_senha:
                    return redirect('trocar_senha')
                return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def trocar_senha(request):
    if request.method == 'POST':
        nova = request.POST.get('nova_senha')
        conf = request.POST.get('confirmacao')
        if nova == conf and len(nova) >= 6:
            request.user.set_password(nova)
            request.user.mudar_senha = False
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Senhas não conferem ou são muito curtas (mínimo 6 caracteres).')
    return render(request, 'trocar_senha.html')

@login_required
def index(request):
    if request.user.mudar_senha:
        return redirect('trocar_senha')
    return render(request, 'index.html')

@login_required
def meu_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('meu_perfil')
        else:
            for f, err in form.errors.items():
                messages.error(request, f"{f}: {err}")
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'meu_perfil.html', {'form': form})


@login_required
@admin_only
def gestao_usuarios(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        instance = get_object_or_404(Usuario, id=usuario_id) if usuario_id else None
        form = UsuarioForm(request.POST, instance=instance)
        if form.is_valid():
            try:
                form.save()
                msg = "Usuário atualizado!" if usuario_id else "Usuário cadastrado!"
                messages.success(request, msg)
                return redirect('gestao_usuarios')
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {e}")
        else:
            for f, err in form.errors.items():
                messages.error(request, f"{f}: {err}")
    users = Usuario.objects.all().order_by('first_name')
    return render(request, 'gestao_usuarios.html', {'users': users})

@login_required
@admin_only
def excluir_usuario(request, id):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=id)
        if usuario == request.user:
            messages.error(request, 'Você não pode excluir sua própria conta.')
        else:
            nome = usuario.get_full_name() or usuario.username
            usuario.delete()
            messages.success(request, f'Usuário "{nome}" excluído com sucesso.')
    return redirect('gestao_usuarios')


@login_required
@admin_only
def api_usuario(request, id):
    u = get_object_or_404(Usuario, id=id)
    return JsonResponse({
        'id': u.id,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'username': u.username,
        'email': u.email,
        'drt': u.drt or "",
        'tipo_profissional': u.tipo_profissional or "",
        'tipo_registro': u.tipo_registro or "",
        'registro_profissional': u.registro_profissional or "",
        'is_active': u.is_active,
        'mudar_senha': u.mudar_senha,
        'is_administrador': u.is_administrador,
        'is_navegador': u.is_navegador,
    })
