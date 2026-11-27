from django.core.management.base import BaseCommand
from telemetry.models import TelemetryRecord

class Command(BaseCommand):
    help = "Create 50 sample satellite telemetry records"

    def handle(self, *args, **options):
        if TelemetryRecord.objects.exists():
            self.stdout.write(self.style.WARNING("Telemetry records already exist. No duplicates added."))
            return

        records = []
        for number in range(1, 51):
            altitude = 400 + ((number * 37) % 1200)
            temperature = 24 + ((number * 7) % 25)
            battery = 48 + ((number * 13) % 51)
            if battery < 58 or temperature > 44:
                status = "Critical"
            elif battery < 68 or temperature > 40:
                status = "Warning"
            else:
                status = "Active"

            records.append(TelemetryRecord(
                satellite_id=f"SAT-{number:03d}",
                altitude=altitude,
                temperature=temperature,
                battery=battery,
                signal_strength=2 + ((number * 3) % 3),
                status=status,
            ))

        TelemetryRecord.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS("Successfully created 50 telemetry records."))
