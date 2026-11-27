from django.db import models

class TelemetryRecord(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Warning", "Warning"),
        ("Critical", "Critical"),
    ]

    satellite_id = models.CharField(max_length=20, unique=True)
    altitude = models.PositiveIntegerField(help_text="Orbit altitude in kilometres")
    temperature = models.FloatField(help_text="Temperature in Celsius")
    battery = models.PositiveIntegerField(help_text="Battery percentage")
    signal_strength = models.PositiveSmallIntegerField(default=3)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")

    class Meta:
        ordering = ["satellite_id"]
        verbose_name = "Telemetry Record"
        verbose_name_plural = "Telemetry Records"

    def __str__(self):
        return self.satellite_id
