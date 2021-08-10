from django.core.management import BaseCommand

from performance_review.tasks import deadline_notify


class Command(BaseCommand):
    help = 'Send a notification to all employees whose goal criteria meet the deadline'

    def handle(self, *args, **options):
        deadline_notify()
