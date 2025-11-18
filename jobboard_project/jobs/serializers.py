from rest_framework import serializers
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), source='company', write_only=True)


    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'company_id', 'location',
            'remote', 'job_type', 'description', 'short_description',
            'salary_min', 'salary_max', 'posted_by', 'posted_at',
            'is_active'
        ]
        read_only_fields = ['id','posted_by','posted_at']

class ApplicationSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'full_name', 'email', 'phone',
            'cover_letter', 'resume', 'created_at'

        ]

    def create(self, validated_data):
        return super().create(validated_data)
