import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Card(models.Model):
    owner = models.ForeignKey(User, models.CASCADE)
    suffix = models.CharField('尾号', max_length = 10)
    tips = models.CharField('备注', max_length = 10)

    def __str__(self):
        return self.suffix + '(' + self.tips + ')'

    class Meta:
        verbose_name = '银行卡'
        verbose_name_plural = '银行卡'

class Investment(models.Model):
    enum_source_type = (
        ('bank', '银行'),
        ('stock', '股票'),
        ('zfb', '支付宝'),
        ('jd', '京东'),
        ('wx', '微信'),
        ('other', '其他'),
    )

    name = models.CharField('名称', max_length = 10)
    source = models.CharField('渠道', choices = enum_source_type, max_length = 10, default = 'bank')
    issue = models.DateField('记录时间', auto_now_add = True)
    start = models.DateField('起息日')
    finish = models.DateField('到期日', default = None, blank = True, null = True)
    finished = models.BooleanField('已到期', default = False)
    period = models.IntegerField('周期(天)', default = 0)
    money = models.FloatField('金额', default = 0.0)
    rate1 = models.FloatField('预期年化收益率(%)', default = 0.0)
    rate2 = models.FloatField('实际年化收益率(%)', default = 0.0)
    income1 = models.FloatField('预计当前收益', default = 0.0)
    income2 = models.FloatField('预计总收益', default = 0.0)
    income3 = models.FloatField('实际总收益', default = 0.0)
    card = models.ForeignKey(Card, models.CASCADE)

    @property
    def get_finished(self):
        return self.finish and datetime.date.today() >= self.finish
    
    @property
    def get_period(self):
        a = self.start
        b = self.finish
        if not b:
            b = datetime.date.today()
        return (b - a).days

    @property
    def get_rate2(self):
        if self.income3 == 0.0 or self.period == 0 or self.money == 0.0:
            return 0.0

        return 100 * 365 * self.income3 / self.period / self.money

    @property
    def get_income1(self):
        today = datetime.date.today()
        if self.finish and today >= self.finish:
            today = self.finish
        p = (today - self.start).days
        if p > 0:
            return self.money * self.rate1 * p / 100 / 365
        return 0.0
    
    @property
    def get_income2(self):
        if self.period > 0:
            return self.money * self.rate1 * self.period / 100 / 365
        return 0.0

    def save(self, *args, **kwargs):
        self.finished = self.get_finished
        self.period = self.get_period
        self.rate2 = self.get_rate2
        self.income1 = self.get_income1
        self.income2 = self.get_income2
        super(Investment, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + '(' + self.start.strftime("%Y-%m-%d") + " --" + str(self.period) + "--> " + self.finish.strftime("%Y-%m-%d") + ')' + str(self.money) + '(' + str(self.rate1) + ')'

    class Meta:
        ordering = ["-issue"]
        verbose_name_plural = '投资'

