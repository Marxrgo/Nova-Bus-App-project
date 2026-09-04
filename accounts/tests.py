from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="nova_staff",
            password="ExamplePassword123!",
            is_staff=True,
        )

    def test_account_home_requires_login(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:home')}",
        )

    def test_staff_can_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "nova_staff", "password": "ExamplePassword123!"},
        )
        self.assertRedirects(response, reverse("accounts:home"))
        
    def test_account_home_loads_after_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nova_staff")
