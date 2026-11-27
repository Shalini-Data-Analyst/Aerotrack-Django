
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Create AeroTrack demo login"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        username = "Shalini"
        password = "38820746"

        user, created = User.objects.get_or_create(
            username=username
        )

        user.set_password(password)
        user.is_active = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "AeroTrack login created successfully!"
            )
        )
