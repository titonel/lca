#!/usr/bin/env python
"""
Normaliza os nomes de pacientes e usuários já cadastrados no banco de dados.

Uso (a partir da raiz do projeto):
    python normalizar_dados.py              # aplica as alterações
    python normalizar_dados.py --dry-run    # apenas exibe o que seria alterado
"""

import os
import sys
import django

# ---------------------------------------------------------------------------
# Inicializa o Django
# ---------------------------------------------------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linhas_cuidado.settings')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

django.setup()

# ---------------------------------------------------------------------------
# Imports (somente após django.setup())
# ---------------------------------------------------------------------------
from core.utils import normalizar_nome  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _exibe_cabecalho(titulo: str) -> None:
    print(f'\n{"=" * 60}')
    print(f'  {titulo}')
    print('=' * 60)


def _resumo(entidade: str, alterados: int, dry_run: bool) -> None:
    modo = '[DRY-RUN] ' if dry_run else ''
    acao = 'seriam alterados' if dry_run else 'alterados'
    print(f'  → {modo}{entidade}: {alterados} registro(s) {acao}.')


# ---------------------------------------------------------------------------
# Normalização de Usuários (core)
# ---------------------------------------------------------------------------
def normalizar_usuarios(dry_run: bool) -> int:
    from core.models import Usuario

    _exibe_cabecalho('Usuários')
    alterados = 0

    for u in Usuario.objects.all():
        novo_first = normalizar_nome(u.first_name)
        novo_last  = normalizar_nome(u.last_name)

        if novo_first != u.first_name or novo_last != u.last_name:
            print(
                f'  #{u.id:>5}  "{u.first_name} {u.last_name}"'
                f'  →  "{novo_first} {novo_last}"'
            )
            if not dry_run:
                Usuario.objects.filter(pk=u.pk).update(
                    first_name=novo_first,
                    last_name=novo_last,
                )
            alterados += 1

    _resumo('Usuários', alterados, dry_run)
    return alterados


# ---------------------------------------------------------------------------
# Normalização de Pacientes — Hipertensão
# ---------------------------------------------------------------------------
def normalizar_pacientes_has(dry_run: bool) -> int:
    from hipertensao.models import Paciente

    _exibe_cabecalho('Pacientes — Hipertensão (HAS)')
    alterados = 0

    for p in Paciente.objects.all():
        novo_nome      = normalizar_nome(p.nome)
        novo_municipio = normalizar_nome(p.municipio) if p.municipio else p.municipio

        mudancas = []
        if novo_nome != p.nome:
            mudancas.append(f'nome: "{p.nome}" → "{novo_nome}"')
        if novo_municipio != p.municipio:
            mudancas.append(f'município: "{p.municipio}" → "{novo_municipio}"')

        if mudancas:
            print(f'  #{p.id:>5}  ' + '  |  '.join(mudancas))
            if not dry_run:
                Paciente.objects.filter(pk=p.pk).update(
                    nome=novo_nome,
                    municipio=novo_municipio,
                )
            alterados += 1

    _resumo('Pacientes HAS', alterados, dry_run)
    return alterados


# ---------------------------------------------------------------------------
# Normalização de Pacientes — Anticoagulação
# ---------------------------------------------------------------------------
def normalizar_pacientes_ac(dry_run: bool) -> int:
    from anticoagulacao.models import Paciente

    _exibe_cabecalho('Pacientes — Anticoagulação (AC)')
    alterados = 0

    for p in Paciente.objects.all():
        novo_nome      = normalizar_nome(p.nome)
        novo_medico    = normalizar_nome(p.medico)    if p.medico    else p.medico
        novo_municipio = normalizar_nome(p.municipio) if p.municipio else p.municipio

        mudancas = []
        if novo_nome != p.nome:
            mudancas.append(f'nome: "{p.nome}" → "{novo_nome}"')
        if novo_medico != p.medico:
            mudancas.append(f'médico: "{p.medico}" → "{novo_medico}"')
        if novo_municipio != p.municipio:
            mudancas.append(f'município: "{p.municipio}" → "{novo_municipio}"')

        if mudancas:
            print(f'  #{p.id:>5}  ' + '  |  '.join(mudancas))
            if not dry_run:
                Paciente.objects.filter(pk=p.pk).update(
                    nome=novo_nome,
                    medico=novo_medico,
                    municipio=novo_municipio,
                )
            alterados += 1

    _resumo('Pacientes AC', alterados, dry_run)
    return alterados


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------
def main() -> None:
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print('\n[DRY-RUN] Nenhuma alteração será gravada no banco.')
    else:
        print('\nIniciando normalização de dados...')

    try:
        total  = normalizar_usuarios(dry_run)
        total += normalizar_pacientes_has(dry_run)
        total += normalizar_pacientes_ac(dry_run)
    except Exception as exc:
        print(f'\nERRO: {exc}')
        print('\nVerifique se o banco de dados existe e as migrações foram aplicadas:')
        print('  python manage.py migrate')
        sys.exit(1)

    print(f'\n{"=" * 60}')
    if dry_run:
        print(f'  [DRY-RUN] {total} registro(s) seriam atualizados.')
    else:
        print(f'  Concluído. {total} registro(s) atualizados com sucesso.')
    print('=' * 60 + '\n')


if __name__ == '__main__':
    main()
