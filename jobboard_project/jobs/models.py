from django.db import models

from django.contrib.auth import get_user_model
from utils.country_codes import COUNTRY_CODE_CHOICES

User = get_user_model()

JOB_TYPE_CHOICES = [
    ('full_time', 'Full_time'),
    ('part_time', 'Part_time'),
    ('contract', 'Contract',),
    ('internship' , 'Internship'),
]
class Phone(models.Model):
    country_code = models.CharField(
        max_length=5,
        choices=COUNTRY_CODE_CHOICES,
        default="+254",
    )
    national_number = models.CharField(
        max_length=15,
        help_text="Phone number without country code",
    )

    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"

    def __str__(self):
        return f"{self.country_code}{self.national_number}"

    @property
    def full_number(self):
        """Return full E.164-like number"""
        return f"{self.country_code}{self.national_number}"

class Company(models.Model):
    name= models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='companies/logos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(blank=False)
    remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="Full_time")
    description = models.TextField(blank=False)
    short_description = models.TextField(blank=False)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"
    


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, blank=True)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField( upload_to='application/resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Application by {self.full_name} for {self.job.title}"


