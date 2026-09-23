from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Project, ProjectImage


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class PortfolioViewTests(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(
            username="creator", password="password"
        )
        self.published = Project.objects.create(
            title="Fitted kitchen",
            slug="fitted-kitchen",
            description="A custom kitchen.",
            cover_image="projects/kitchen.jpg",
            created_by=self.creator,
            status=Project.Status.PUBLISHED,
        )
        Project.objects.create(
            title="Private project",
            slug="private-project",
            description="Not ready.",
            cover_image="projects/private.jpg",
            created_by=self.creator,
            status=Project.Status.DRAFT,
        )

    def test_list_excludes_drafts(self):
        response = self.client.get(reverse("portfolio:list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["projects"]), [self.published])

    def test_detail_hides_drafts(self):
        response = self.client.get(
            reverse("portfolio:detail", args=["private-project"])
        )

        self.assertEqual(response.status_code, 404)

    def test_project_detail_includes_gallery_images(self):
        image = ProjectImage.objects.create(
            project=self.published,
            image="projects/gallery/kitchen-detail.jpg",
            caption="Oak worktop",
        )

        response = self.client.get(
            reverse("portfolio:detail", args=[self.published.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["project"].images.all()),
            [image],
        )
