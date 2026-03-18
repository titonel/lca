import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from hipertensao.models import Medicamento


class Command(BaseCommand):
    help = "Carrega medicamentos a partir de um arquivo TOML para o banco de dados"

    def add_arguments(self, parser):
        parser.add_argument(
            "toml_file",
            type=str,
            help="Caminho para o arquivo medicamentos.toml",
        )
        parser.add_argument(
            "--atualizar",
            action="store_true",
            help="Atualiza registros existentes (mesmo principio_ativo + dose_padrao)",
        )

    def handle(self, *args, **options):
        toml_path = Path(options["toml_file"])
        if not toml_path.exists():
            raise CommandError(f"Arquivo não encontrado: {toml_path}")

        # tomllib está disponível na stdlib a partir do Python 3.11;
        # para versões anteriores tenta o pacote tomli (pip install tomli).
        if sys.version_info >= (3, 11):
            import tomllib
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
        else:
            try:
                import tomllib
                with open(toml_path, "rb") as f:
                    data = tomllib.load(f)
            except ModuleNotFoundError:
                try:
                    import tomli as tomllib
                    with open(toml_path, "rb") as f:
                        data = tomllib.load(f)
                except ModuleNotFoundError:
                    raise CommandError(
                        "Instale o suporte a TOML: pip install tomli  "
                        "(ou use Python 3.11+)"
                    )

        registros = data.get("medicamentos", [])
        if not registros:
            raise CommandError(
                "Nenhum registro encontrado. O arquivo deve ter uma tabela "
                "[[medicamentos]]."
            )

        criados = atualizados = ignorados = 0

        for item in registros:
            principio_ativo = item.get("principio_ativo", "").strip()
            dose_padrao = item.get("dose_padrao", "").strip()

            if not principio_ativo or not dose_padrao:
                self.stderr.write(
                    self.style.WARNING(
                        f"Registro ignorado (principio_ativo ou dose_padrao vazio): {item}"
                    )
                )
                ignorados += 1
                continue

            defaults = {
                "classe": item.get("classe", "").strip(),
                "nomes_comerciais": item.get("nomes_comerciais", "").strip(),
                "ativo": item.get("ativo", True),
                "is_remume": item.get("is_remume", False),
            }

            if options["atualizar"]:
                obj, created = Medicamento.objects.update_or_create(
                    principio_ativo=principio_ativo,
                    dose_padrao=dose_padrao,
                    defaults=defaults,
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1
            else:
                _, created = Medicamento.objects.get_or_create(
                    principio_ativo=principio_ativo,
                    dose_padrao=dose_padrao,
                    defaults=defaults,
                )
                if created:
                    criados += 1
                else:
                    ignorados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Concluído — criados: {criados}, "
                f"atualizados: {atualizados}, "
                f"ignorados/existentes: {ignorados}"
            )
        )
