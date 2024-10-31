# Generated by Django 5.1.1 on 2024-10-24 07:39

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadosocr',
            name='fecha_registro',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultadosocr',
            name='fecha_salida',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resultadosocr',
            name='id_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultadosocr',
            name='npaginas',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(choices=[('informe', 'Informe'), ('carta_recibida', 'Carta Recibida'), ('carta_enviada', 'Carta Enviada'), ('proforma', 'Proforma'), ('adquisicion', 'Adquisición'), ('compra', 'Compra'), ('certificacion', 'Certificación'), ('miscelanea', 'Miscelánea')], max_length=20)),
                ('resultado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='ocr.resultadosocr')),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
    ]