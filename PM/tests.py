from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import BusSlot, Looptype
# Create your tests here.

#TODO: its gonna be a headache to change this when renaming everything

User = get_user_model()

#Basically creating functions for django test to use
#Has to have test_' before function so django knows to test it
class LoopDashboardTests(TestCase):
    '''Runs setUp w/test then rollsback db''' 
    def setUp(self): #Django runs this first ; Django always runs this before the rest of these functions lmao
        self.music_slot = BusSlot.objects.create(loop=Looptype.MUSIC, slot_number=1)
        self.ib_slot = BusSlot.objects.create(loop=Looptype.IB, slot_number=1)

    def test_music_dashboard_loads_for_anonymous_user(self): # Tests if anynomous users are in Student view permissions
        response = self.client.get(reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student view")

    def test_ib_dashboard_loads_for_anonymous_user(self): # Same check but for IB loop's own page now
        response = self.client.get(reverse("loops:loop_dashboard", args=["IB"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student view")

    def test_dashboard_shows_staff_mode_for_staff_user(self): #Tests if staff users are in staff view permissions
        staff = User.objects.create_user(username="staffer", password="pw12345!", is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.assertContains(response, "Staff editing mode")

    def test_dashboard_shows_empty_slot(self): #Tests if slots show Empty
        response = self.client.get(reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.assertContains(response, "Empty")

    def test_dashboard_shows_assigned_bus_number(self): #Tests if updating slots working
        self.music_slot.bus_number = 2256
        self.music_slot.save()
        response = self.client.get(reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.assertContains(response, "2256")

    def test_music_dashboard_does_not_show_ib_slots(self): # Confirms the split actually keeps loops separate
        self.ib_slot.bus_number = 9999
        self.ib_slot.save()
        response = self.client.get(reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.assertNotContains(response, "9999")

    def test_invalid_loop_name_returns_404(self): # New page is parameterized now, so bad loop names need checking
        response = self.client.get(reverse("loops:loop_dashboard", args=["FAKE"]))
        self.assertEqual(response.status_code, 404)


class UpdateSlotPermissionTests(TestCase):
    def setUp(self): #creates test busslot and different test accounts ; basically setups vars for tests
        self.slot = BusSlot.objects.create(loop = Looptype.MUSIC, slot_number = 1)
        self.url = reverse("loops:update_slot", args=[self.slot.id])

        self.music_manager = User.objects.create_user(username="music_mgr", password="pw12345!", is_staff=True, managed_loop=Looptype.MUSIC)
        self.ib_manager = User.objects.create_user(username="ib_mgr", password="pw12345!", is_staff=True, managed_loop=Looptype.IB)
        self.superuser = User.objects.create_superuser(username="admin", password="pw12345!", email="admin@example.com")

    def test_anonymous_user_redirected_to_login(self): #Tests if links redirects to login page for random(non admin) users
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_wrong_loop_manager_gets_permission_denied(self):
        self.client.force_login(self.ib_manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_correct_loop_manager_can_view_form(self):
        self.client.force_login(self.music_manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_view_form_for_any_loop(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class UpdateSlotSubmissionTests(TestCase):
    def setUp(self): #Sets up a staff acc
        self.slot = BusSlot.objects.create(loop=Looptype.MUSIC, slot_number=1)
        self.url = reverse("loops:update_slot", args=[self.slot.id])
        self.manager = User.objects.create_user(
            username="music_mgr", password="pw12345!", is_staff=True, managed_loop=Looptype.MUSIC
        )
        self.client.force_login(self.manager)

    def test_assigning_a_bus_number(self):
        response = self.client.post(self.url, {"bus_number": 2256})
        # Redirect now goes to this slot's own loop page, not a shared dashboard
        self.assertRedirects(response, reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.bus_number, 2256)

    def test_removing_a_bus_number(self):
        self.slot.bus_number = 2256
        self.slot.save()

        response = self.client.post(self.url, {"bus_number": ""})
        self.assertRedirects(response, reverse("loops:loop_dashboard", args=["MUSIC"]))
        self.slot.refresh_from_db()
        self.assertIsNone(self.slot.bus_number)

    def test_invalid_bus_number_does_not_save(self):
        response = self.client.post(self.url, {"bus_number": "not-a-number"})
        self.assertEqual(response.status_code, 200)  # re-renders form with errors
        self.slot.refresh_from_db()
        self.assertIsNone(self.slot.bus_number)


class ClearLoopTests(TestCase):
    def setUp(self):
        self.music_slot = BusSlot.objects.create(loop=Looptype.MUSIC, slot_number=1, bus_number=1234)
        self.ib_slot = BusSlot.objects.create(loop=Looptype.IB, slot_number=1, bus_number=5678)
        self.url = reverse("loops:clear_loop", args=["MUSIC"])

        self.music_manager = User.objects.create_user(
            username="music_mgr", password="pw12345!", is_staff=True, managed_loop=Looptype.MUSIC
        )
        self.ib_manager = User.objects.create_user(
            username="ib_mgr", password="pw12345!", is_staff=True, managed_loop=Looptype.IB
        )

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_wrong_loop_manager_gets_permission_denied(self):
        self.client.force_login(self.ib_manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_shows_confirmation_page_without_clearing(self):
        self.client.force_login(self.music_manager)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.music_slot.refresh_from_db()
        self.assertEqual(self.music_slot.bus_number, 1234)  # untouched

    def test_post_clears_only_the_target_loop(self):
        self.client.force_login(self.music_manager)
        response = self.client.post(self.url)
        # Redirect now goes to Music's own loop page, not a shared dashboard
        self.assertRedirects(response, reverse("loops:loop_dashboard", args=["MUSIC"]))

        self.music_slot.refresh_from_db()
        self.ib_slot.refresh_from_db()
        self.assertIsNone(self.music_slot.bus_number)
        self.assertEqual(self.ib_slot.bus_number, 5678)  # other loop untouched

    def test_invalid_loop_returns_404(self):
        self.client.force_login(self.music_manager)
        response = self.client.get(reverse("loops:clear_loop", args=["FAKE"]))
        self.assertEqual(response.status_code, 404)