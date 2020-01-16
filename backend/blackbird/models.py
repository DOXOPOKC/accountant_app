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
    tariff = models.FloatField(default=0.0)
    # norm_type = models.FloatField(max_length=10, choices=NORM_TYPES)
    is_rough = models.BooleanField(default=True)
    equasion = models.TextField(max_length=300)

    def get_formula(self):
        return self.equasion

    def get_tax(self):
        return self.tax_rate

    def get_tariff(self):
        return self.tariff