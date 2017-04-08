from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now


class Category(models.Model):
    title = models.CharField(
        verbose_name='Titre',
        max_length=80,
    )

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Coupon(models.Model):
    title = models.CharField(
        verbose_name='titre',
        max_length=80,
    )
    price = models.DecimalField(
        verbose_name='prix',
        max_digits=10,
        decimal_places=2,
    )
    barcode = models.CharField(
        verbose_name='code-barres',
        help_text='Code EAN13 (13 chiffres)',
        validators=[
            RegexValidator(r'[0-9]{13}'),
        ],
        max_length=13,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='coupons',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='date de création',
        default=now,
        editable=False,
    )

    class Meta:
        verbose_name = 'coupon'
        verbose_name_plural = 'coupons'
        ordering = ('price', 'title')

    def __str__(self):
        return f'{self.title} - {self.price}'
