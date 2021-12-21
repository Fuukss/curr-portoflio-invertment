from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models import ProtectedError


class Currencies(models.Model):
    currency_name = models.CharField(max_length=3, default='')

    def __str__(self):
        return self.currency_name

    class Meta:
        verbose_name_plural = 'currency name'


class InvestmentDetails(models.Model):
    currency = models.CharField(max_length=3, default='')
    percent_of_investment = models.DecimalField(max_digits=4, decimal_places=1)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    def __str__(self):
        return self.currency + ' ' + str(self.percent_of_investment)

    def return_details(self):
        return self.currency, self.percent_of_investment, self.year, self.month, self.day

    class Meta:
        verbose_name_plural = 'investment details'
        ordering = ['id']


@receiver([pre_delete], sender=Currencies)
def default_currencies_handler(sender, instance, **kwargs):
    """
    Signal for unable deleted basics currencies.
    """
    raise ProtectedError('The General currencies can not be deleted', instance)

