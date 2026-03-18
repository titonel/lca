"""
Comando para normalizar nomes já registrados no banco de dados.

Uso:
    python manage.py normalizar_nomes
    python manage.py normalizar_nomes --dry-run   # apenas exibe o que seria alterado
"""

from django.core.management.base import BaseCommand
from core.utils import normalizar_nome


class Command(BaseCommand):
    help = 'Normaliza nomes de pacientes e usuários já cadastrados no banco de dados.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Exibe as alterações sem gravá-las no banco.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        total = 0

        total += self._normalizar_usuarios(dry_run)
        total += self._normalizar_pacientes_has(dry_run)
        total += self._normalizar_pacientes_ac(dry_run)

        modo = '[DRY-RUN] ' if dry_run else ''
        self.stdout.write(self.style.SUCCESS(
            f'{modo}Concluído. {total} registro(s) {"seriam " if dry_run else ""}atualizados.'
        ))

    def _normalizar_usuarios(self, dry_run):
        from core.models import Usuario
        alterados = 0
        for u in Usuario.objects.all():
            novo_first = normalizar_nome(u.first_name)
            novo_last = normalizar_nome(u.last_name)
            if novo_first != u.first_name or novo_last != u.last_name:
                self.stdout.write(
                    f'  [Usuário #{u.id}] "{u.first_name} {u.last_name}" → "{novo_first} {novo_last}"'
                )
                if not dry_run:
                    u.first_name = novo_first
                    u.last_name = novo_last
                    Usuario.objects.filter(pk=u.pk).update(
                        first_name=novo_first, last_name=novo_last
                    )
                alterados += 1
        self.stdout.write(f'Usuários: {alterados} alterado(s).')
        return alterados

    def _normalizar_pacientes_has(self, dry_run):
        from hipertensao.models import Paciente
        alterados = 0
        for p in Paciente.objects.all():
            novo_nome = normalizar_nome(p.nome)
            if novo_nome != p.nome:
                self.stdout.write(f'  [HAS Paciente #{p.id}] "{p.nome}" → "{novo_nome}"')
                if not dry_run:
                    Paciente.objects.filter(pk=p.pk).update(nome=novo_nome)
                alterados += 1
        self.stdout.write(f'Pacientes HAS: {alterados} alterado(s).')
        return alterados

    def _normalizar_pacientes_ac(self, dry_run):
        from anticoagulacao.models import Paciente
        alterados = 0
        for p in Paciente.objects.all():
            novo_nome = normalizar_nome(p.nome)
            novo_medico = normalizar_nome(p.medico) if p.medico else p.medico
            if novo_nome != p.nome or novo_medico != p.medico:
                self.stdout.write(
                    f'  [AC Paciente #{p.id}] nome: "{p.nome}" → "{novo_nome}"'
                    + (f', médico: "{p.medico}" → "{novo_medico}"' if novo_medico != p.medico else '')
                )
                if not dry_run:
                    Paciente.objects.filter(pk=p.pk).update(
                        nome=novo_nome, medico=novo_medico
                    )
                alterados += 1
        self.stdout.write(f'Pacientes Anticoagulação: {alterados} alterado(s).')
        return alterados
