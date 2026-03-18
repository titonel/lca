from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_administrador or request.user.tipo_profissional == 'ADM'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('index')
    return wrapper_func

def navegador_only(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_navegador or request.user.is_superuser or request.user.is_administrador or request.user.tipo_profissional == 'ADM'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acesso restrito a Navegadores.")
        return redirect('index')
    return wrapper_func

def medico_only(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.tipo_profissional == 'MED' or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acesso restrito a Médicos.")
        return redirect('index')
    return wrapper_func

def multi_only(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        allowed_roles = ['ENF', 'NUT', 'FAR']
        if request.user.is_authenticated and (request.user.tipo_profissional in allowed_roles or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acesso restrito à Equipe Multidisciplinar.")
        return redirect('index')
    return wrapper_func

def health_team(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        allowed_roles = ['MED', 'ENF', 'NUT', 'FAR']
        if request.user.is_authenticated and (request.user.tipo_profissional in allowed_roles or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acesso restrito à Equipe de Profissionais de Saúde.")
        return redirect('index')
    return wrapper_func
