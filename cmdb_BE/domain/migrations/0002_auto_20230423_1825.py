# Generated by Django 3.2.13 on 2023-04-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainmanage',
            name='ExpirationDateStatus',
            field=models.IntegerField(choices=[('1', '域名未过期'), ('2', '域名已过期')], default='1', verbose_name='域名过期状态'),
        ),
        migrations.AlterField(
            model_name='domainmanage',
            name='status',
            field=models.CharField(choices=[('1', '急需续费'), ('2', '急需赎回'), ('2', '急需赎回'), ('3', '正常'), ('4', '转出中'), ('5', '域名持有者信息修改中'), ('6', '未实名认证'), ('7', '实名认证失败'), ('8', '实名认证审核中')], default='6', max_length=20, verbose_name='域名状态'),
        ),
    ]
