# Generated by Django 2.1.4 on 2018-12-27 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suffix', models.CharField(max_length=10, verbose_name='尾号')),
                ('tips', models.CharField(max_length=10, verbose_name='备注')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('source', models.CharField(choices=[('bank', '银行'), ('stock', '股票'), ('zfb', '支付宝'), ('jd', '京东'), ('wx', '微信'), ('other', '其他')], default='bank', max_length=10, verbose_name='渠道')),
                ('issue', models.DateField(auto_now_add=True, verbose_name='购买时间')),
                ('start', models.DateField(verbose_name='起息日')),
                ('finish', models.DateField(verbose_name='到期日')),
                ('period', models.DurationField(verbose_name='周期(天)')),
                ('money', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='金额')),
                ('rate1', models.DecimalField(decimal_places=4, max_digits=5, verbose_name='预期年化收益率')),
                ('rate2', models.DecimalField(decimal_places=4, max_digits=5, verbose_name='实际年化收益率')),
                ('income', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='实际收益')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Card')),
            ],
            options={
                'ordering': ['-issue'],
            },
        ),
    ]
