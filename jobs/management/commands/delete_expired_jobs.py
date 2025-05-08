from django.core.management.base import BaseCommand
from jobs.models import Job
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Delete jobs older than 7 days"

    def handle(self, *args, **kwargs):
        one_week_ago = now() - timedelta(days=7)
        expired_jobs = Job.objects.filter(created_at__lt=one_week_ago)
        count = expired_jobs.count()
        expired_jobs.delete()
        self.stdout.write(f"Deleted {count} expired jobs.")