# Generated by Django 3.2.10 on 2022-02-03 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marwacoin', '0027_auto_20220203_0734'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='avatar',
            field=models.ImageField(blank=True, default='OIP.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='firstsouscategorie',
            name='avatar',
            field=models.ImageField(blank=True, default='OIP.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='secondsouscategorie',
            name='avatar',
            field=models.ImageField(blank=True, default='OIP.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='contact',
            name='cause',
            field=models.CharField(choices=[('demande une partenaire', 'demande une partenaire'), ('la deuxiem echoix', 'la deuxiem choices')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='operation',
            field=models.CharField(choices=[('vente', 'vente'), ('location', 'location'), ('echange', 'echange'), ('donation', 'donation')], default='vente', max_length=255),
        ),
    ]
