from rest_framework import serializers
from .models import *


class PhoneSerializer(serializers.ModelSerializer):
    full_number = serializers.CharField(read_only=True)
    class Meta:
        model = Phone
        fields = ['id','country_code', 'national_number', 'full_number']
        





class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name','slug', 'website', 'description', 'logo',
            'contact_email', 'created_at', 'phone'
        ]

        read_only_fields = [ 'created_at']

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
        read_only_fields = ['posted_by','posted_at']

class ApplicationSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(read_only=True)
    phone_id = serializers.PrimaryKeyRelatedField(queryset=Phone.objects.all(), source='phone', write_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'full_name', 'email', 'phone', 'phone_id',
            'cover_letter', 'resume', 'created_at'

        ]
        read_only_fields = ['status','created_at']

  
