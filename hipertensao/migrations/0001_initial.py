import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classe', models.CharField(max_length=100)),
                ('principio_ativo', models.CharField(max_length=100)),
                ('dose_padrao', models.CharField(max_length=50)),
                ('nomes_comerciais', models.CharField(blank=True, max_length=255)),
                ('ativo', models.BooleanField(default=True)),
                ('is_remume', models.BooleanField(default=False, verbose_name='Pertence ao SUS/REMUME')),
            ],
            options={
                'ordering': ['classe', 'principio_ativo'],
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('etnia', models.CharField(
                    choices=[('Branca', 'Branca'), ('Parda', 'Parda'), ('Negra', 'Negra'), ('Indígena', 'Indígena')],
                    max_length=20,
                )),
                ('data_nascimento', models.DateField()),
                ('data_insercao', models.DateField(default=datetime.date.today)),
                ('data_alta', models.DateField(blank=True, null=True)),
                ('municipio', models.CharField(default='Caraguatatuba', max_length=100)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('ativo', models.BooleanField(default=True)),
                ('siresp', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número CROSS / SIRESP')),
                ('altura_ultima', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AtendimentoMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_atendimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('score_prevent_valor', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score Prevent (%)')),
                ('subjetivo', models.TextField(verbose_name='S - Subjetivo')),
                ('objetivo', models.TextField(verbose_name='O - Objetivo')),
                ('avaliacao', models.TextField(verbose_name='A - Avaliação')),
                ('plano', models.TextField(verbose_name='P - Plano')),
                ('cid10_1', models.CharField(max_length=10, verbose_name='CID-10 Principal')),
                ('cid10_2', models.CharField(blank=True, max_length=10, null=True)),
                ('cid10_3', models.CharField(blank=True, max_length=10, null=True)),
                ('cid11_correspondente', models.CharField(blank=True, max_length=200)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hipertensao.paciente')),
                ('medico', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.CreateModel(
            name='Afericao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_afericao', models.DateTimeField(auto_now_add=True)),
                ('pressao_sistolica', models.IntegerField()),
                ('pressao_diastolica', models.IntegerField()),
                ('frequencia_cardiaca', models.IntegerField(blank=True, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('altura', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('imc', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('observacao', models.TextField(blank=True)),
                ('paciente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='afericoes',
                    to='hipertensao.paciente',
                )),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to=settings.AUTH_USER_MODEL,
                )),
                ('medicamentos', models.ManyToManyField(blank=True, to='hipertensao.medicamento')),
            ],
            options={
                'ordering': ['-data_afericao'],
            },
        ),
        migrations.CreateModel(
            name='AtendimentoMultidisciplinar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_atendimento', models.DateTimeField(auto_now_add=True)),
                ('religiao', models.CharField(blank=True, max_length=50, null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=50, null=True)),
                ('escolaridade', models.CharField(blank=True, max_length=50, null=True)),
                ('fonte_renda', models.CharField(blank=True, max_length=50, null=True)),
                ('renda_familiar', models.CharField(blank=True, max_length=50, null=True)),
                ('reside_com', models.CharField(blank=True, max_length=50, null=True)),
                ('rede_familiar', models.CharField(blank=True, max_length=50, null=True)),
                ('queixa_principal', models.TextField(blank=True, null=True)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Peso (kg)')),
                ('altura', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Altura (m)')),
                ('imc', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='IMC')),
                ('circunferencia_abdominal', models.DecimalField(
                    decimal_places=2,
                    max_digits=5,
                    verbose_name='Circunferência Abdominal (cm)',
                )),
                ('tem_diabetes', models.BooleanField(default=False)),
                ('tipo_diabetes', models.CharField(
                    blank=True,
                    choices=[('1', 'Tipo 1'), ('2', 'Tipo 2'), ('G', 'Gestacional')],
                    max_length=1,
                    null=True,
                )),
                ('fumante', models.BooleanField(default=False)),
                ('macos_por_dia', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('anos_fumando', models.IntegerField(blank=True, null=True)),
                ('carga_tabagica', models.DecimalField(
                    blank=True,
                    decimal_places=1,
                    max_digits=6,
                    null=True,
                    verbose_name='Anos-Maço',
                )),
                ('tem_lesao_orgao', models.BooleanField(default=False)),
                ('loa_coracao', models.BooleanField(default=False, verbose_name='Coração (HVE/IAM)')),
                ('loa_cerebro', models.BooleanField(default=False, verbose_name='Cérebro (AVC/AIT)')),
                ('loa_rins', models.BooleanField(default=False, verbose_name='Rins (Doença Renal)')),
                ('loa_arterias', models.BooleanField(default=False, verbose_name='Artérias Periféricas')),
                ('loa_olhos', models.BooleanField(default=False, verbose_name='Retinopatia')),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('paciente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='atendimentos_multi',
                    to='hipertensao.paciente',
                )),
                ('profissional', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.CreateModel(
            name='AvaliacaoPrevent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
                ('idade', models.IntegerField()),
                ('sexo', models.CharField(max_length=1)),
                ('colesterol_total', models.IntegerField(verbose_name='Colesterol Total (mg/dL)')),
                ('hdl', models.IntegerField(verbose_name='HDL (mg/dL)')),
                ('pressao_sistolica', models.IntegerField(verbose_name='PAS (mmHg)')),
                ('em_tratamento_has', models.BooleanField(default=True, verbose_name='Em tto Anti-hipertensivo?')),
                ('tem_diabetes', models.BooleanField(default=False)),
                ('fumante', models.BooleanField(default=False)),
                ('tfg', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='eGFR (ml/min)')),
                ('risco_10_anos', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Risco 10 Anos (%)')),
                ('risco_30_anos', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Risco 30 Anos (%)')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hipertensao.paciente')),
            ],
            options={
                'verbose_name': 'Avaliação PREVENT',
            },
        ),
        migrations.CreateModel(
            name='TriagemHipertensao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_triagem', models.DateTimeField(default=django.utils.timezone.now)),
                ('pa_sistolica_1', models.IntegerField(verbose_name='PAS 1')),
                ('pa_diastolica_1', models.IntegerField(verbose_name='PAD 1')),
                ('pa_sistolica_2', models.IntegerField(verbose_name='PAS 2')),
                ('pa_diastolica_2', models.IntegerField(verbose_name='PAD 2')),
                ('pa_sistolica_3', models.IntegerField(verbose_name='PAS 3')),
                ('pa_diastolica_3', models.IntegerField(verbose_name='PAD 3')),
                ('media_sistolica', models.DecimalField(decimal_places=1, max_digits=5)),
                ('media_diastolica', models.DecimalField(decimal_places=1, max_digits=5)),
                ('qtd_antihipertensivos', models.IntegerField(default=0)),
                ('risco_loa_presente', models.BooleanField(default=False)),
                ('status_elegibilidade', models.CharField(
                    choices=[('ELEGIVEL', 'Elegível'), ('CONTRARREFERENCIA', 'Não Elegível')],
                    max_length=20,
                )),
                ('motivo_desfecho', models.TextField(blank=True, null=True)),
                ('paciente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='triagens_has',
                    to='hipertensao.paciente',
                )),
                ('profissional', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.CreateModel(
            name='PrescricaoMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_prescricao', models.DateTimeField(auto_now_add=True)),
                ('observacoes_gerais', models.TextField(blank=True)),
                ('atendimento', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='prescricao',
                    to='hipertensao.atendimentomedico',
                )),
            ],
        ),
        migrations.CreateModel(
            name='ItemPrescricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento_nome', models.CharField(max_length=200)),
                ('concentracao', models.CharField(max_length=100)),
                ('posologia', models.TextField()),
                ('quantidade', models.CharField(max_length=50)),
                ('tipo', models.CharField(
                    choices=[
                        ('CONTINUO', 'Uso Contínuo'),
                        ('TEMPORARIO', 'Uso Temporário'),
                        ('CONTROLADO', 'Controle Especial'),
                    ],
                    default='CONTINUO',
                    max_length=20,
                )),
                ('prescricao', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='itens',
                    to='hipertensao.prescricaomedica',
                )),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='medicamento',
            unique_together={('principio_ativo', 'dose_padrao')},
        ),
    ]
