"""Views for Job API

TODO EXERCISE
-------
1. Create similar endpoints (list, detail) for `portal`
2. Write as many test cases as you can for `portal` endpoints
3. Create similar endpoints (list, detail) for `job_description`
4. Write as many test cases as you can for `job_description` endpoints

"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

## import models
from core.models import JobTitle
from job import serializers


class JobTitleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.JobTitleDetailSerializer

    # represents objects that are available for this viewset.
    # queryset objects that are manageable by this view.
    queryset = JobTitle.objects.all()

    # In order to use endpoint provided by this viewset, we will need ]
    # authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        We want to filter out jobtitles for authenticated users
        """

        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Returns the serializer class to be used for the request"""

        if self.action == "list":
            return serializers.JobTitleSerializer
        return self.serializer_class

