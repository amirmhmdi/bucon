from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post


@override_settings(
	STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class BlogViewTests(TestCase):
	def setUp(self):
		self.author = User.objects.create_user(
			username="author", password="password"
		)
		self.published = Post.objects.create(
			title="Published guide",
			slug="published-guide",
			author=self.author,
			content="Published content",
			status=Post.Status.PUBLISHED,
		)
		Post.objects.create(
			title="Draft guide",
			slug="draft-guide",
			author=self.author,
			content="Private content",
			status=Post.Status.DRAFT,
		)

	def test_list_excludes_drafts(self):
		response = self.client.get(reverse("blog:list"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context["posts"]), [self.published])

	def test_detail_hides_drafts(self):
		response = self.client.get(reverse("blog:detail", args=["draft-guide"]))

		self.assertEqual(response.status_code, 404)

	def test_published_detail_is_available(self):
		response = self.client.get(
			reverse("blog:detail", args=[self.published.slug])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["post"], self.published)

# Create your tests here.
