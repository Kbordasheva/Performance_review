from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):
    id = models.IntegerField(
        primary_key=True, blank=False, null=False, editable=False)
    name = models.CharField(_('Name'), max_length=50)
    manager = models.ForeignKey(
        'employee.Employee',
        verbose_name=_('Manager'),
        related_name='managed_units',
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self) -> str:
        return self.name
