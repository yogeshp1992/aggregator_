"""
Serializers for Job API
"""

from rest_framework import serializers
from core.models import JobTitle


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = "__all__"
        read_only_fields = ["id"]

