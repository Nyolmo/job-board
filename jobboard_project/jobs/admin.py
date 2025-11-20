from django.contrib import admin
from .models import Company, Job, Application, Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("id", "country_code", "national_number", "full_number")
    search_fields = ("national_number",)
    list_filter = ("country_code",)


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ("full_name", "email", "phone", "resume", "created_at")
    can_delete = False


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "website",  "description","created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "company", "location",
        "remote", "job_type",
        "salary_min", "salary_max",
        "posted_by", "posted_at", "is_active",
    )
    list_filter = (
        "remote", "job_type", "is_active",
        "posted_at", "company",
    )
    search_fields = ("title", "company__name", "location")
    ordering = ("-posted_at",)
    inlines = [ApplicationInline]

    readonly_fields = ("posted_at",)

    fieldsets = (
        ("Job Details", {
            "fields": ("title", "company", "location", "remote", "job_type")
        }),
        ("Descriptions", {
            "fields": ("short_description", "description")
        }),
        ("Salary Info", {
            "fields": ("salary_min", "salary_max")
        }),
        ("Meta", {
            "fields": ("posted_by", "posted_at", "is_active")
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "full_name", "email",
        "job", "phone", "created_at"
    )
    search_fields = ("full_name", "email", "job__title")
    list_filter = ("created_at", "job")
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Applicant Info", {
            "fields": ("full_name", "email", "phone")
        }),
        ("Job", {
            "fields": ("job",)
        }),
        ("Application Details", {
            "fields": ("cover_letter", "resume")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )
