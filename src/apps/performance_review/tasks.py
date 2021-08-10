from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from employee.models import Employee
from performance_review.models import Criteria


def deadline_notify():
    all_criteria = Criteria.objects.filter(is_done=False)\
        .select_related('goal', 'goal__review', 'goal__review__employee')
    for criteria in all_criteria:
        expiration_date = criteria.deadline
        delta = expiration_date - timezone.now().date()
        if 7 >= delta.days > 0:
            employee = criteria.goal.review.employee
            _notify(employee.id, criteria.id, delta.days)


def _notify(employee_id, criteria_id, delta):
    send_message(employee_id, criteria_id, delta)


@shared_task
def send_message(employee_id, criteria_id, days):
    employee = Employee.objects.get(id=employee_id)
    criteria = Criteria.objects.get(id=criteria_id)
    subject = f'Attention! Criteria {criteria_id} is about to meet deadline'
    message = f'Hello! Please pay attention that the criteria {criteria_id} - ' \
              f' "{criteria.text}" of the goal "{criteria.goal.text}" is about to meet the deadline in {days} days'
    email_from = 'example@pr-example.com'
    mail_sent = send_mail(subject, message,
                          email_from,
                          [employee.email],
                          fail_silently=False)
    return mail_sent
