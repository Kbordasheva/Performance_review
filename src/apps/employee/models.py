from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.db.models import EmailField
from django.utils.translation import gettext_lazy as _

from employee.choices import Gender, Seniority


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('The email field must be set')
        user = self.model(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user


class Employee(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First name'), max_length=200, blank=True)
    first_name_ru = models.CharField(_('First name in Russian'), max_length=200, blank=True)
    last_name = models.CharField(_('Last name'), max_length=200, blank=True)
    last_name_ru = models.CharField(_('Last name in Russian'), max_length=200, blank=True)
    middle_name_ru = models.CharField(_('Middle name in Russian'), max_length=200, blank=True)
    gender = models.IntegerField(_('Gender'), choices=Gender.choices, null=True)
    birth_date = models.DateField(_('Birth Date'), blank=True, null=True)
    email = EmailField(_('Email'), max_length=200, unique=True, null=True)
    phone = models.CharField(_('Phone'), max_length=100, blank=True)
    employment_date = models.DateField(_('Employment Date'), null=True)
    dismiss_date = models.DateField(_('Dismiss Date'), blank=True, null=True)
    position = models.CharField(_('Position'), max_length=254, blank=True)
    seniority = models.CharField(_('Seniority'), choices=Seniority.choices, max_length=20, blank=True)
    skills = models.ManyToManyField(
        'employee.Skill',
        related_name='employees',
        blank=True,
    )
    unit = models.ForeignKey(
        'unit.Unit',
        verbose_name=_('Unit'),
        related_name='employees',
        on_delete=models.PROTECT,
        null=True
    )
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Is Active?'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'

    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        # shortcut
        return self.get_full_name()

    @property
    def full_name_ru(self) -> str:
        # shortcut
        return self.get_full_name_ru()

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_full_name_ru(self) -> str:
        return (
            f'{self.first_name_ru} '
            f'{f"{self.middle_name_ru} " if self.middle_name_ru else ""}'
            f'{self.last_name_ru}'
        )

    @property
    def current_review(self):
        return self.review.order_by('-year').first()


class Skill(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

