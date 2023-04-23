# Generated by Django 3.2.13 on 2023-04-21 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomainAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=30, verbose_name='域名名称')),
                ('host_name', models.CharField(max_length=20, verbose_name='主机记录')),
                ('RecordType', models.CharField(max_length=20, verbose_name='记录类型')),
                ('analyshost', models.GenericIPAddressField(verbose_name='解析地址')),
                ('host_status', models.CharField(max_length=20, verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('note', models.TextField(blank=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '域名解析',
                'db_table': 'domain_analysis',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='DomainManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('platform', models.CharField(max_length=20, verbose_name='平台管理')),
                ('status', models.CharField(max_length=20, verbose_name='域名状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('expire_time', models.DateTimeField(auto_now=True, verbose_name='到期时间')),
                ('ExpirationTime', models.IntegerField(verbose_name='过期时间提示')),
                ('note', models.TextField(blank=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '域名管理',
                'db_table': 'domain_manage',
                'ordering': ('-id',),
            },
        ),
    ]
