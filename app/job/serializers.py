"""
Serializers for Job API
"""

from rest_framework import serializers
from core.models import JobTitle, Portal


class JobTitleSerializer(serializers.ModelSerializer):
    """
    Serializer class for JobTitle list view
    """
    class Meta:
        model = JobTitle
        fields = ["id", "title"]
        read_only_fields = ["id"]


class JobTitleDetailSerializer(JobTitleSerializer):
    """Serializer class for JobTitle detail view

    WE will reuse functionality written under `JobTitleSerializer`
    By these means, we are avoiding duplicates in code.

    Writing nested serializers
    """

    class Meta(JobTitleSerializer.Meta):
        fields = JobTitleSerializer.Meta.fields + [
            "job_description", "portal"
        ]


class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portal
        fields = ["name", "description"]
        read_only_fields = ["id"]

