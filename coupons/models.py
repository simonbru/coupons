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
        validators=[
            RegexValidator(r'[0-9]+'),
        ],
        max_length=40,
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
    disabled = models.BooleanField(
        verbose_name='désactivé',
        default=False,
        help_text='Masque le coupon pour les utilisateurs anonymes',
    )

    class Meta:
        verbose_name = 'coupon'
        verbose_name_plural = 'coupons'
        ordering = ('price', 'title')

    def __str__(self):
        return f'{self.title} - {self.price}'

    def last_comment_per_place(self):
        places = {}
        for comment in self.comments.order_by('-created_at'):
            if comment.restaurant not in places:
                places[comment.restaurant] = comment
        return places


class RestaurantManager(models.Manager):

    # Use Fribourg as default location
    FRIBOURG_LOC = (46.802352, 7.151291)

    def by_distance(self, lat=FRIBOURG_LOC[0], lon=FRIBOURG_LOC[1]):
        """Queryset ordered by estimated distance to given location"""
        lat = float(lat)
        lon = float(lon)
        return Restaurant.objects.extra(
            select={'distance': 'abs(lat - %s) + abs(lon - %s)'},
            select_params=(lat, lon),
        ).order_by('distance')


class Restaurant(models.Model):
    id = models.CharField(
        verbose_name='place id',
        primary_key=True,
        max_length=50,
        help_text="ID du lieu selon l'API de Google Maps",
    )
    name = models.CharField(
        verbose_name='nom',
        max_length=80,
    )
    address = models.CharField(
        verbose_name='adresse',
        max_length=150,
    )
    lat = models.DecimalField(
        verbose_name='latitude',
        max_digits=9,
        decimal_places=6,
    )
    lon = models.DecimalField(
        verbose_name='longitude',
        max_digits=9,
        decimal_places=6,
    )

    objects = RestaurantManager()

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def city(self):
        parts = self.address.split(',')
        if len(parts) > 0:
            return parts[-1]

    @property
    def short_address(self):
        parts = self.address.split(',')
        if len(parts) > 1:
            return parts[0]


class Comment(models.Model):
    coupon = models.ForeignKey(
        'Coupon',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(
        verbose_name='créé le',
        default=now,
    )
    author_ip = models.GenericIPAddressField(
        verbose_name="addresse IP de l'auteur",
        protocol='both',
        unpack_ipv4=True,
    )
    does_coupon_work = models.BooleanField(
        verbose_name='le coupon marche-t-il ?',
        default=True,
    )

    class Meta:
        verbose_name = 'commentaire'
        verbose_name_plural = 'commentaires'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.created_at}, {self.does_coupon_work}'