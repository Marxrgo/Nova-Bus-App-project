from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the shared Nova Bus staff account without granting Django superuser access."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="nova_staff")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        if User.objects.filter(username=username).exists():
            raise CommandError(f"A user named '{username}' already exists.")

        password = getpass("Password: ")
        confirm = getpass("Password (again): ")

        if password != confirm:
            raise CommandError("Passwords do not match.")

        user = User(username=username, is_staff=True, is_active=True)
        user.set_password(password)
        user.full_clean(exclude=["password"])
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created shared staff account '{username}'. Django superuser access is OFF."
            )
        )
