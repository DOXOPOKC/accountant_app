from django.db import models


# NORM_TYPES = [
#     (1, 'м3'),
#     (2, 'чел.'),
#     (3, 'шт.'),
#     (4, 'место'),
# ]


class Formula(models.Model):
    since_date = models.DateField(null=True, blank=True)
    up_to_date = models.DateField(null=True, blank=True)
    tax_rate = models.FloatField(default=0.0)
    is_rough = models.BooleanField(default=True)
    equasion = models.TextField(max_length=300)

    def get_formula(self):
        return self.equasion

    def get_tax(self):
        return self.tax_rate

    def __str__(self):
        return ('Формула расчета. '
                + f'Действует с {self.since_date.strftime("%d.%m.%Y")} '
                + f'по {self.up_to_date.strftime("%d.%m.%Y")}.')

    class Meta:
        verbose_name_plural = "Формулы"


class Tariff(models.Model):
    since_date = models.DateField(null=True, blank=True)
    up_to_date = models.DateField(null=True, blank=True)
    tariff = models.FloatField(default=0.0)

    def __str__(self):
        return (f'Тариф {self.tariff}р., действующий с'
                + f' {self.since_date.strftime("%d.%m.%Y")} по'
                + f' {self.up_to_date.strftime("%d.%m.%Y")}.')

    class Meta:
        verbose_name_plural = "Тарифы"
