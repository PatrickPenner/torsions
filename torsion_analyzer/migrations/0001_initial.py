# Generated by Django 3.1.2 on 2021-09-16 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Molecule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_id', models.IntegerField()),
                ('name', models.CharField(max_length=80)),
                ('mol_string', models.TextField()),
                ('file_type', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='TorsionAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'pending'), ('r', 'running'), ('s', 'success'), ('f', 'failure')], default='p', max_length=1)),
                ('mol_string', models.TextField()),
                ('result_string', models.TextField()),
                ('file_type', models.CharField(max_length=5)),
                ('accessed', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TorsionPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smarts', models.TextField()),
                ('csd_plot_path', models.TextField()),
                ('pdb_plot_path', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TorsionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atom_id_1', models.IntegerField()),
                ('atom_id_2', models.IntegerField()),
                ('atom_id_3', models.IntegerField()),
                ('atom_id_4', models.IntegerField()),
                ('angle', models.FloatField()),
                ('quality', models.CharField(max_length=10)),
                ('pattern_hierarchy', models.TextField()),
                ('molecule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torsion_analyzer.molecule')),
                ('torsion_pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torsion_analyzer.torsionpattern')),
            ],
        ),
        migrations.AddField(
            model_name='molecule',
            name='torsion_analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torsion_analyzer.torsionanalysis'),
        ),
    ]
