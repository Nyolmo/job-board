from django.db import models

from user.models import User
from django.forms import ValidationError
from jobs.utils.country_codes import COUNTRY_CODE_CHOICES
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.text import slugify



JOB_TYPE_CHOICES = [
    ('full_time', 'Full_time'),
    ('part_time', 'Part_time'),
    ('contract', 'Contract',),
    ('internship' , 'Internship'),
]


class AutoSlugModel(models.Model):
    slug= models.SlugField(unique=True, blank=True,null=True, max_length=255)

    slug_source_field = None

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.slug_source_field:
                raise ValueError("slug_source_field must be defined to auto-generate slug.")
            base_slug = slugify(getattr(self, self.slug_source_field))
            slug = base_slug
            counter = 1

            ModelClass = self.__class__

            while ModelClass.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)





class Phone(models.Model):
    country_code = models.CharField(
        max_length=5,
        choices=COUNTRY_CODE_CHOICES,
        default="+254",
        help_text="Country code for the phone number",
    )
    national_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\d{4,15}$',
            message = 'Phone number must contain only digits(4-15)')],  
        help_text="Phone number without country code",
    )

    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
        unique_together = ('country_code', 'national_number')

    def __str__(self):
        return f"{self.country_code}{self.national_number}"

    @property
    def full_number(self):
        """Return full E.164-like number"""
        return f"{self.country_code}{self.national_number}"

class Company(AutoSlugModel):
    slug_source_field = "name"
    name= models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='companies/logos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Job(AutoSlugModel):
    slug_source_field = "title"
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(blank=False)
    remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    description = models.TextField(blank=False)
    short_description = models.TextField(blank=True)
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0)]
        )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0)]
        )
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_at']
        indexes = [
            models.Index(fields=['title', 'location', 'job_type']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company.name}"
    
    def clean(self):
        #ensuring salary range is valid
        if self.salary_min and self.salary_max:
            if self.salary_min > self.salary_max:
                raise ValidationError('Minimum salary cannot exceed the maximum salary.')

    


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
   

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField( upload_to='application/resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"Application by {self.full_name} for {self.job.title}"


