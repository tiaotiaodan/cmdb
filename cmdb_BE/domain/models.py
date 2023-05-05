from django.db import models

# Create your models here.
class DomainManage(models.Model):
    name = models.CharField(max_length=30, verbose_name="名称")
    platform = models.CharField(max_length=20, verbose_name="平台管理")
    status = models.CharField(max_length=20, verbose_name="域名状态", blank=True, null=True,)
    create_time = models.CharField(max_length=20, verbose_name="创建时间", blank=True, null=True,)
    expire_time = models.CharField(max_length=20, verbose_name="到期时间", blank=True, null=True,)
    ExpirationTime = models.CharField(max_length=20,verbose_name="过期时间提示", blank=True, null=True,)
    ExpirationDateStatus = models.CharField(max_length=20,verbose_name="域名过期状态", choices=(('1','域名未过期'),('2','域名已过期')), default='1', blank=True, null=True,)
    note = models.TextField(blank=True, null=True, verbose_name="备注")

    class Meta:
        db_table = "domain_manage"
        verbose_name_plural = "域名管理"
        ordering = ('-id',)

    def __str__(self):
        return self.name


class DomainAnalysis(models.Model):
    domain_name = models.ForeignKey(DomainManage, on_delete=models.PROTECT, verbose_name="关联域名名称")   # 一对多
    host_name = models.CharField(max_length=20,  verbose_name="主机记录")
    RecordType = models.CharField(max_length=20, verbose_name="记录类型")
    analyshost = models.GenericIPAddressField(verbose_name="解析地址")
    host_status = models.CharField(max_length=20, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    note = models.TextField(blank=True, null=True, verbose_name="备注")

    class Meta:
        db_table = "domain_analysis"
        verbose_name_plural = "域名解析"
        ordering = ('-id',)

    def __str__(self):
        return self.domain_name