import django_filters
from .models import *
from django import forms

class JobFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="salary_min",
        lookup_expr="gte",
        label="Minimum Salary",
        widget = forms.NumberInput(attrs={"placeholder": "Min salary"})
    )

    max_salary = django_filters.NumberFilter(
        field_name="salary_max",
        lookup_expr="lte",
        label="Maximum Salary",
        widget = forms.NumberInput(attrs={"placeholder": "Max Salary"})

       )
    
    company = django_filters.ModelChoiceFilter(
        queryset=Company.objects.all(),
        empty_label = "Any company",
        label="Company",
    )

    location = django_filters.CharFilter(
        lookup_expr="icontains",
        label="location",
        widget = forms.TextInput(attrs={"placeholder": "Location"})
    )

    job_type = django_filters.ChoiceFilter(
        choices = Job.JOB_TYPE_CHOICES,
        empty_label = "Any type",

        label= "Job type"
    )

    remote = django_filters.BooleanFilter(
        label="Remote",
        widget = forms.CheckboxInput()
    )

    posted_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Posted After",
        widget = forms.DateInput(attrs={"type": "date"})
    )

    posted_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Posted Before",
        widget = forms.DateInput(attrs={"type":"date"})
    )

    ordering = django_filters.OrderingFilter(
        fields= (
            ("salary_min", "salary"),
            ("created_at", "date_posted"),
        ),
        field_labels={
            "salary_min" : "Salary",
            "created_at" : "Date Posted",
        },
        label="Order By"
    )

    class Meta:
        model = Job
        fields = [
            "location",
            "job_type",
            "remote",
            "company",
            "min_salary",
            "max_salary",
            "posted_after",
            "posted_before"
        ]