# Generated by Django 3.1.3 on 2020-12-21 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administracao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorarioEstabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('vagas', models.PositiveIntegerField()),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='administracao.estabelecimentosaude')),
                ('vacina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='administracao.vacina')),
            ],
        ),
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('aplicado', models.BooleanField(default=False)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='administracao.estabelecimentosaude')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='administracao.usuario')),
                ('vacina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracao.vacina')),
            ],
        ),
    ]
