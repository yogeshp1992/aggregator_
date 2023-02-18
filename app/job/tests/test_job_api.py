"""Tests for job API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

from django.urls import reverse, reverse_lazy

# We have registered `core` as an application under `INSTALLED_APPS`
from core.models import JobTitle, Portal, JobDescription
from job.serializers import JobTitleSerializer, JobTitleDetailSerializer


JOB_TITLE_URL = reverse("jobtitle:jobtitle-list")  # /api/jobtitle/jobtitles

"""
TODO - refer
https://www.django-rest-framework.org/api-guide/routers/#routers
reverse(<applicationname>:<basename>-list)
reverse(<applicationname>:<basename>-detail)
"""


def create_user(**params):
    """Create and return a new user"""

    return get_user_model().objects.create_user(**params)


def detail_url(job_title_id):
    """create and return a job title detail URL"""

    return reverse("jobtitle:jobtitle-detail", args=[job_title_id])


def create_job_description(user, **params):
    """create and return new job description"""

    defaults = {
        "user": user,
        "role": "Simple Job Title",
        "description_text": "should know git,CICD, Linux and must know Python",
        "pub_date": timezone.now()
    }
    defaults.update(**params)
    job_description = JobDescription.objects.create(**defaults)
    return job_description


def create_job_title(user, portal, job_description, **params):
    """create and return a sample job title"""

    defaults = {
        "title": "Simple Job Title"
    }
    defaults.update(params)
    job_title = JobTitle.objects.create(
        user=user,
        job_description=job_description,
        portal=portal,
        **params
    )
    return job_title


class PublicJobTitleApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth required API call"""

        res = self.client.get(JOB_TITLE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobTitleApiTests(TestCase):
    """Test authorized API requests"""

    def setUp(self) -> None:
        """Test fixtures"""

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "password@321"
        )

        # portal
        self.portal = Portal.objects.create(
            user=self.user,
            name="naukri.com",
            description="famous job hunting website"
        )

        # job_description
        self.job_description = JobDescription.objects.create(
            user=self.user,
            role="To build backend microservices",
            description_text="should know git,CICD, Linux and must know Python",
            pub_date=timezone.now()
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_job_titles(self):
        """Test retrieving a list of job titles"""

        create_job_title(
            user=self.user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description(
                self.user
            )
        )
        create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )

        job_titles = JobTitle.objects.all().order_by("-id")
        serializer = JobTitleSerializer(job_titles, many=True)

        res = self.client.get(JOB_TITLE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_job_title_list_limited_to_user(self):
        """Test list of job titles is limited to authenticated user"""

        other_user = get_user_model().objects.create_user(
            "other@example.com",
            "password@123"
        )
        create_job_title(
            user=other_user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description(other_user)
        )
        create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )

        res = self.client.get(JOB_TITLE_URL)

        job_titles = JobTitle.objects.all()
        job_titles = job_titles.filter(user=self.user).order_by("-id")
        serializer = JobTitleSerializer(job_titles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_jobtitle_detail(self):
        """Test get details of particular job title"""

        job_title = create_job_title(
            user=self.user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )
        url = detail_url(job_title.id)
        res = self.client.get(url)
        serializer = JobTitleDetailSerializer(job_title)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_create_job_title(self):
        """Test creating a jobtitle"""

        # NOTE :: no need to pass user_id in payload
        # user_id will be picked from request attributes.
        payload = {
            "title": "Python developer",
            "portal": self.portal.id,
            "job_description": self.job_description.id
        }

        res = self.client.post(JOB_TITLE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        job_title = JobTitle.objects.get(id=res.data["id"])
        self.assertEqual(self.portal.id, res.data["portal"])
        self.assertEqual(self.job_description.id, res.data["job_description"])
        self.assertEqual(job_title.user, self.user)

    def test_partial_job_title_update(self):
        """Test partial update of a job title"""

        job_title = create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=self.job_description
        )

        payload = {
            "title": "Python developer",
            "portal": self.portal.id,
            "job_description": self.job_description.id
        }

        url = detail_url(job_title.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Need to reload DB when doing a patch request
        # by default model is not refreshed
        # (django does not automatically refresh field once we retrieve them)
        job_title.refresh_from_db()
        self.assertEqual(job_title.title, payload["title"])
        self.assertEqual(job_title.user, self.user)

    def test_full_update_job_title(self):
        """Test full update of job title"""

        job_title = create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )
        payload = {
            "title": "Python developer",
            "portal": self.portal.id,
            "job_description": self.job_description.id
        }
        url = detail_url(job_title.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        job_title.refresh_from_db()

        portal = Portal.objects.get(id=res.data["portal"])
        self.assertEqual(portal.id, self.portal.id)
        job_description = JobDescription.objects.get(
            id=res.data["job_description"]
        )
        self.assertEqual(job_description.id, self.job_description.id)
        self.assertEqual(job_title.user, self.user)

    def test_jobtitle_update_user_makes_no_difference(self):
        """Test changing the jobtitle user results in no difference"""

        new_user = create_user(
            email="otheruser@example.com",
            password="password@3210"
        )
        job_title = create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )
        payload = {
            "title": "Python developer",
            "portal": self.portal.id,
            "user": new_user.id,
            "job_description": self.job_description.id
        }
        url = detail_url(job_title.id)
        self.client.patch(url, payload)

        job_title.refresh_from_db()
        self.assertEqual(job_title.user, self.user)

    def test_delete_job_title(self):
        """Test deleting a job title successful"""

        job_title = create_job_title(
            user=self.user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )

        url = detail_url(job_title.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobTitle.objects.filter(id=job_title.id).exists())

    def test_job_title_other_users_jobtitle_error(self):
        """Test trying to delete another users jobtitle gives error"""

        new_user = create_user(
            email="otheruser@example.com",
            password="password@3210"
        )
        job_title = create_job_title(
            user=new_user,
            title="DEVOPS Engineer",
            portal=self.portal,
            job_description=create_job_description(self.user)
        )

        url = detail_url(job_title.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(JobTitle.objects.filter(id=job_title.id).exists())



