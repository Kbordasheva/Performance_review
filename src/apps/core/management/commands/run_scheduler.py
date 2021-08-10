from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management import BaseCommand

from performance_review.tasks import deadline_notify


class Command(BaseCommand):
    help = 'Run blocking scheduler to create periodical tasks'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        # add periodical tasks
        scheduler.add_job(deadline_notify, CronTrigger(hour=7, minute=30))  # every day at 7:30 UTC (10:30 Minsk)

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
