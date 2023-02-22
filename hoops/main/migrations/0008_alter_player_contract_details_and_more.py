# Generated by Django 4.1.5 on 2023-02-21 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_contract_player_contract_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='contract_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.contract'),
        ),
        migrations.AlterField(
            model_name='player',
            name='contract_offers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.playeroffers'),
        ),
        migrations.AlterField(
            model_name='player',
            name='feature_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.featurelist'),
        ),
        migrations.AlterField(
            model_name='player',
            name='history_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.historylist'),
        ),
    ]
