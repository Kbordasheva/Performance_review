from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed "created_at" and "updated_at" fields.
    created_at - automatically set the field to now when the object is first created.
    updated_at - automatically set the field to now every time the object is saved.
    """
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


class PerformanceReview(models.Model):
    employee = models.ForeignKey(
        'employee.Employee',
        verbose_name=_('Employee'),
        on_delete=models.PROTECT,
        related_name='review',
    )
    year = models.SmallIntegerField(
        _('Year'),
        validators=[MinValueValidator(2000), MaxValueValidator(2050)],
        null=True
    )

    def __str__(self) -> str:
        return f'PR of {self.employee.full_name} - {self.year}'


class Goal(TimeStampedModel):
    review = models.ForeignKey(
        'performance_review.PerformanceReview',
        verbose_name=_('Review'),
        on_delete=models.CASCADE,
        related_name='goals',
    )
    text = models.TextField(_('Text'), max_length=1000)
    is_done = models.BooleanField(
        _('Is goal done?'),
        default=False,
        help_text=_(
            'Designates whether the goal should be treated as completed'
        ),
    )

    def __str__(self) -> str:
        return f'Goal {self.id} of {self.review.employee.full_name} - {self.review.year}'


class Criteria(TimeStampedModel):
    goal = models.ForeignKey(
        'performance_review.Goal',
        verbose_name=_('Goal'),
        on_delete=models.CASCADE,
        related_name='criteria',
    )
    text = models.TextField(_('Text'), max_length=1000)
    is_done = models.BooleanField(
        _('Is criteria done?'),
        default=False,
        help_text=_(
            'Designates whether the criteria should be treated as completed'
        ),
    )
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    deadline = models.DateField(_('Deadline'), null=True, blank=True)
    finish_date = models.DateField(_('Finish Date'), null=True, blank=True)

    def __str__(self) -> str:
        return f'Criteria of goal id {self.goal.id} - ' \
               f'{self.goal.review.employee.full_name} - ' \
               f'{self.goal.review.year}'


class Comment(TimeStampedModel):
    author = models.ForeignKey(
        'employee.Employee',
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
        related_name='comments',
    )
    text = models.TextField(_('Text'), max_length=2000)
    goal = models.ForeignKey(
        'performance_review.Goal',
        verbose_name=_('Goals'),
        on_delete=models.CASCADE,
        related_name='comments',
    )
