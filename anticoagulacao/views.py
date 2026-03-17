import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Paciente, Medicao
from .decorators import health_team, admin_only


@login_required
def index(request):
    if request.user.mudar_senha:
        return redirect('trocar_senha')
    return render(request, 'anticoagulacao/index.html')


@login_required
@health_team
def gestao_pacientes(request):
    termo = request.GET.get('busca', '')
    if termo:
        pacientes = Paciente.objects.filter(
            Q(nome__icontains=termo) | Q(cpf__icontains=termo) | Q(cross__icontains=termo)
        ).order_by('-ativo', 'nome')
    else:
        pacientes = Paciente.objects.all().order_by('-ativo', 'nome')

    return render(request, 'anticoagulacao/pacientes.html', {'pacientes': pacientes})


@login_required
@health_team
def salvar_paciente(request):
    if request.method == 'POST':
        p_id = request.POST.get('paciente_id')

        if p_id:
            p = get_object_or_404(Paciente, id=p_id)
        else:
            p = Paciente()

        p.nome = request.POST.get('nome', '').upper()
        p.cpf = request.POST.get('cpf')

        cross = request.POST.get('cross')
        p.cross = int(cross) if cross else None

        nasc = request.POST.get('data_nascimento')
        if nasc:
            p.data_nascimento = nasc

        d_ins = request.POST.get('data_insercao')
        if d_ins:
            p.data_insercao = d_ins

        p.sexo = request.POST.get('sexo')
        p.municipio = request.POST.get('municipio')
        p.medico = request.POST.get('medico')
        p.indicacao = request.POST.get('indicacao')

        meta = request.POST.get('meta')
        p.meta = int(meta) if meta else 2
        p.ativo = True if request.POST.get('ativo') else False

        p.save()
        messages.success(request, 'Paciente salvo com sucesso!')
    return redirect('ac:gestao_pacientes')


@login_required
@health_team
def dar_alta_paciente(request, id):
    if request.method == 'POST':
        p = get_object_or_404(Paciente, id=id)
        p.ativo = False
        p.data_alta = date.today()
        p.save()
        return JsonResponse({'status': 'success', 'message': 'Alta realizada.'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
@health_team
def atendimento(request):
    paciente_id = request.GET.get('id')

    if paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)

        medicoes = paciente.medicoes.all().order_by('-data_medicao')
        historico_tabela = medicoes[:10]

        dados_grafico = paciente.medicoes.all().order_by('data_medicao')
        grafico_labels = [m.data_medicao.strftime('%d/%m/%Y') for m in dados_grafico]
        grafico_data = [m.valor_inr for m in dados_grafico]

        meta_min, meta_max = 2.0, 3.0
        indicacao_txt = (paciente.indicacao or "").lower()
        if 'prótese' in indicacao_txt or 'mecanica' in indicacao_txt:
            meta_min, meta_max = 2.5, 3.5

        return render(request, 'anticoagulacao/atendimento.html', {
            'paciente': paciente,
            'historico': historico_tabela,
            'grafico_labels': json.dumps(grafico_labels),
            'grafico_data': json.dumps(grafico_data),
            'meta_min': meta_min,
            'meta_max': meta_max,
        })

    else:
        pacientes = Paciente.objects.filter(ativo=True).order_by('nome')
        return render(request, 'anticoagulacao/atendimento.html', {'pacientes_lista': pacientes})


@login_required
@health_team
def registrar_atendimento(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        inr = request.POST.get('inr')
        obs = request.POST.get('obs')

        paciente = get_object_or_404(Paciente, id=paciente_id)

        Medicao.objects.create(
            paciente=paciente,
            usuario=request.user,
            valor_inr=float(inr.replace(',', '.')),
            intercorrencia_txt=obs,
            intercorrencia=bool(obs)
        )
        messages.success(request, 'INR registrado com sucesso!')
        return redirect(f"/anticoagulacao/atendimento/?id={paciente.id}")
    return redirect('ac:atendimento')


@login_required
@admin_only
def linha_cuidado(request):
    return render(request, 'anticoagulacao/dashboard.html')


@login_required
@health_team
def api_paciente(request, id):
    try:
        p = get_object_or_404(Paciente, id=id)

        d_nasc = p.data_nascimento.strftime('%Y-%m-%d') if p.data_nascimento else ''
        d_ins = p.data_insercao.strftime('%Y-%m-%d') if p.data_insercao else ''

        return JsonResponse({
            'status': 'success',
            'id': p.id,
            'nome': p.nome or '',
            'cpf': p.cpf or '',
            'cross': p.cross or '',
            'nascimento': d_nasc,
            'data_insercao': d_ins,
            'municipio': p.municipio or '',
            'medico': p.medico or '',
            'meta': p.meta or 2,
            'indicacao': p.indicacao or '',
            'sexo': p.sexo or 1,
            'ativo': p.ativo
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@admin_only
def api_dashboard(request):
    pacientes = Paciente.objects.filter(ativo__in=[True, 1]).prefetch_related('medicoes')
    hoje = date.today()

    lista_pacientes = []
    for p in pacientes:
        idade = 0
        if p.data_nascimento:
            idade = hoje.year - p.data_nascimento.year - (
                (hoje.month, hoje.day) < (p.data_nascimento.month, p.data_nascimento.day))

        meta_min, meta_max = 2.0, 3.0
        indicacao_txt = (p.indicacao or "").lower()
        if any(x in indicacao_txt for x in ['prótese', 'mecanica', 'protese']):
            meta_min, meta_max = 2.5, 3.5

        lista_medicoes = []
        for m in p.medicoes.all():
            if m.data_medicao:
                lista_medicoes.append({
                    'data': m.data_medicao.strftime('%Y-%m-%d'),
                    'inr': m.valor_inr or 0.0
                })

        lista_pacientes.append({
            'sexo': 'Masculino' if str(p.sexo) == '1' else 'Feminino',
            'idade': idade,
            'municipio': (p.municipio or "Não Informado").title(),
            'indicacao': (p.indicacao or "OUTROS").strip().upper(),
            'meta_min': meta_min,
            'meta_max': meta_max,
            'medicoes': lista_medicoes
        })

    return JsonResponse({'dados_pacientes': lista_pacientes}, safe=False)


@login_required
@admin_only
def painel_admin(request):
    from core.models import Usuario
    usuarios = Usuario.objects.all().order_by('username')
    total_pacientes = Paciente.objects.count()
    return render(request, 'anticoagulacao/admin/painel.html', {
        'usuarios': usuarios,
        'total_pacientes': total_pacientes
    })


@login_required
@admin_only
def gerenciar_pacientes_admin(request):
    pacientes = Paciente.objects.all().order_by('-data_insercao')
    return render(request, 'anticoagulacao/admin/pacientes_admin.html', {'pacientes': pacientes})
