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
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cross', models.IntegerField(blank=True, null=True, unique=True)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('sexo', models.IntegerField(blank=True, null=True)),
                ('data_nascimento', models.DateField()),
                ('municipio', models.CharField(blank=True, max_length=100, null=True)),
                ('indicacao', models.CharField(blank=True, max_length=200, null=True)),
                ('medico', models.CharField(blank=True, max_length=100, null=True)),
                ('meta', models.IntegerField(blank=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('data_insercao', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_alta', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Paciente (Anticoagulação)',
                'verbose_name_plural': 'Pacientes (Anticoagulação)',
            },
        ),
        migrations.CreateModel(
            name='Medicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_inr', models.FloatField()),
                ('data_medicao', models.DateTimeField(default=django.utils.timezone.now)),
                ('intercorrencia', models.BooleanField(default=False)),
                ('intercorrencia_txt', models.TextField(blank=True, max_length=500, null=True)),
                ('paciente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='medicoes',
                    to='anticoagulacao.paciente',
                )),
                ('usuario', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Profissional Responsável',
                )),
            ],
            options={
                'verbose_name': 'Medição INR',
                'verbose_name_plural': 'Medições INR',
                'ordering': ['-data_medicao'],
            },
        ),
    ]
