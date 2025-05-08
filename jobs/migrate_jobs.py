from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Migrate job titles to categories'

    def handle(self, *args, **kwargs):
        for job in Job.objects.all():
            if job.title in dict(Job.CATEGORY_CHOICES):  
                job.category = job.title
                job.save()
                self.stdout.write(self.style.SUCCESS(f"Migrated job '{job.title}' to category '{job.category}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipping job '{job.title}': Title does not match a valid category."))