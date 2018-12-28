from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Card(models.Model):
    owner = models.ForeignKey(User, models.CASCADE)
    suffix = models.CharField('尾号', max_length = 10)
    tips = models.CharField('备注', max_length = 10)

    def __str__(self):
        return self.suffix + '(' + self.tips + ')'

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
    issue = models.DateField('购买时间', auto_now_add = True)
    start = models.DateField('起息日')
    finish = models.DateField('到期日')
    period = models.DurationField('周期(天)')
    money = models.DecimalField('金额', max_digits = 10, decimal_places = 2)
    rate1 = models.DecimalField('预期年化收益率', max_digits = 5, decimal_places = 4)
    rate2 = models.DecimalField('实际年化收益率', max_digits = 5, decimal_places = 4)
    income = models.DecimalField('实际收益', max_digits = 10, decimal_places = 2)
    card = models.ForeignKey(Card, models.CASCADE)

    def __str__(self):
        return self.name + '(' + self.start.strftime("%Y-%m-%d") + " --" + str(self.period) + "--> " + self.finish.strftime("%Y-%m-%d") + ')' + str(self.money) + '(' + str(self.rate1) + ')'

    class Meta:
        ordering = ["-issue"]

