from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import UserJob
from occupation.models import Location, Employer, Job


def post_save_user_job(sender, instance, created, *args, **kwargs):
    job = instance.position.lower()
    location = instance.location.lower()
    employer_name = instance.employer_name.lower()
    new_job = Job.objects.get_or_create(text=job)
    new_location, created = Location.objects.get_or_create(name=location)
    new_employer = Employer.objects.get_or_create(location=new_location, name=employer_name)


post_save.connect(post_save_user_job, sender=UserJob)
